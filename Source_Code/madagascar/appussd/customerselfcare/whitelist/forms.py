from django import forms


class FormWhitelist(forms.Form):
    ACTIONS_CHOICES = (
        (1, "Customer Whitelist"),
        (2, "Dealer Whitelist"),
    )

    actions = forms.ChoiceField(choices=ACTIONS_CHOICES)
