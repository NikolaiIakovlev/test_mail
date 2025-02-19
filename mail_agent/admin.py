from django.contrib import admin

from .models import EmailOpen, EmailTemplate, SentEmail, Subscriber


class SentEmailAdmin(admin.ModelAdmin):
    list_display = ("subject", "sent_at", "status", "id")  # Поля для отображения
    list_filter = ("status", "sent_at")  # Фильтры по статусу и времени отправки
    search_fields = ("subject", "message")  # Поиск по теме и сообщению
    list_editable = ("status",)  # Сделать поле статус редактируемым прямо из списка
    readonly_fields = ("unique_id", "sent_at")  # Только для чтения

    def subscribers_count(self, obj):
        return obj.subscribers.count()  # Количество подписчиков в рассылке

    subscribers_count.short_description = "Количество подписчиков в рассылке"


admin.site.register(SentEmail, SentEmailAdmin)
admin.site.register(Subscriber)
admin.site.register(EmailOpen)
admin.site.register(EmailTemplate)


# admin.site.register(Mailing)
# admin.site.register(OpenTracking)
# admin.site.register(EmailOpen)
# admin.site.register(Subscriber)
# admin.site.register(EmailTemplate)
# admin.site.register(SentEmail)


# @admin.register(Subscriber)
# class SubscriberAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name')

# @admin.register(EmailTemplate)
# class EmailTemplateAdmin(admin.ModelAdmin):
#     list_display = ('name', 'subject')

# @admin.register(SentEmail)
# class SentEmailAdmin(admin.ModelAdmin):
#     list_display = ('subject', 'recipient', 'sent_at')
