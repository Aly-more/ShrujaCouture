from django import forms


class CheckoutForm(forms.Form):

    customer_name = forms.CharField(
        label="Full Name",
        max_length=150
    )

    email = forms.EmailField()

    phone = forms.CharField(
        max_length=15
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows":4})
    )

    city = forms.CharField(
        max_length=100
    )

    state = forms.CharField(
        max_length=100
    )

    pincode = forms.CharField(
        max_length=10
    )