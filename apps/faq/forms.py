from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet
from DjangoBaseSetup.messages.messages import ValidationMessages
from django.forms import formset_factory
from apps.languages.models import Languages
from .models import Faq


# Cms page Form
class FaqForm(forms.ModelForm):
    question = forms.CharField(
        required=False,
        label='Question',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.question_field_is_required.value
        }
    )
    answer = forms.CharField(
        required=False,
        label='Answer',
        initial='',
        widget=forms.TextInput(attrs={'class': "form-control form-control-solid form-control-lg"}),
        error_messages={
            'required': ValidationMessages.answer_field_is_required.value
        }
    )

    class Meta:
        model = Faq
        fields = ['question', 'answer']

    def clean_question(self):
        data = self.cleaned_data
        question = data.get('question')
        if question == "" or question is None:
            raise ValidationError(self.fields['question'].error_messages['required'])
        return question

    def clean_answer(self):
        data = self.cleaned_data
        answer = data.get('answer')
        if answer == "" or answer is None:
            raise ValidationError(self.fields['answer'].error_messages['required'])
        return answer


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        length = len(self.forms)
        for i in range(length):
            if i == 0:
                self.forms[i].empty_permitted = False
            else:
                self.forms[i].empty_permitted = True


# faq page formset
try:
    FaqLangFormSet = formset_factory(
        FaqForm,
        formset=RequiredFormSet,
        extra=Languages.objects.filter(is_active=True).count()
    )
except:
    pass
