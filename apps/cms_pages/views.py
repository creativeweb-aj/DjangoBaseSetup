from DjangoBaseSetup.common_modules.mainService import MainService
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.languages.models import Languages
from apps.cms_pages.models import CmsPages, CmsPageDescriptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import urlencode
from DjangoBaseSetup.messages.messages import CmsPageMessages
try:
    from apps.cms_pages.form import CmsForm, CmsLangFormSet
except:
    pass


MODEL_NAME_SINGULAR = 'Cms Page'
MODEL_NAME_PLURAL = 'Cms Pages'


@login_required(login_url='login')
def index(request):
    DB = CmsPages.objects.all()

    if request.GET.get('page_name'):
        pageName = request.GET.get('page_name').strip()
        DB = DB.filter(page_name__icontains=pageName)

    if request.GET.get('page_title'):
        pageTitle = request.GET.get('page_title').strip()
        DB = DB.filter(page_title__icontains=pageTitle)

    orderBy = request.GET.get('order_by', "created_at")
    direction = request.GET.get('direction', "DESC")

    if direction == "DESC":
        DB = DB.order_by("-" + orderBy).all()
    else:
        DB = DB.order_by(orderBy).all()

    # Create main service instance with request
    service = MainService(request)
    totalRecord = DB.count()
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

    return render(request, "cms_pages/index.html", context)


@login_required(login_url='login')
def view(request, id):
    data = CmsPages.objects.get(id=id)
    if not data:
        return redirect('dashboard.index')
    context = {
        "data": data,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, 'cms_pages/view.html', context)


@login_required(login_url='login')
def add(request):
    languages = Languages.objects.filter(is_active=1)
    if request.method == "POST":
        form = CmsForm(request.POST)
        formSet = CmsLangFormSet(request.POST, prefix='CmsApi')
        if form.is_valid() and formSet.is_valid():
            formData = form.cleaned_data
            formSetData = formSet.cleaned_data
            cmsObj = CmsPages()
            cmsObj.page_name = formData.get("page_name")
            cmsObj.page_title = formSetData[0].get("page_title")
            cmsObj.slug = formSetData[0].get("page_title").replace(" ", "-")
            cmsObj.description = formSetData[0].get("description")
            cmsObj.save()
            for i in range(len(languages)):
                if formSetData[i]:
                    cmsLangObj = CmsPageDescriptions()
                    cmsLangObj.cms_page = cmsObj
                    cmsLangObj.language_code = languages[i].lang_code
                    cmsLangObj.page_title = formSetData[i].get("page_title")
                    cmsLangObj.description = formSetData[i].get("description")
                    cmsLangObj.save()
            messages.success(request, CmsPageMessages.cms_page_has_been_added_successfully.value)
            return redirect('cms_pages.index')
    else:
        form = CmsForm()
        formSet = CmsLangFormSet(prefix='CmsApi')
    context = {
        "form": form,
        "formSet": formSet,
        "languages": languages,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "cms_pages/add.html", context)


@login_required(login_url='login')
def edit(request, id):
    CmsPageObj = CmsPages.objects.get(id=id)
    languages = Languages.objects.filter(is_active=1).all()
    if not CmsPageObj:
        return redirect('dashboard.index')
    if request.method == "POST":
        formSet = CmsLangFormSet(request.POST, prefix='cmsEdit')
        if formSet.is_valid():
            formSetData = formSet.cleaned_data
            # Update CmsApi page data
            cmsPage = CmsPages.objects.get(id=id)

            cmsPage.page_title = formSetData[0].get("page_title")

            cmsPage.description = formSetData[0].get("description")
            cmsPage.save()
            for i in range(len(languages)):
                if formSetData[i]:
                    Obj = CmsPageDescriptions.objects.filter(cms_page_id=id)[i]
                    Obj.cms_page = cmsPage
                    Obj.language_code = languages[i].lang_code
                    Obj.page_title = formSetData[i].get("page_title")
                    Obj.description = formSetData[i].get("description")
                    Obj.save()
            messages.success(request, CmsPageMessages.cms_page_has_been_updated_successfully.value)

            return redirect('cms_pages.index')
    else:
        CmsDescriptionDetails = CmsPageDescriptions.objects.filter(cms_page_id=id)
        cmsLanguageDetails = []
        if CmsDescriptionDetails:
            for i in range(len(languages)):
                newArr = {}
                try:
                    data = CmsDescriptionDetails[i]
                    if data:
                        newArr['page_title'] = data.page_title
                        newArr['description'] = data.description
                        cmsLanguageDetails.append(newArr)
                except:
                    newArr['page_title'] = ''
                    newArr['description'] = ''
                    cmsLanguageDetails.append(newArr)
        formSet = CmsLangFormSet(initial=cmsLanguageDetails, prefix='cmsEdit')
    context = {
        'formSet': formSet,
        "languages": languages,
        "cms_page_detail": CmsPageObj,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "cms_pages/edit.html", context)
