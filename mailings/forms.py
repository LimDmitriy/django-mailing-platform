from django import forms

from mailings.models import Subscriber, Message, Mailing


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


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["start_time", "end_time", "message", "subscribers"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["start_time"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите дату начал рассылки "}
        )
        self.fields["end_time"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите дату окончания рассылки"}
        )
        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["subscribers"].widget.attrs.update({"class": "form-control"})

