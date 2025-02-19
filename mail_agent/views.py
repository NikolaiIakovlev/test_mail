
from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware
from django.views.generic import (CreateView, DeleteView, ListView, UpdateView,
                                  View)
from django.views.generic.edit import FormView
from mail_agent.models import Subscriber
from PIL import Image

from .forms import MailForm, RecipientForm
from .models import EmailOpen, EmailTemplate, SentEmail, Subscriber
from .tasks import send_newsletter


# Контроллер для отслеживания открытия письма
class TrackOpenView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get("email")
        unique_id = request.GET.get("id")

        if not email or not unique_id:
            return JsonResponse(
                {"status": "error", "message": "Неверный запрос"}, status=400
            )

        # Найти рассылку по уникальному идентификатору
        mailing = get_object_or_404(SentEmail, unique_id=unique_id)
        subscriber = get_object_or_404(Subscriber, email=email)

        # Сохранение события открытия в базе данных
        EmailOpen.objects.create(
            unique_id=unique_id,
            opened_at=timezone.now(),
            mailing=mailing,  # Добавляем ссылку на рассылку
            subscriber=subscriber,  # Добавляем подписчика
        )
        mailing.status = 2
        mailing.save()

        # Создание пустого изображения 1x1 пиксель
        img = Image.new("RGB", (1, 1), color=(255, 255, 255))
        img_io = BytesIO()
        img.save(img_io, "PNG")

        # Возвращаем изображение как ответ
        img_io.seek(0)
        return HttpResponse(img_io, content_type="image/png")


class IndexView(FormView):
    """
    Контроллер для отправки рассылки
    """

    template_name = "index.html"
    form_class = MailForm

    # Обработка отправки рассылки
    def form_valid(self, form):
        template_id = self.request.POST.get("template")
        subscriber_ids = self.request.POST.getlist("subscribers")
        title = self.request.POST.get("title")
        text = self.request.POST.get("text")
        scheduled_time = form.cleaned_data.get("scheduled_time")

        # Если дата и время указаны, делаем их aware (с учетом часового пояса)
        if scheduled_time:
            # Если дата уже aware, не применяем make_aware
            if not is_aware(scheduled_time):
                scheduled_time = make_aware(scheduled_time)

        # Если не указана дата и время, отправляем сразу
        if not scheduled_time:
            scheduled_time = timezone.now()

        # Проверка, если время отправки в прошлом, отправляем сразу
        if scheduled_time < timezone.now():
            scheduled_time = timezone.now()

        # Отправка задачи в Celery с учетом времени отправки
        send_newsletter.apply_async(
            args=[subscriber_ids, template_id, title, text], eta=scheduled_time
        )

        return JsonResponse(
            {"status": "success", "message": "Рассылка успешно отправлена!"}
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def load_templates(request):
    """Представление для загрузки шаблонов рассылок"""
    templates = EmailTemplate.objects.all()
    return JsonResponse(
        {
            "templates": [
                {"id": template.id, "name": template.name} for template in templates
            ]
        }
    )


def load_subscribers(request):
    """Представление для загрузки подписчиков"""
    subscribers = Subscriber.objects.all()
    return JsonResponse(
        {
            "subscribers": [
                {
                    "id": subscriber.id,
                    "first_name": subscriber.first_name,
                    "last_name": subscriber.last_name,
                }
                for subscriber in subscribers
            ]
        }
    )


class AddRecipientView(CreateView):
    """Представление для добавления адресата"""

    model = Subscriber
    form_class = RecipientForm
    template_name = "add_recipient.html"
    success_url = reverse_lazy(
        "recipients"
    )  # Перенаправление на список адресатов после сохранения


class EditRecipientView(UpdateView):
    """Представление для редактирования адресата"""

    model = Subscriber
    form_class = RecipientForm
    template_name = "edit_recipient.html"
    context_object_name = "recipient"  # Имя переменной для объекта в шаблоне
    success_url = reverse_lazy(
        "recipients"
    )  # Перенаправление на список адресатов после редактирования

    def get_object(self, queryset=None):
        # Получаем объект адресата по id из URL
        recipient_id = self.kwargs.get("recipient_id")
        return get_object_or_404(Subscriber, id=recipient_id)


class DeleteRecipientView(DeleteView):
    """Представление для удаления адресата"""

    model = Subscriber
    template_name = "confirm_delete.html"
    context_object_name = "recipient"  # Имя переменной для объекта в шаблоне
    success_url = reverse_lazy(
        "recipients"
    )  # Перенаправление на страницу со списком адресатов после удаления

    def get_object(self, queryset=None):
        # Получаем объект адресата по id из URL
        recipient_id = self.kwargs.get("recipient_id")
        return get_object_or_404(Subscriber, id=recipient_id)


class SentEmailsView(ListView):
    """Представление для списка отправленных писем"""

    model = SentEmail
    template_name = "sent_emails.html"
    context_object_name = "emails"  # Имя переменной для списка в шаблоне
    queryset = SentEmail.objects.all()  # Все отправленные письма

    def get_queryset(self):
        # Фильтрация и сортировка по дате, если необходимо
        return SentEmail.objects.all().order_by(
            "-sent_at"
        )  # Возвращаем письма, отсортированные по дате отправки (по убыванию)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Вы можете добавить дополнительные данные в контекст, если нужно
        # Например, получение всех шаблонов писем для отображения
        context["templates"] = EmailTemplate.objects.all()

        return context


class RecipientsListView(ListView):
    """Представление для списка адресатов"""

    model = Subscriber
    template_name = "recipients.html"
    context_object_name = "recipients"  # Имя переменной для списка в шаблоне
    queryset = Subscriber.objects.all()  # Все подписчики

    def get_queryset(self):
        # Дополнительная логика фильтрации, если необходимо
        return Subscriber.objects.all()
