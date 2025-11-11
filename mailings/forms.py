from django import forms

from mailings.models import Subscriber, Message


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "fullname", "comment"]

    def __init__(self, *args, **kwargs):
        super(SubscriberForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название email"}
        )
        self.fields["fullname"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите Ф.И.О."}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите комментарий"}
        )


class MessageForm(forms.ModelForm):
    model = Message
    fields = ["subject", "content"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тему письма"}
        )
        self.fields["content"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите сообщение"}
        )