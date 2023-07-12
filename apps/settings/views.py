import datetime
import os
from urllib.parse import urlencode
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup.messages.messages import SettingMessages, ValidationMessages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from .models import Setting

VALID_IMAGE_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "gif",
]

# Setting file saving path
SETTING_MEDIA_PATH = 'media/uploads/setting_images/'
SETTING_MEDIA_PATH_UPLOAD = 'uploads/setting_images/'


@login_required(login_url='login')
def index(request):
    DB = Setting.objects.all()
    if request.GET.get('title'):
        title = request.GET.get('title').strip()
        DB = DB.filter(title__icontains=title)
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
        'page': page,
        'page_range': pageRange,
        'page_size': recordPerPage,
        'order_by': orderBy,
        'direction': direction,
        'searching_variables': searchingVariables,
        'query_string': queryString,
        'total_record': totalRecord,
    }
    return render(request, "settings/index.html", context)


@login_required(login_url='login')
def add(request):
    form = ""
    validationErrors = {}
    if request.method == "POST":
        form = request.POST
        if request.POST.get("title") is None or request.POST.get("title") == "":
            validationErrors["title"] = ValidationMessages.title_field_required.value

        if request.POST.get("key") is None or request.POST.get("key") == "":
            validationErrors["key"] = ValidationMessages.key_field_required.value

        if request.POST['input_type'] != 'file' and \
                request.POST['input_type'] != 'checkbox' and \
                request.POST['input_type'] != 'radio':
            if request.POST["value"] is None or request.POST["value"] == "":
                validationErrors["value"] = ValidationMessages.value_field_required.value

        if request.POST.get("input_type") is None or request.POST.get("input_type") == "":
            validationErrors["input_type"] = ValidationMessages.input_field_required.value

        else:
            if Setting.objects.filter(title=request.POST.get("[title]")).exists():
                validationErrors["title"] = ValidationMessages.title_already_exists.value

        if request.POST['input_type'] == 'file':
            if len(request.FILES) > 0:
                file = request.FILES['attachment'].name
                extension = file.split(".")[-1].lower()
                if extension not in VALID_IMAGE_EXTENSIONS:
                    validationErrors["attachment"] = ValidationMessages.file_not_valid.value

        if not validationErrors:
            if request.method == 'POST' and len(request.FILES) != 0:
                fileObj = request.FILES['attachment']
                imgUrl = saveFile(fileObj)
                if imgUrl:
                    settingObj = Setting()
                    settingObj.title = (request.POST["title"]).strip()
                    settingObj.key = (request.POST["key"]).strip()
                    settingObj.value = imgUrl
                    settingObj.input_type = request.POST["input_type"]
                    editAble = request.POST.getlist('editable')
                    if len(editAble) > 0:
                        settingObj.editable = 1
                    else:
                        settingObj.editable = 0
                    settingObj.save()
            else:
                settingObj = Setting()
                if request.POST['input_type'] == 'checkbox':
                    v = request.POST.getlist("checkbox")
                    if len(v) > 0:
                        settingObj.value = 1
                    else:
                        settingObj.value = 0
                elif request.POST['input_type'] == 'radio':
                    r = request.POST.getlist("radio")
                    if len(r) > 0:
                        settingObj.value = 1
                    else:
                        settingObj.value = 0
                else:
                    settingObj.value = (request.POST["value"]).strip()
                settingObj.title = (request.POST["title"]).strip()
                settingObj.key = (request.POST["key"]).strip()
                settingObj.input_type = request.POST["input_type"]
                editAble = request.POST.getlist('editable')
                if len(editAble) > 0:
                    settingObj.editable = 1
                else:
                    settingObj.editable = 0
                settingObj.save()
            messages.success(request, SettingMessages.settings_page_has_been_added_successfully.value)
            return redirect('settings.index')
    context = {
        "form": form,
        "errors": validationErrors,
    }
    return render(request, "settings/add.html", context)


@login_required(login_url='login')
def edit(request, id):
    settingsObj = Setting.objects.get(id=id)
    if not settingsObj:
        return redirect('settings.index')
    form = settingsObj
    validationErrors = {}
    if request.method == "POST":
        form = request.POST
        if request.POST["title"] == "":
            validationErrors["title"] = ValidationMessages.title_field_required.value

        if request.POST["key"] == "":
            validationErrors["key"] = ValidationMessages.key_field_required.value

        if request.POST['input_type'] != 'file' and \
                request.POST['input_type'] != 'checkbox' and \
                request.POST['input_type'] != 'radio':
            if request.POST["value"] == "" or request.POST["value"] is None:
                validationErrors["value"] = ValidationMessages.value_field_required.value

        if request.POST["input_type"] == "":
            validationErrors["input_type"] = ValidationMessages.input_field_required.value

        if request.POST['input_type'] == 'file' and len(request.FILES) > 0:
            file = request.FILES['attachment'].name
            extension = file.split(".")[-1].lower()
            if extension not in VALID_IMAGE_EXTENSIONS:
                validationErrors["attachment"] = ValidationMessages.file_not_valid.value

        if not validationErrors:
            if request.POST['input_type'] == 'file' and len(request.FILES) > 0:
                fileObj = request.FILES['attachment']
                imgUrl = saveFile(fileObj)
                if imgUrl:
                    settingsObj.title = (request.POST["title"]).strip()
                    settingsObj.key = (request.POST["key"]).strip()
                    settingsObj.value = imgUrl
                    settingsObj.input_type = request.POST["input_type"]
                    editAble = request.POST.getlist('editable')
                    if len(editAble) > 0:
                        settingsObj.editable = 1
                    else:
                        settingsObj.editable = 0
                    settingsObj.save()
            elif request.POST['input_type'] != 'file':
                if request.POST['input_type'] == 'checkbox':
                    v = request.POST.getlist("checkbox")
                    if len(v) > 0:
                        settingsObj.value = 1
                    else:
                        settingsObj.value = 0
                elif request.POST['input_type'] == 'radio':
                    r = request.POST.getlist("radio")
                    if len(r) > 0:
                        settingsObj.value = 1
                    else:
                        settingsObj.value = 0
                else:
                    settingsObj.value = (request.POST["value"]).strip()
                settingsObj.title = (request.POST["title"]).strip()
                settingsObj.key = (request.POST["key"]).strip()
                settingsObj.input_type = request.POST["input_type"]
                editAble = request.POST.getlist('editable')
                if len(editAble) > 0:
                    settingsObj.editable = 1
                else:
                    settingsObj.editable = 0
                settingsObj.save()
            messages.success(request, SettingMessages.setting_has_been_updated_successfully.value)
            return redirect('settings.index')
    context = {
        "form": form,
        "errors": validationErrors,
        "settings_detail": settingsObj
    }
    return render(request, "settings/edit.html", context)


# this function use for delete data
@login_required(login_url='login')
def delete(request, id):
    Setting.objects.filter(id=id).delete()

    messages.success(request, SettingMessages.setting_has_been_deleted_successfully.value)
    return redirect('settings.index')


# this function use for settings prefix
@login_required(login_url='login')
def prefix(request, key):
    if request.method == "POST":
        settingsObjs = Setting.objects.filter(key__icontains=key).order_by('-id')
        if settingsObjs.count() > 0:
            for setting in settingsObjs:
                if setting.input_type == 'file':
                    try:
                        file = request.FILES[setting.key]
                        if file:
                            fileObj = request.FILES[setting.key]
                            imgUrl = saveFile(fileObj)
                            if imgUrl:
                                setting.value = imgUrl
                                setting.save()
                    except KeyError:
                        print(f'KeyError : {KeyError}')
                else:
                    if setting.input_type == 'checkbox':
                        v = request.POST.getlist(setting.key)
                        if len(v) > 0:
                            setting.value = 1
                        else:
                            setting.value = 0
                        setting.save()
                    elif setting.input_type == 'radio':
                        r = request.POST.getlist(setting.key)
                        if len(r) > 0:
                            setting.value = r[0]
                        else:
                            setting.value = ''
                        setting.save()
                    elif setting.input_type == 'textarea':
                        try:
                            values = request.POST.get(setting.key)
                            setting.value = values.strip()
                            setting.save()
                        except KeyError:
                            print(f'KeyError : {KeyError}')
                    elif setting.input_type == 'text':
                        try:
                            values = request.POST.get(setting.key)
                            setting.value = values.strip()
                            setting.save()
                        except KeyError:
                            print(f'KeyError : {KeyError}')
                    elif setting.input_type == 'select':
                        value = request.POST.getlist(setting.key)
                        value = value[0]
                        setting.value = value
                        setting.save()
            messages.success(request, SettingMessages.setting_has_been_updated_successfully.value)
    else:
        settingsObjs = Setting.objects.filter(key__icontains=key).order_by('-id')
        if settingsObjs is None:
            settingsObjs = []
    context = {
        "results": settingsObjs,
        "key": key
    }
    return render(request, "settings/prefix.html", context)


# To save file and create folder
def saveFile(fileObj):
    # Create folder
    day = str(datetime.datetime.now().day)
    month = str(datetime.datetime.now().month)
    year = str(datetime.datetime.now().year)
    dateTime = day + '-' + month + '-' + year
    folder = SETTING_MEDIA_PATH + dateTime + "/"
    folderDirectory = SETTING_MEDIA_PATH_UPLOAD + dateTime + "/"
    if not os.path.exists(folder):
        os.mkdir(folder)
    # Save file
    try:
        fs = FileSystemStorage()
        fileName = fileObj.name.split(".")[0].lower()
        fileName = fileName.replace(' ', '')
        extension = fileObj.name.split(".")[-1].lower()
        timeStamp = str(int(datetime.datetime.now().timestamp()))
        newFileName = fileName + '-' + timeStamp + "." + extension
        fs.save(folderDirectory + newFileName, fileObj)
        imageUrl = '/' + SETTING_MEDIA_PATH + dateTime + '/' + newFileName
    except FileNotFoundError:
        print(f'Exception ==> {FileNotFoundError}')
        imageUrl = ''
    return imageUrl
