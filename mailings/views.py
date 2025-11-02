from django.urls import reverse_lazy

from .models import Subscriber
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

