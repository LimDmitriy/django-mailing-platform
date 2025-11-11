from django.urls import path
from .apps import MailingsConfig
from .views import SubscriberListView, SubscriberCreateView, SubscriberDetailView, SubscriberUpdateView, \
	SubscriberDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView

app_name = MailingsConfig.name

urlpatterns = [
	path("", SubscriberListView.as_view(), name="subscriber_list"),
	path("subscribers/create/", SubscriberCreateView.as_view(), name="subscriber_create"),
	path("subscribers/<int:pk>/detail/", SubscriberDetailView.as_view(), name="subscriber_detail"),
	path("subscribers/<int:pk>/update/", SubscriberUpdateView.as_view(), name="subscriber_update"),
	path("subscribers/<int:pk>/delete/", SubscriberDeleteView.as_view(), name="subscriber_delete"),
	path("message/list/", MessageListView.as_view(), name="message_list"),
	path("message/create/", MessageCreateView.as_view(), name="message_create"),
	path("message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"),
	path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
	path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
]

