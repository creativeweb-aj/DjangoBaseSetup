from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet
from DjangoBaseSetup.messages.messages import ValidationMessages
from django.forms import formset_factory
from apps.languages.models import Languages


# Cms page Form
class CmsLangForm(forms.Form):
    page_title = forms.CharField(
        required=False,
        label='Page Title',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.page_title_field_is_required.value
        }
    )
    description = forms.CharField(
        required=False,
        label='Description',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.description_field_is_required.value
        }
    )

    def clean_page_title(self):
        data = self.cleaned_data
        page_title = data.get('page_title')
        if page_title == "" or page_title is None:
            raise ValidationError(self.fields['page_title'].error_messages['required'])
        return page_title

    def clean_description(self):
        data = self.cleaned_data
        description = data.get('description')
        if description == "" or description is None:
            raise ValidationError(self.fields['description'].error_messages['required'])
        return description


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        length = len(self.forms)
        for i in range(length):
            if i == 0:
                self.forms[i].empty_permitted = False
            else:
                self.forms[i].empty_permitted = True


# Cms page formset
try:
    CmsLangFormSet = formset_factory(
        CmsLangForm,
        formset=RequiredFormSet,
        extra=Languages.objects.filter(is_active=1).count()
    )
except:
    pass


class CmsForm(forms.Form):
    page_name = forms.CharField(
        required=False,
        label='Page Name',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.page_name_field_is_required.value
        }
    )

    def clean_page_name(self):
        data = self.cleaned_data
        page_name = data.get('page_name')
        if page_name == "" or page_name is None:
            raise ValidationError(self.fields['page_name'].error_messages['required'])
        return page_name
