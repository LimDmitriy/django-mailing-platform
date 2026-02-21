from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .services import send_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Subscriber, Message, Mailing
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


@method_decorator(cache_page(60 * 5), name="dispatch")
class HomeView(ListView):
    model = Mailing
    template_name = "mailings/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="running").count()
        context["unique_subscribers"] = (
            Subscriber.objects.filter(mailings__isnull=False).distinct().count()
        )
        return context


@method_decorator(cache_page(60 * 5), name="dispatch")
class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = "mailings/subscribers_list.html"
    context_object_name = "subscribers"

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Subscriber.objects.all()
        return Subscriber.objects.filter(owner=self.request.user)


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    fields = ("email", "fullname", "comment")
    template_name = "mailings/subscriber_form.html"
    success_url = reverse_lazy("mailings:subscriber_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SubscriberDetailView(LoginRequiredMixin, DetailView):
    model = Subscriber
    template_name = "mailings/subscriber_detail.html"
    context_object_name = "subscriber"


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    fields = ("email", "fullname", "comment")
    template_name = "mailings/subscriber_form.html"
    success_url = reverse_lazy("mailings:subscriber_list")


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    template_name = "mailings/subscriber_confirm_delete.html"
    success_url = reverse_lazy("mailings:subscriber_list")


@method_decorator(cache_page(60 * 5), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "mailings/message_form.html"
    fields = ("subject", "content")
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="manager").exists():
            return qs
        return qs.filter(user=self.request.user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("subject", "content")
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="manager").exists():
            return qs
        return qs.filter(user=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ("start_time", "end_time", "message", "subscribers")
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ("start_time", "end_time", "message", "subscribers")
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        if self.request.user.groups.filter(name="manager").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingStatsView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/user_mailings_stats.html"
    context_object_name = "mailings"

    def get_queryset(self):
        messages = Message.objects.filter(user=self.request.user)
        return Mailing.objects.filter(message__in=messages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats_list = []
        for mailing in context["mailings"]:
            stats_list.append(
                {
                    "mailing": mailing,
                    "success": mailing.delivery_statuses.filter(
                        status="success"
                    ).count(),
                    "failed": mailing.delivery_statuses.filter(status="failed").count(),
                }
            )

        context["stats"] = stats_list
        return context


def send_mail_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_email(mailing)
    messages.success(request, "Рассылка отправлена")
    return redirect("mailings:mailing_list")
