from urllib.parse import urlencode
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup.messages.messages import EmailTemplateMessages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from apps.languages.models import Languages
from .models import EmailActions, EmailTemplates, EmailTemplatesDescription

try:
    from .form import EmailTemplateFormSet
except:
    pass

MODEL_NAME_SINGULAR = 'Email Template'
MODEL_NAME_PLURAL = 'Email Templates'


@login_required(login_url='login')
def index(request):
    DB = EmailTemplates.objects.all()

    if request.GET.get('name'):
        name = request.GET.get('name').strip()
        DB = DB.filter(name__icontains=name)

    if request.GET.get('subject'):
        subject = request.GET.get('subject').strip()
        DB = DB.filter(subject__icontains=subject)

    orderBy = request.GET.get('order_by', "created_at")
    direction = request.GET.get('direction', "DESC")
    if direction == "DESC":
        DB = DB.order_by("-" + orderBy).all()
    else:
        DB = DB.order_by(orderBy).all()

    # Create main service instance with request
    service = MainService(request)
    totalRecord = DB.count()
    # get page record data from service
    # Get page size value
    recordPerPage = service.getPageRecordSize()

    page = request.GET.get('page', 1)
    paginator = Paginator(DB, recordPerPage)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    pageStart = results.start_index()
    pageEnd = results.end_index()

    # Get page range
    pageRange = service.getPageRange(results, paginator)

    searchingVariables = request.GET
    queryString = searchingVariables.copy()
    if 'page' in queryString:
        queryString.pop("page")
    if 'direction' in queryString:
        queryString.pop("direction")
    if 'order_by' in queryString:
        queryString.pop("order_by")
    queryString = urlencode(queryString)

    context = {
        'results': results,
        'page_start': pageStart,
        'page_end': pageEnd,
        'total_record': totalRecord,
        'page_size': recordPerPage,
        'page': page,
        'page_range': pageRange,
        'order_by': orderBy,
        'direction': direction,
        'searching_variables': searchingVariables,
        'query_string': queryString,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL
    }
    return render(request, "email_templates/index.html", context)


@login_required(login_url='login')
def add(request):
    emailActions = EmailActions.objects.all()
    languages = Languages.objects.filter(is_active=1)
    if request.method == "POST":
        formSet = EmailTemplateFormSet(request.POST, prefix="addEmailTemp")
        if formSet.is_valid():
            formData = formSet.cleaned_data
            emailTemplates = EmailTemplates()
            emailTemplates.name = formData[0].get('name')
            emailTemplates.subject = formData[0].get("subject")
            emailTemplates.action = formData[0].get("action")
            emailTemplates.body = formData[0].get("body")
            emailTemplates.save()

            for i in range(len(languages)):
                if formData[i]:
                    obj = EmailTemplatesDescription()
                    obj.email_template = emailTemplates
                    obj.language_code = languages[i].lang_code
                    obj.page_title = formData[i].get("name")
                    obj.description = formData[i].get("body")
                    obj.save()

            messages.success(request, EmailTemplateMessages.email_template_has_been_added_successfully.value)
            return redirect('Email Templates.index')
    else:
        formSet = EmailTemplateFormSet(prefix="addEmailTemp")
    context = {
        "formSet": formSet,
        "emailActions": emailActions,
        "languages": languages,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL
    }
    return render(request, "email_templates/add.html", context)


@login_required(login_url='login')
def edit(request, id):
    languages = Languages.objects.filter(is_active=1)
    emailDetail = EmailTemplates.objects.get(id=id)
    emailActions = EmailActions.objects.all()

    if not emailDetail:
        return redirect('email_templates.index')

    if request.method == "POST":
        formSet = EmailTemplateFormSet(request.POST, prefix='editEmailTemp')
        if formSet.is_valid():
            formData = formSet.cleaned_data
            emailTempObj = EmailTemplates.objects.get(id=id)
            emailTempObj.name = formData[0].get('name')
            emailTempObj.subject = formData[0].get('subject')
            emailTempObj.action = formData[0].get('action')
            emailTempObj.body = formData[0].get('body')
            emailTempObj.save()
            for i in range(len(languages)):
                if formData[i]:
                    obj = EmailTemplatesDescription.objects.filter(email_template__id=id)[i]
                    obj.email_template = emailDetail
                    obj.language_code = languages[i].lang_code
                    obj.page_title = formData[i].get("name")
                    obj.description = formData[i].get("body")
                    obj.save()
            messages.success(request, EmailTemplateMessages.email_template_has_been_updated_successfully.value)
            return redirect('email_templates.index')
    else:
        emailTemplate = EmailTemplatesDescription.objects.filter(email_template__id=id)
        templates = []
        if emailTemplate:
            for i in range(len(languages)):
                newArr = {}
                try:
                    data = emailTemplate[i]

                    if data:
                        newArr['name'] = data.page_title
                        newArr['subject'] = emailDetail.subject
                        newArr['action'] = int(emailDetail.action)
                        newArr['body'] = data.description
                        templates.append(newArr)
                except:
                    newArr['name'] = ''
                    newArr['subject'] = ''
                    newArr['action'] = ''
                    newArr['body'] = ''
                    templates.append(newArr)
        formSet = EmailTemplateFormSet(initial=templates, prefix='editEmailTemp')
    context = {
        "formSet": formSet,
        "emailDetail": emailDetail,
        "emailActions": emailActions,
        "languages": languages,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL
    }
    return render(request, "email_templates/edit.html", context)


@login_required(login_url='login')
def getConstant(request):
    data = {}
    action = request.GET.get('action', None)
    if action:
        constants = EmailActions.objects.filter(id=action).values("option").first()
        if constants:
            constantsList = constants['option'].split(",")
        else:
            constantsList = ''
        data['success1'] = 1
        data['options'] = constantsList
    else:
        data['error'] = 0
    return JsonResponse(data)
