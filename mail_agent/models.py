import uuid

from django.db import models


class Subscriber(models.Model):
    """
    Подписчики
    """

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    username = models.CharField(max_length=100, verbose_name="Логин")
    birthday = models.DateField(verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    def opened_emails(self):
        # Количество открытых писем для подписчика
        return EmailOpen.objects.filter(subscriber=self).count()


class EmailTemplate(models.Model):
    """
    Шаблон электронной почты
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    subject = models.CharField(max_length=255, verbose_name="Тема")
    html_content = models.TextField(verbose_name="HTML-содержимое")

    class Meta:
        verbose_name = "Шаблон электронной почты"
        verbose_name_plural = "Шаблоны электронной почты"

    def __str__(self):
        return self.name


class SentEmail(models.Model):
    """
    Отправленное письмо
    """

    DELIVERY_STATUS_CHOICES = (
        (1, "Доставлено"),
        (2, "Прочитано"),
    )

    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Сообщение")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    subscribers = models.ManyToManyField(
        Subscriber, related_name="emails_sent", verbose_name="Подписчики"
    )
    unique_id = models.UUIDField(
        default=uuid.uuid4, unique=True, verbose_name="Идентификатор рассылки"
    )  # Идентификатор для всей рассылки
    status = models.IntegerField(
        choices=DELIVERY_STATUS_CHOICES, default=1, verbose_name="Статус доставки"
    )

    class Meta:
        verbose_name = "Отправленное письмо"
        verbose_name_plural = "Отправленные письма"

    def __str__(self):
        return f"Письмо {self.subject} от {self.sent_at}. Статус: {self.status}"

    def opened_count(self):
        # Количество открытых писем
        return self.opens.count()

    def not_opened_count(self):
        # Количество не открытых писем (если их открытие зафиксировано)
        return self.subscribers.count() - self.opened_count()


class EmailOpen(models.Model):
    """
    Открытие электронной почты
    """

    opened_at = models.DateTimeField(auto_now_add=True)
    mailing = models.ForeignKey(
        SentEmail,
        related_name="opens",
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
    )
    subscriber = models.ForeignKey(
        Subscriber,
        related_name="opens",
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
    )
    unique_id = (
        models.UUIDField()
    )  # Уникальный идентификатор для конкретного подписчика

    class Meta:
        verbose_name = "Открытие электронной почты"
        verbose_name_plural = "Открытия электронной почты"

    def __str__(self):
        return (
            f"{self.subscriber.email} opened {self.mailing.subject} at {self.opened_at}"
        )

    # Метод для обработки открытия письма
    @classmethod
    def track_open(cls, email, unique_id, mailing, subscriber):
        # Проверяем, не открывал ли этот подписчик это письмо ранее
        if not cls.objects.filter(email=email, unique_id=unique_id).exists():
            return cls.objects.create(
                email=email, unique_id=unique_id, mailing=mailing, subscriber=subscriber
            )
        return None  # Возвращаем None, если письмо уже было открыто


# import uuid
# from django.db import models


# class Subscriber(models.Model):
#     """
#     Подписчики
#     """
#     email = models.EmailField(unique=True, verbose_name="Электронная почта")
#     first_name = models.CharField(max_length=100, verbose_name="Имя")
#     last_name = models.CharField(max_length=100, verbose_name="Фамилия")
#     username = models.CharField(max_length=100, verbose_name="Логин")
#     birthday = models.DateField(verbose_name="Дата рождения")

#     class Meta:
#         verbose_name = 'Подписчик'
#         verbose_name_plural = 'Подписчики'

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} <{self.email}>"


# class SentEmail(models.Model):
#     """
#     Рассылка
#     """
#     subject = models.CharField(max_length=255, verbose_name="Тема письма")
#     message = models.TextField(verbose_name="Сообщение")
#     recipient = models.EmailField(verbose_name="Получатель")
#     sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
#     subscribers = models.ManyToManyField(Subscriber, related_name='рассылки', verbose_name="Подписчики")
#     tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Идентификатор")

#     class Meta:
#         verbose_name = 'Отправленное письмо'
#         verbose_name_plural = 'Отправленные письма1'

#     def __str__(self):
#         return f"Письмо {self.subject} отправлено {self.recipient}"


# class EmailOpen(models.Model):
#     """
#     Открытие электронной почты
#     """
#     email = models.EmailField()
#     unique_id = models.CharField(max_length=255, unique=True)
#     opened_at = models.DateTimeField(auto_now_add=True)
#     mailing = models.ForeignKey(SentEmail, related_name='opens', on_delete=models.CASCADE, verbose_name="Рассылка")
#     subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, verbose_name="Подписчик")

#     class Meta:
#         verbose_name = 'Открытие электронной почты'
#         verbose_name_plural = 'Открытия электронной почты'

#     def __str__(self):
#         return f"{self.email} opened at {self.opened_at}"


# class EmailTemplate(models.Model):
#     """
#     Шаблон электронной почты
#     """
#     name = models.CharField(max_length=255, unique=True, verbose_name="Название")
#     subject = models.CharField(max_length=255, verbose_name="Тема")
#     html_content = models.TextField(verbose_name="HTML-содержимое")

#     class Meta:
#         verbose_name = 'Шаблон электронной почты'
#         verbose_name_plural = 'Шаблоны электронной почты'

#     def __str__(self):
#         return self.name
#########################

# class Mailing(models.Model):
#     """
#     Рассылка
#     """
#     subject = models.CharField(max_length=255, verbose_name="Тема")
#     template = models.TextField(verbose_name="Шаблон")
#     scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="Время отправки")
#     sent = models.BooleanField(default=False, verbose_name="Отправлено")
#     subscribers = models.ManyToManyField(Subscriber, related_name='рассылки', verbose_name="Подписчики")
#     tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Идентификатор")

#     class Meta:
#         verbose_name = 'Рассылка'
#         verbose_name_plural = 'Рассылки'

#     def __str__(self):
#         return self.subject
