from django import forms
from django.core.exceptions import ValidationError
from DjangoBaseSetup.messages.messages import ValidationMessages
from .models import AdminModule, AdminModuleAction


class ModuleAddForm(forms.ModelForm):
    parent_id = forms.ModelChoiceField(
        queryset=AdminModule.objects.all(),
        label='Select Parent',
        empty_label='Select Parent',
        required=False,
        initial='',
        widget=forms.Select(attrs={'class': "form-control form-control-solid form-control-lg"}),
    )
    title = forms.CharField(
        required=False,
        label='Title',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Title'}),
        error_messages={
            'required': ValidationMessages.title_field_is_required.value
        }
    )
    path = forms.CharField(
        required=False,
        label='Path',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Path'}),
        error_messages={
            'required': ValidationMessages.path_field_is_required.value
        }
    )
    segment = forms.CharField(
        required=False,
        label='Segment',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Segment'}),
        error_messages={
            'required': ValidationMessages.segment_field_is_required.value
        }
    )
    module_order = forms.CharField(
        required=False,
        label='Order',
        widget=forms.TextInput(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Order'}),
        error_messages={
            'required': ValidationMessages.order_field_is_required.value
        }
    )
    icon = forms.CharField(
        required=False,
        label='Icon',
        widget=forms.Textarea(
            attrs={'class': "form-control form-control-solid form-control-lg", 'placeholder': 'Icon'}),
        error_messages={
            'required': ValidationMessages.icon_field_is_required.value,

        }
    )

    class Meta:
        model = AdminModule
        fields = ['parent_id', 'title', 'path', 'segment', 'module_order', 'icon']

    def clean_parent_id(self):
        data = self.cleaned_data
        parent_id = data.get('parent_id')
        return parent_id

    def clean_title(self):
        data = self.cleaned_data
        title = data.get('title')
        if title == "" or title is None:
            raise ValidationError(self.fields['title'].error_messages['required'])
        return title

    def clean_path(self):
        data = self.cleaned_data
        path = data.get('path')
        if path == "" or path is None:
            raise ValidationError(self.fields['path'].error_messages['required'])
        return path

    def clean_module_order(self):
        data = self.cleaned_data
        module_order = data.get('module_order')
        if module_order == "" or module_order is None:
            raise ValidationError(self.fields['module_order'].error_messages['required'])
        return module_order

    def clean_icon(self):
        data = self.cleaned_data
        icon = data.get('icon')
        if icon == "" or icon is None:
            raise ValidationError(self.fields['icon'].error_messages['required'])
        return icon


class ModuleActionForm(forms.ModelForm):
    class Meta:
        model = AdminModuleAction
        fields = ['admin_module_id', 'name', 'function_name']
