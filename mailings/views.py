from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .services import send_email

from .models import Subscriber, Message, Mailing
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

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
	return redirect('mailings:mailing_list')