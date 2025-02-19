
from uuid import uuid4
from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.utils import timezone
from django.utils.html import strip_tags

from .models import EmailTemplate, SentEmail, Subscriber


@shared_task
def send_newsletter(subscriber_ids, template_id, title, text):
    """
    Отправка рассылки
    """
    template = EmailTemplate.objects.get(id=template_id)
    subscribers = Subscriber.objects.filter(id__in=subscriber_ids)

    for subscriber in subscribers:
        unique_id = str(uuid4())
        context = {
            "first_name": subscriber.first_name or None,
            "last_name": subscriber.last_name or None,
            "email": subscriber.email,
            "unique_id": unique_id,
            "title": title,
            "text": text or None,
        }

        template_instance = Template(template.html_content)
        context_instance = Context(context)
        html_content = template_instance.render(context_instance)

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=title,
            body=text_content,
            from_email=EMAIL_HOST_USER,
            to=[subscriber.email],
        )

        email.attach_alternative(html_content, "text/html")

        tracking_pixel_url = f'<img src="http://127.0.0.1:8000/track_open?email={subscriber.email}&id={unique_id}" width="1" height="1" style="display: none;" />'
        html_content += tracking_pixel_url
        email.send()

        sent_email = SentEmail.objects.create(
            subject=template.subject,
            message=html_content,
            sent_at=timezone.now(),
            unique_id=unique_id,
        )

        sent_email.subscribers.set(subscribers)

    return f"Рассылка успешно отправлена для {len(subscribers)} подписчиков!"
