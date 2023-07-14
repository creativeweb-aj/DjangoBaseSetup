from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet, formset_factory
from DjangoBaseSetup.messages.messages import ValidationMessages
from .models import EmailTemplates
from apps.languages.models import Languages


class EmailTemplateForm(forms.Form):
    name = forms.CharField(
        required=False,
        label='Name',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Name'}
        ),
        error_messages={
            'required': ValidationMessages.name_field_is_required.value
        }
    )
    subject = forms.CharField(
        required=False,
        label='Subject',
        initial='',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Name'}
        ),
        error_messages={
            'required': ValidationMessages.subject_field_is_required.value
        }
    )
    action = forms.CharField(
        required=False,
        label='Action',
        initial='',
        widget=forms.Select(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Name'}
        ),
        error_messages={
            'required': ValidationMessages.action_field_is_required.value
        }
    )
    body = forms.CharField(
        required=False,
        label='Email Body',
        initial='',
        widget=forms.Textarea(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Name'}
        ),
        error_messages={
            'required': ValidationMessages.email_body_field_is_required.value
        }
    )

    class Meta:
        model = EmailTemplates
        fields = ['name', 'subject', 'action', 'body']

    def clean_name(self):
        data = self.cleaned_data
        name = data.get('name')
        if name == "" or name is None:
            raise ValidationError(self.fields['name'].error_messages['required'])
        return name

    def clean_subject(self):
        data = self.cleaned_data
        subject = data.get('subject')
        if subject == "" or subject is None:
            raise ValidationError(self.fields['subject'].error_messages['required'])
        return subject

    def clean_action(self):
        data = self.cleaned_data
        action = data.get('action')
        if action == "" or action is None:
            raise ValidationError(self.fields['action'].error_messages['required'])
        return action

    def clean_body(self):
        data = self.cleaned_data
        body = data.get('body')
        if body == "" or body is None:
            raise ValidationError(self.fields['body'].error_messages['required'])
        return body


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        length = len(self.forms)
        for i in range(length):
            if i == 0:
                self.forms[i].empty_permitted = False
            else:
                self.forms[i].empty_permitted = True


# Formset for email template
try:
    EmailTemplateFormSet = formset_factory(
        EmailTemplateForm,
        formset=RequiredFormSet,
        extra=Languages.objects.filter(is_active=1).count()
    )
except:
    pass