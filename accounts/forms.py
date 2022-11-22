from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'gender',
                  'phone_number', 'email', 'password']


    # Overriding the form styling behavior
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {'type': 'text', 'class': 'form-control form-control-light', 'placeholder': 'Your first name', 'id': 'reg-fn'})
        self.fields["last_name"].widget.attrs.update(
            {'type': 'text', 'class': 'form-control form-control-light', 'placeholder': 'Your last name', 'id': 'reg-ln'})
        self.fields["gender"].widget.attrs.update(
            {'type': 'select', 'class': 'form-select form-select-light', 'placeholder': 'Your gender'})
        self.fields["phone_number"].widget.attrs.update(
            {'type': 'text', 'class': 'form-control form-control-light', 'placeholder': 'Your phone number', 'id': 'reg-phone'})
        self.fields["email"].widget.attrs.update(
            {'type': 'email', 'class': 'form-control form-control-light', 'placeholder': 'Your email address', 'id': 'reg-email'})
        self.fields["password"].widget.attrs.update(
            {'type': 'password', 'class': 'form-control form-control-light', 'placeholder': 'Your password', 'id': 'reg-password'})
        self.fields["confirm_password"].widget.attrs.update(
            {'type': 'password', 'class': 'form-control form-control-light', 'placeholder': 'Confirm your password', 'id': 'reg-password-confirm'})


    # Checking if Password matches Confirm Password
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match each others."
            )
