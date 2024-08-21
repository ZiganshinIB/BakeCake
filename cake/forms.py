from django import forms


class PhoneForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'contacts__form_iunput',
            'placeholder': '+7(999)999--99-99',
            'required': 'required'
        })
    )
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'contacts__form_iunput',
            'placeholder': 'Имя',
            'required': 'required'
        })
    )


class PinForm(forms.Form):
    pin = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'tipsPopup__form_inputNum popup__input',
            'placeholder': '9999',
            'required': 'required',
            'style': 'width: 200px; height: 50px;'
        })
    )