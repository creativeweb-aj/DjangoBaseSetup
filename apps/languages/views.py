from urllib.parse import urlencode
from DjangoBaseSetup import settings
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup.messages.messages import LanguageMessages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from .models import *


@login_required(login_url='login')
def index(request):
    languages = Languages.objects.all()
    if request.GET.get('title'):
        title = request.GET.get('title').strip()
        languages = languages.filter(title__icontains=title)

    order_by = request.GET.get('order_by', "created_at")
    direction = request.GET.get('direction', "DESC")
    if direction == "DESC":
        languages = languages.order_by("-" + order_by).all()
    else:
        languages = languages.order_by(order_by).all()
    recordPerPage = settings.READING_RECORD_PER_PAGE
    page = request.GET.get('page', 1)
    paginator = Paginator(languages, recordPerPage)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    # Get the index of the current page
    pageStart = results.start_index()
    pageEnd = results.end_index()
    
    # Get page range
    pageRange = MainService.getPageRange(results, paginator)

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
        'page': page,
        'page_range': pageRange,
        'order_by': order_by,
        'direction': direction,
        'searching_variables': searchingVariables,
        'query_string': queryString,
    }

    return render(request, "languages/index.html", context)


@login_required(login_url='login')
def edit(request, id):
    ObjDetail = Languages.objects.filter(id=id).first()
    if not ObjDetail:
        return redirect('languages.index')

    form = ObjDetail
    validationErrors = {}
    if request.method == "POST":
        form = request.POST

        if request.POST["title"] == "":
            validationErrors["title"] = "The language name field is required."

        if request.POST["lang_code"] == "":
            validationErrors["lang_code"] = "The language code field is required."

        if request.POST["folder_code"] == "":
            validationErrors["folder_code"] = "The folder code field is required."

        if not validationErrors:
            Obj = ObjDetail
            Obj.title = request.POST["title"]
            Obj.lang_code = request.POST["lang_code"]
            Obj.folder_code = request.POST["folder_code"]
            Obj.save()
            messages.success(request, LanguageMessages.languageUpdateSuccess.value)
            return redirect('languages.index')

    context = {
        "form": form,
        "errors": validationErrors,
        "ObjDetail": ObjDetail,
    }
    return render(request, "languages/edit.html", context)


