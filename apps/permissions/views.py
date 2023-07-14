import re
from urllib.parse import urlencode
from django.db.models import Q
from DjangoBaseSetup.common_modules.mainService import MainService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .form import ModuleAddForm
from .models import AdminModule, AdminModuleAction
from DjangoBaseSetup.messages.messages import PermissionMessages


@login_required(login_url='login')
def index(request):
    DB = AdminModule.objects.all()
    modulesData = DB

    if request.GET.get('id'):
        id = request.GET.get('id')
        DB = DB.filter(Q(parent_id=id) | Q(id=id))

    if request.GET.get('title'):
        title = request.GET.get('title').strip()
        DB = DB.filter(title__icontains=title)

    if request.GET.get('module_order'):
        moduleOrder = request.GET.get('module_order')
        DB = DB.order_by("-" + moduleOrder).all()

    if request.GET.get('is_active'):
        DB = DB.filter(is_active=request.GET.get('is_active'))

    orderBy = request.GET.get('order_by', "created_at")
    direction = request.GET.get('direction', "DESC")

    if direction == "DESC":
        DB = DB.order_by("-" + orderBy).all()
    else:
        DB = DB.order_by(orderBy).all()

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
        'page': page,
        'page_range': pageRange,
        'total_record': totalRecord,
        'order_by': orderBy,
        'direction': direction,
        'searching_variables': searchingVariables,
        'query_string': queryString,
        'modules': modulesData
    }
    return render(request, "permissions/index.html", context)


@login_required(login_url='login')
@csrf_exempt
def add(request):
    if request.method == 'POST':
        form = ModuleAddForm(request.POST or None)
        count = request.POST['count']
        if form.is_valid():
            module = AdminModule()
            module.parent_id = form.cleaned_data["parent_id"]
            module.title = form.cleaned_data["title"]
            module.path = form.cleaned_data["path"]
            module.segment = form.cleaned_data['segment']
            module.module_order = form.cleaned_data['module_order']
            module.icon = form.cleaned_data["icon"]
            module.save()
            for i in range(0, int(count) + 1):
                moduleAction = AdminModuleAction()
                moduleAction.admin_module_id = module
                moduleAction.name = request.POST['name-' + str(i)]
                moduleAction.function_name = request.POST['function_name-' + str(i)]
                moduleAction.save()
            messages.success(request, PermissionMessages.acl_has_been_added_successfully.value)
            return redirect('module.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = ModuleAddForm()
    context = {
        "form": form,
    }
    return render(request, "permissions/add.html", context)


@login_required(login_url='login')
@csrf_exempt
def edit(request, id):
    module = AdminModule.objects.get(id=id)
    if not module:
        return redirect('dashboard.index')
    moduleActions = AdminModuleAction.objects.filter(admin_module_id__id=id)
    adminModule = []
    countGet = 0
    for action in moduleActions:
        countGet += 1
        adminArr = {'name': action.name, 'function_name': action.function_name}
        adminModule.append(adminArr)
    initialDict = {
        "parent_id": module.parent_id,
        "title": module.title,
        "path": module.path,
        "segment": module.segment,
        "module_order": module.module_order,
        "icon": module.icon
    }
    form = ModuleAddForm(initial=initialDict)
    if request.method == "POST":
        form = ModuleAddForm(request.POST, instance=module)
        count = request.POST['count']
        if form.is_valid():
            form.save()
            AdminModuleAction.objects.filter(admin_module_id__id=id).delete()
            for i in range(0, int(count) + 1):
                moduleAction = AdminModuleAction()
                moduleAction.admin_module_id = module
                try:
                    moduleAction.name = request.POST['name-' + str(i)]
                    moduleAction.function_name = request.POST['function_name-' + str(i)]
                    moduleAction.save()
                except:
                    pass
            messages.success(request, PermissionMessages.acl_has_been_updated_successfully.value)
            return redirect('module.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {
        'form': form,
        'admin_module': adminModule,
        'action_count': countGet - 1,
        'module_data': module,
    }
    return render(request, 'permissions/edit.html', context)


@login_required(login_url='login')
def delete(request, id):
    service = MainService(request)
    isPermission = service.checkPermission(request.user, 'module.delete')
    if not isPermission:
        return redirect('dashboard.index')
    AdminModule.objects.filter(id=id).delete()
    messages.success(request, PermissionMessages.acl_has_been_deleted_successfully.value)
    return redirect('module.index')


@login_required(login_url='login')
def status(request, id):
    service = MainService(request)
    isPermission = service.checkPermission(request.user, 'module.status')
    if not isPermission:
        return redirect('dashboard.index')
    module = AdminModule.objects.filter(id=id).first()
    if module is None:
        return redirect('dashboard.index')
    if module.is_active:
        module.is_active = False
        messages.success(request, PermissionMessages.acl_deactivated.value)
    else:
        module.is_active = True
        messages.success(request, PermissionMessages.acl_activated.value)
    module.save()
    return redirect('module.index')


@api_view(['GET'])
def addMoreAction(request):
    indexValue = request.GET.get('index')
    templateName = loader.render_to_string("permissions/add_more.html")
    constant = "{" + 'index' + "}"
    messageBody = re.sub(constant, indexValue, templateName)
    messageBody = re.sub(r'&nbsp;', ' ', messageBody, flags=re.IGNORECASE)
    data = {
        'body': messageBody
    }
    return Response(data)
