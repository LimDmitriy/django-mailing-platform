from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .services import send_email
from django.contrib.auth.decorators import login_required

from .models import Subscriber, Message, Mailing
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


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


class SubscriberListView(ListView):
    model = Subscriber
    template_name = "mailings/subscribers_list.html"
    context_object_name = "subscribers"


class SubscriberCreateView(CreateView):
    model = Subscriber
    fields = ("email", "fullname", "comment")
    template_name = "mailings/subscriber_form.html"
    success_url = reverse_lazy("mailings:subscriber_list")


class SubscriberDetailView(DetailView):
    model = Subscriber
    template_name = "mailings/subscriber_detail.html"
    context_object_name = "subscriber"


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    fields = ("email", "fullname", "comment")
    template_name = "mailings/subscriber_form.html"
    success_url = reverse_lazy("mailings:subscriber_list")


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = "mailings/subscriber_confirm_delete.html"
    success_url = reverse_lazy("mailings:subscriber_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"


class MessageCreateView(CreateView):
    model = Message
    template_name = "mailings/message_form.html"
    fields = ("subject", "content")
    success_url = reverse_lazy("mailings:message_list")


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailings/message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    fields = ("subject", "content")
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    model = Mailing
    fields = ("start_time", "end_time", "message", "subscribers")
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ("start_time", "end_time", "message", "subscribers")
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


def send_mail_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    send_email(mailing)
    messages.success(request, "Рассылка отправлена")
    return redirect("mailings:mailing_list")


@login_required
def user_mailings_stats(request):

    messages = Message.objects.filter(user=request.user)
    mailings = Mailing.objects.filter(message__in=messages)

    stats = []
    for mailing in mailings:
        success_count = mailing.delivery_statuses.filter(status="success").count()
        failed_count = mailing.delivery_statuses.filter(status="failed").count()
        stats.append(
            {
                "mailing": mailing,
                "success": success_count,
                "failed": failed_count,
                "total": success_count + failed_count,
            }
        )

    return render(request, "mailings/user_mailings_stats.html", {"stats": stats})
