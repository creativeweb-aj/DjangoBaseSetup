from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from DjangoBaseSetup.messages.messages import ValidationMessages
from apps.users.models import User
from django import forms
import re


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Your Email',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0 ",
                   'placeholder': 'Email'}),
        error_messages={
            'required': ValidationMessages.email_field_is_required.value
        }
    )
    password = forms.CharField(
        required=False,
        label='Your Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0 ",
                   'placeholder': 'Password'}),
        error_messages={
            'required': ValidationMessages.password_field_is_required.value
        }
    )

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email

    def clean_password(self):
        data = self.cleaned_data
        password = data.get('password')
        if password == "" or password is None:
            raise ValidationError(self.fields['password'].error_messages['required'])
        return password


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        label='First Name',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.first_name_field_is_required.value
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.last_name_field_is_required.value
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.email_field_is_required.value,
            'invalid': ValidationMessages.email_is_not_valid.value
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_first_name(self):
        data = self.cleaned_data
        first_name = data.get('first_name')
        if first_name == "" or first_name is None:
            raise ValidationError(self.fields['first_name'].error_messages['required'])
        return first_name

    def clean_last_name(self):
        data = self.cleaned_data
        last_name = data.get('last_name')
        if last_name == "" or last_name is None:
            raise ValidationError(self.fields['last_name'].error_messages['required'])
        return last_name

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        return email


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(
        required=False,
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': "Old password"}),
        error_messages={
            'required': ValidationMessages.old_password_is_required.value,
            'error_messages': ValidationMessages.old_password_is_not_correct.value,
        }
    )
    new_password = forms.CharField(
        required=False,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': "New password"}),
        error_messages={
            'required': ValidationMessages.new_password_field_is_required.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': "Confirm password"}),
        error_messages={
            'required': ValidationMessages.confirm_password_field_is_required.value,
            'error_messages': ValidationMessages.confirm_password_and_new_password_must_match.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
        }
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']

    def clean_old_password(self):
        data = self.cleaned_data
        password = self.instance.password
        old_password = data.get('old_password')
        if old_password == "" or old_password is None:
            raise ValidationError(self.fields['old_password'].error_messages['required'])
        elif old_password is not None or not old_password:
            isChecked = check_password(old_password, password)
            if not isChecked:
                raise ValidationError(self.fields['old_password'].error_messages['error_messages'])
        return old_password

    def clean_new_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        if new_password == "" or new_password is None:
            raise ValidationError(self.fields['new_password'].error_messages['required'])
        elif 8 > len(new_password) > 0:
            raise ValidationError(self.fields['new_password'].error_messages['min_value'])
        return new_password

    def clean_confirm_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif new_password != confirm_password:
            raise ValidationError(self.fields['confirm_password'].error_messages['error_messages'])
        return confirm_password


# Forgot Password Form
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0",
                   'placeholder': "Email"}),
        error_messages={
            'required': ValidationMessages.email_field_is_required.value,
            'invalid': ValidationMessages.email_is_not_valid.value,
            'exists': ValidationMessages.email_is_not_exists.value
        }
    )

    # Clean method for email validations
    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email')
        user_email = User.objects.filter(email=email).exists()
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        elif not user_email:
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return email


# Password Rest Form
class PasswordRestForm(forms.Form):
    new_password = forms.CharField(
        required=False,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0 ",
                   'placeholder': "New password"}),
        error_messages={
            'required': ValidationMessages.new_password_field_is_required.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0",
                   'placeholder': "Confirm password"}),
        error_messages={
            'required': ValidationMessages.confirm_password_field_is_required.value,
            'error_messages': ValidationMessages.confirm_password_and_new_password_must_match.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
        }
    )

    def clean_new_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        if new_password == "" or new_password is None:
            raise ValidationError(self.fields['new_password'].error_messages['required'])
        elif 8 > len(new_password) > 0:
            raise ValidationError(self.fields['new_password'].error_messages['min_value'])
        return new_password

    def clean_confirm_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif new_password != confirm_password:
            raise ValidationError(self.fields['confirm_password'].error_messages['error_messages'])
        return confirm_password


class PasswordRestOtpForm(forms.Form):
    otp = forms.CharField(
        required=False,
        label='OTP',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0 ",
                   'placeholder': "OTP"}),
        error_messages={
            'required': ValidationMessages.OTP_field_is_required.value,
        }
    )

    new_password = forms.CharField(
        required=False,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0 ",
                   'placeholder': "New password"}),
        error_messages={
            'required': ValidationMessages.new_password_field_is_required.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
            'passwordData': ValidationMessages.password_must_contain_upperchar_lowerchar_specchar_numbers.value
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid h-auto py-5 px-6 rounded-lg border-0",
                   'placeholder': "Confirm password"}),
        error_messages={
            'required': ValidationMessages.confirm_password_field_is_required.value,
            'error_messages': ValidationMessages.confirm_password_and_new_password_must_match.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
            'passwordData': ValidationMessages.password_must_contain_upperchar_lowerchar_specchar_numbers.value
        }
    )

    def clean_otp(self):
        data = self.cleaned_data
        otp = data.get('otp')
        if otp == "" or otp is None:
            raise ValidationError(self.fields['otp'].error_messages['required'])
        return otp

    def clean_new_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        if new_password == "" or new_password is None:
            raise ValidationError(self.fields['new_password'].error_messages['required'])
        elif 8 > len(new_password) > 0:
            raise ValidationError(self.fields['new_password'].error_messages['min_value'])
        elif not re.match('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', new_password):
            raise ValidationError(self.fields['new_password'].error_messages['passwordData'])
        return new_password

    def clean_confirm_password(self):
        data = self.cleaned_data
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif new_password != confirm_password:
            raise ValidationError(self.fields['confirm_password'].error_messages['error_messages'])
        elif not re.match('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', confirm_password):
            raise ValidationError(self.fields['confirm_password'].error_messages['passwordData'])
        return confirm_password
