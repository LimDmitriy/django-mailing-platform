from django.utils import timezone
from django.db import models
from django.db.models import CASCADE
from django.conf import settings


class Subscriber(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )
    email = models.EmailField(verbose_name="Почта", unique=True)
    fullname = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = [
            "fullname",
        ]

    def __str__(self):
        return f"{self.fullname} - {self.email}"


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Пользователь",
    )

    subject = models.CharField(max_length=250, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Письмо")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "subject",
        ]

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("running", "Запущена"),
        ("finished", "Завершена"),
    ]
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings"
    )
    start_time = models.DateTimeField(verbose_name="Дата начала рассылки")
    end_time = models.DateTimeField(
        verbose_name="Дата окончания рассылки", blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус рассылки",
        default="created",
    )
    message = models.ForeignKey(
        "Message",
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="mailings",
    )
    subscribers = models.ManyToManyField(
        "Subscriber", verbose_name="Получатели", related_name="mailings"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = [
            "status",
        ]
        permissions = [
            ("can_view_statistics", "Can view statistics")
        ]

    def __str__(self):
        return f"{self.message.subject} - ({self.status})"

    def update_status(self):
        if not self.pk:
            return

        now = timezone.now()
        if self.end_time and now >= self.end_time:
            self.status = "finished"
            return

        if self.delivery_statuses.exists():
            self.status = "running"
            return

        self.status = "created"

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    def total_attempts(self):
        return self.delivery_statuses.count()

    def succsesful_attempts(self):
        return self.delivery_statuses.filter(status="success").count()

    def failed_attempts(self):
        return self.delivery_statuses.filter(status="failed").count()


class DeliveryStatus(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата попытки")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )
    server_response = models.TextField(
        verbose_name="Ответ сервера", blank=True, null=True
    )
    mailing = models.ForeignKey(
        "Mailing",
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name="delivery_statuses",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = [
            "-sent_at",
        ]

    def __str__(self):
        return f"{self.mailing}"
