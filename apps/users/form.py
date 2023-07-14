from django import forms
from django.core.exceptions import ValidationError
from DjangoBaseSetup.messages.messages import ValidationMessages
from .models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(
        required=False,
        label='User Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'User name'}),
        error_messages={
            'required': ValidationMessages.username_field_is_required.value
        }
    )
    first_name = forms.CharField(
        required=False,
        label='Fist Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'First name'}),
        error_messages={
            'required': ValidationMessages.first_name_field_is_required.value
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Last name'}),
        error_messages={
            'required': ValidationMessages.last_name_field_is_required.value
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.email_field_is_required.value,
            'invalid': ValidationMessages.email_is_not_valid.value
        }
    )
    mobile_number = forms.CharField(
        required=False,
        label='Phone Number',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Phone number'}),
        error_messages={
            'required': ValidationMessages.mobile_field_is_required.value,
            'exists': ValidationMessages.mobile_number_exist.value,
            'minimum': ValidationMessages.mobile_number_minimum.value,
            'maximum': ValidationMessages.mobile_number_maximum.value,
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number']

    def clean_username(self):
        data = self.cleaned_data
        username = data.get('username')
        if username == "" or username is None:
            raise ValidationError(self.fields['username'].error_messages['required'])
        return username

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

    def clean_mobile_number(self):
        data = self.cleaned_data
        mobile_number = data.get('mobile_number')
        user_mobile_number = User.objects.filter(mobile_number=mobile_number).exists()
        if mobile_number == "" or mobile_number is None:
            raise ValidationError(self.fields['mobile_number'].error_messages['required'])
        elif len(mobile_number) < 10:
            raise ValidationError(self.fields['mobile_number'].error_messages['minimum'])
        elif len(mobile_number) > 12:
            raise ValidationError(self.fields['mobile_number'].error_messages['maximum'])
        elif user_mobile_number:
            raise ValidationError(self.fields['mobile_number'].error_messages['exists'])
        return mobile_number


class UserAddForm(forms.Form):
    username = forms.CharField(
        required=False,
        label='User Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'User name'}),
        error_messages={
            'required': ValidationMessages.username_field_is_required.value
        }
    )
    first_name = forms.CharField(
        required=False,
        label='First Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'First name'}),
        error_messages={
            'required': ValidationMessages.first_name_field_is_required.value
        }
    )
    last_name = forms.CharField(
        required=False,
        label='Last Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Last name'}),
        error_messages={
            'required': ValidationMessages.last_name_field_is_required.value
        }
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Email'}),
        error_messages={
            'required': ValidationMessages.email_field_is_required.value,
            'invalid': ValidationMessages.email_is_not_valid.value,
            'exists': ValidationMessages.email_is_already_exists.value
        }
    )
    mobile_number = forms.CharField(
        required=False,
        label='Phone Number',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Phone number'}),
        error_messages={
            'required': ValidationMessages.mobile_field_is_required.value,
            'exists': ValidationMessages.mobile_number_exist.value,
            'minimum': ValidationMessages.mobile_number_minimum.value,
            'maximum': ValidationMessages.mobile_number_maximum.value,
        }
    )
    password = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Password'}),
        error_messages={
            'required': ValidationMessages.password_field_is_required.value,
            'min_value': ValidationMessages.password_should_contains_atleast_8_digits.value,
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Confirm password'}),
        error_messages={
            'required': ValidationMessages.confirm_password_field_is_required.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
            'validators': ValidationMessages.confirm_password_and_new_password_must_match.value
        }
    )

    def clean_username(self):
        data = self.cleaned_data
        username = data.get('username')
        if username == "" or username is None:
            raise ValidationError(self.fields['username'].error_messages['required'])
        return username

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
        user_email = User.objects.filter(email=email).exists()
        if email == "" or email is None:
            raise ValidationError(self.fields['email'].error_messages['required'])
        elif user_email:
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return email

    def clean_mobile_number(self):
        data = self.cleaned_data
        mobile_number = data.get('mobile_number')
        user_mobile_number = User.objects.filter(mobile_number=mobile_number).exists()
        if mobile_number == "" or mobile_number is None:
            raise ValidationError(self.fields['mobile_number'].error_messages['required'])
        elif len(mobile_number) < 10:
            raise ValidationError(self.fields['mobile_number'].error_messages['minimum'])
        elif len(mobile_number) > 12:
            raise ValidationError(self.fields['mobile_number'].error_messages['maximum'])
        elif user_mobile_number:
            raise ValidationError(self.fields['mobile_number'].error_messages['exists'])
        return mobile_number

    def clean_password(self):
        data = self.cleaned_data
        password = data.get('password')
        if password == "" or password is None:
            raise ValidationError(self.fields['password'].error_messages['required'])
        elif 8 > len(password) > 0:
            raise ValidationError(self.fields['password'].error_messages['min_value'])
        return password

    def clean_confirm_password(self):
        data = self.cleaned_data
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif confirm_password != data.get('password'):
            raise ValidationError(self.fields['confirm_password'].error_messages['validators'])
        return confirm_password


class UserPasswordChangeForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Password'}),
        error_messages={
            'required': ValidationMessages.password_field_is_required.value,
            'min_value': ValidationMessages.password_should_contains_atleast_8_digits.value,
        }
    )
    confirm_password = forms.CharField(
        required=False,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Confirm password'}),
        error_messages={
            'required': ValidationMessages.confirm_password_field_is_required.value,
            'min_value': ValidationMessages.confirm_password_should_contains_at_least_8_digits.value,
            'validators': ValidationMessages.confirm_password_and_new_password_must_match.value
        }
    )

    class Meta:
        model = User
        fields = ['password', 'confirm_password']

    def clean_password(self):
        data = self.cleaned_data
        password = data.get('password')
        if password == "" or password is None:
            raise ValidationError(self.fields['password'].error_messages['required'])
        elif 8 > len(password) > 0:
            raise ValidationError(self.fields['password'].error_messages['min_value'])
        return password

    def clean_confirm_password(self):
        data = self.cleaned_data
        confirm_password = data.get('confirm_password')
        if confirm_password == "" or confirm_password is None:
            raise ValidationError(self.fields['confirm_password'].error_messages['required'])
        elif 8 > len(confirm_password) > 0:
            raise ValidationError(self.fields['confirm_password'].error_messages['min_value'])
        elif confirm_password != data.get('password'):
            raise ValidationError(self.fields['confirm_password'].error_messages['validators'])
        return confirm_password
