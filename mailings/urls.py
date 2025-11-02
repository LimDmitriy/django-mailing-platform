from django.urls import path
from .apps import MailingsConfig
from .views import SubscriberListView, SubscriberCreateView, SubscriberDetailView, SubscriberUpdateView, \
	SubscriberDeleteView

app_name = MailingsConfig.name

urlpatterns = [
	path("", SubscriberListView.as_view(), name="subscriber_list"),
	path("subscribers/create/", SubscriberCreateView.as_view(), name="subscriber_create"),
	path("subscribers/<int:pk>/", SubscriberDetailView.as_view(), name="subscriber_detail"),
	path("subscribers/<int:pk>/update/", SubscriberUpdateView.as_view(), name="subscriber_update"),
	path("subscribers/<int:pk>/delete/", SubscriberDeleteView.as_view(), name="subscriber_delete"),
]

