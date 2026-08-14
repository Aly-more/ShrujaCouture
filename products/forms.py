from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:

        model = ContactMessage

        fields = [
            "full_name",
            "email",
            "subject",
            "message",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Your full name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com"
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "How can we help?"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": "Write your message here...",
                    "rows": 6,
                }
            ),

        }