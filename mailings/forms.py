from django import forms

from mailings.models import Subscriber


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
