# Generated by Django 4.2.19 on 2025-02-17 10:12

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название"
                    ),
                ),
                ("subject", models.CharField(max_length=255, verbose_name="Тема")),
                ("html_content", models.TextField(verbose_name="HTML-содержимое")),
            ],
            options={
                "verbose_name": "Шаблон электронной почты",
                "verbose_name_plural": "Шаблоны электронной почты",
            },
        ),
        migrations.CreateModel(
            name="Subscriber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Электронная почта"
                    ),
                ),
                ("first_name", models.CharField(max_length=100, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                ("username", models.CharField(max_length=100, verbose_name="Логин")),
                ("birthday", models.DateField(verbose_name="Дата рождения")),
            ],
            options={
                "verbose_name": "Подписчик",
                "verbose_name_plural": "Подписчики",
            },
        ),
        migrations.CreateModel(
            name="SentEmail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(max_length=255, verbose_name="Тема письма"),
                ),
                ("message", models.TextField(verbose_name="Сообщение")),
                (
                    "sent_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время отправки"
                    ),
                ),
                (
                    "unique_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        unique=True,
                        verbose_name="Идентификатор рассылки",
                    ),
                ),
                (
                    "subscribers",
                    models.ManyToManyField(
                        related_name="emails_sent",
                        to="mail_agent.subscriber",
                        verbose_name="Подписчики",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отправленное письмо",
                "verbose_name_plural": "Отправленные письма",
            },
        ),
        migrations.CreateModel(
            name="EmailOpen",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("opened_at", models.DateTimeField(auto_now_add=True)),
                ("unique_id", models.UUIDField()),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opens",
                        to="mail_agent.sentemail",
                        verbose_name="Рассылка",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opens",
                        to="mail_agent.subscriber",
                        verbose_name="Подписчик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Открытие электронной почты",
                "verbose_name_plural": "Открытия электронной почты",
            },
        ),
    ]
