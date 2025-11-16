from django.contrib import admin
from .models import Mailing, Message, Subscriber, DeliveryStatus


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "comment")
    search_fields = ("fullname", "email")
    ordering = ("fullname",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    search_fields = ("subject",)
    ordering = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("message", "status", "start_time", "end_time")
    list_filter = ("status",)
    search_fields = ("message__subject",)
    ordering = ("-start_time",)
    filter_horizontal = ("subscribers",)


@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ("mailing", "status", "sent_at")
    list_filter = ("status", "sent_at")
    search_fields = ("mailing__message__subject",)
    ordering = ("-sent_at",)
