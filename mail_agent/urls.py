from django.urls import path

from . import views
from .views import (AddRecipientView, DeleteRecipientView, EditRecipientView,
                    IndexView, RecipientsListView, SentEmailsView,
                    TrackOpenView)

urlpatterns = [
    path(
        "", IndexView.as_view(), name="index"
    ),  # URL для отправки рассылки и вывода главной страницы
    path(
        "track_open/", TrackOpenView.as_view(), name="track_open"
    ),  # URL для отслеживания открытия письма
    path(
        "recipients/", RecipientsListView.as_view(), name="recipients"
    ),  # URL для просмотра списка подписчиков
    path(
        "add/", AddRecipientView.as_view(), name="add_recipient"
    ),  # URL для добавления подписчика на рассылку
    path(
        "edit/<int:recipient_id>/", EditRecipientView.as_view(), name="edit_recipient"
    ),  # URL для редактирования подписчика
    path(
        "delete/<int:recipient_id>/",
        DeleteRecipientView.as_view(),
        name="delete_recipient",
    ),  # URL для удаления подписчика
    path(
        "sent_emails/", SentEmailsView.as_view(), name="sent_emails"
    ),  # URL для просмотра отправленных писем
    path(
        "load_templates/", views.load_templates, name="load_templates"
    ),  # URL для загрузки шаблонов
    path(
        "load_subscribers/", views.load_subscribers, name="load_subscribers"
    ),  # URL для загрузки подписчиков
]