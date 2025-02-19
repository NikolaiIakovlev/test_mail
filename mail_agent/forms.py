from django import forms

from .models import EmailTemplate, Subscriber


class EmailForm(forms.Form):
    """Форма отправки электронной почты"""

    subscribers = forms.ModelMultipleChoiceField(
        queryset=Subscriber.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Адресаты",
    )
    subject = forms.CharField(label="Тема письма", max_length=100)
    message = forms.CharField(label="Текст письма", widget=forms.Textarea)


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "username", "first_name", "last_name", "birthday"]


class EmaiagentlForm(forms.Form):
    subject = forms.CharField(max_length=255, label="Тема")
    message = forms.CharField(widget=forms.Textarea, label="Сообщение")
    recipient = forms.EmailField(label="Получатель")


class MailForm(forms.Form):
    template = forms.ModelChoiceField(
        queryset=EmailTemplate.objects.all(), label="Шаблон"
    )
    subscribers = forms.ModelMultipleChoiceField(
        queryset=Subscriber.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Подписчики",
    )
    title = forms.CharField(max_length=100, label="Заголовок")
    text = forms.CharField(widget=forms.Textarea, label="Текст письма")
    scheduled_time = forms.DateTimeField(
        required=False,
        label="Время отправки",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
