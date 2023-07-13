from DjangoBaseSetup.common_modules.mainService import MainService
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from DjangoBaseSetup.messages.messages import FaqMessages
from apps.languages.models import Languages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import urlencode
from apps.faq.models import Faq, FaqDescriptions

try:
    from apps.faq.forms import FaqLangFormSet
except:
    pass

# Create your views here.
MODEL_NAME_SINGULAR = 'FAQ'
MODEL_NAME_PLURAL = 'FAQ'


@login_required(login_url='login')
def index(request):
    DB = Faq.objects.all()

    if request.GET.get('question'):
        question = request.GET.get('question').strip()
        DB = DB.filter(question__icontains=question)

    if request.GET.get('answer'):
        answer = request.GET.get('answer').strip()
        DB = DB.filter(answer__icontains=answer)

    if request.GET.get('is_active'):
        DB = DB.filter(is_active=request.GET.get('is_active'))

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
        'page_range': pageRange,
        "total_record": totalRecord,
        'page': page,
        'order_by': orderBy,
        'direction': direction,
        'searching_variables': searchingVariables,
        'query_string': queryString,
        'page_size': recordPerPage,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "faq/index.html", context)


@login_required(login_url='login')
def add(request):
    languages = Languages.objects.filter(is_active=1)
    if request.method == "POST":
        formSet = FaqLangFormSet(request.POST, prefix='faq')
        if formSet.is_valid():
            formSetData = formSet.cleaned_data
            faqObj = Faq()
            faqObj.question = formSetData[0].get("question")
            faqObj.answer = formSetData[0].get("answer")
            faqObj.save()
            for i in range(len(languages)):
                if formSetData[i]:
                    faqLangObj = FaqDescriptions()
                    faqLangObj.faq = faqObj
                    faqLangObj.language_code = languages[i].lang_code
                    faqLangObj.question = formSetData[i].get("question")
                    faqLangObj.answer = formSetData[i].get("answer")
                    faqLangObj.save()
            messages.success(request, FaqMessages.faq_page_has_been_added_successfully.value)
            return redirect('faqs.index')
    else:
        formSet = FaqLangFormSet(prefix='faq')
    context = {
        "form_set": formSet,
        "languages": languages,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "faq/add.html", context)


@login_required(login_url='login')
def edit(request, id):
    faqObj = Faq.objects.get(id=id)
    languages = Languages.objects.filter(is_active=1).all()
    if not faqObj:
        return redirect('dashboard.index')
    if request.method == "POST":
        formSet = FaqLangFormSet(request.POST, prefix='faqEdit')
        if formSet.is_valid():
            formSetData = formSet.cleaned_data
            # Update CmsApi page data
            faqObj = Faq.objects.get(id=id)
            faqObj.question = formSetData[0].get("question")
            faqObj.answer = formSetData[0].get("answer")
            faqObj.save()
            for i in range(len(languages)):
                if formSetData[i]:
                    faqLangObj = FaqDescriptions.objects.filter(faq__id=id)[i]
                    faqLangObj.faq = faqObj
                    faqLangObj.language_code = languages[i].lang_code
                    faqLangObj.question = formSetData[i].get("question")
                    faqLangObj.answer = formSetData[i].get("answer")
                    faqLangObj.save()
            messages.success(request, FaqMessages.faq_page_has_been_updated_successfully.value)
            return redirect('faqs.index')
    else:
        FaqDescriptionDetails = FaqDescriptions.objects.filter(faq__id=id)
        faqLanguageDetails = []
        if FaqDescriptionDetails:
            for i in range(len(languages)):
                newArr = {}
                try:
                    data = FaqDescriptionDetails[i]
                    if data:
                        newArr['question'] = data.question
                        newArr['answer'] = data.answer
                        faqLanguageDetails.append(newArr)
                except:
                    newArr['question'] = ''
                    newArr['answer'] = ''
                    faqLanguageDetails.append(newArr)
        formSet = FaqLangFormSet(initial=faqLanguageDetails, prefix='faqEdit')
    context = {
        'form_set': formSet,
        "languages": languages,
        "faq_detail": faqObj,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "faq/edit.html", context)


@login_required(login_url='login')
def status(request, id):
    faq = Faq.objects.filter(id=id).first()
    if faq is None:
        return redirect('dashboard.index')
    if faq.is_active:
        faq.is_active = False
        messages.success(request, FaqMessages.faq_deactivated.value)
    else:
        faq.is_active = True
        messages.success(request, FaqMessages.faq_activated.value)
    faq.save()
    return redirect('faqs.index')


@login_required(login_url='login')
def delete(request, id):
    Faq.objects.filter(id=id).delete()
    messages.success(request, FaqMessages.faq_deleted.value)
    return redirect('faqs.index')
