from urllib.parse import urlencode
from DjangoBaseSetup.common_modules.mainService import MainService
from DjangoBaseSetup.messages.messages import LoginMessages, UserMessages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import BadHeaderError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from DjangoBaseSetup.common_modules.emailService import EmailService, EmailType
from apps.users.models import User
from django.db.models import Q
from .form import UserAddForm, UserPasswordChangeForm, UserForm

MODEL_NAME_SINGULAR = 'User'
MODEL_NAME_PLURAL = 'Users'


@login_required(login_url='login')
def index(request):
    DB = User.objects.filter(is_delete=0, user_role_id=2)

    if request.GET.get('id'):
        _id = request.GET.get('id')
        DB = DB.filter(id__icontains=_id)

    if request.GET.get('username'):
        name = request.GET.get('username').strip()
        DB = DB.filter(username__icontains=name)

    if request.GET.get('full_name'):
        full_name = request.GET.get('full_name').strip()
        first, last = full_name.split()
        DB = DB.filter(Q(first_name__icontains=first) & Q(last_name__icontains=last))

    if request.GET.get('mobile_number'):
        mobileNumber = request.GET.get('mobile_number').strip()
        DB = DB.filter(mobile_number__icontains=mobileNumber)

    if request.GET.get('email'):
        email = request.GET.get('email').strip()
        DB = DB.filter(email__icontains=email)

    if request.GET.get('is_active'):
        DB = DB.filter(is_active=request.GET.get('is_active'))

    fromDate = request.GET.get('registered_from')
    toDate = request.GET.get('registered_to')
    if fromDate and toDate:
        # fromDate = fromDate+' 00:00'
        # toDate = toDate+' 23:59'
        DB = DB.filter(created_at__gte=fromDate)
        DB = DB.filter(created_at__lte=toDate)
    elif fromDate:
        # fromDate = fromDate + ' 00:00'
        DB = DB.filter(created_at__gte=fromDate)
    elif toDate:
        # toDate = toDate + ' 23:59'
        DB = DB.filter(created_at__lte=toDate)

    orderBy = request.GET.get('order_by', "created_at")
    direction = request.GET.get('direction', "DESC")
    if direction == "DESC":
        DB = DB.order_by("-" + orderBy)
    else:
        DB = DB.order_by(orderBy)

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

    content = {
        'results': results,
        'page_start': pageStart,
        'page_end': pageEnd,
        'page_range': pageRange,
        "total_record": totalRecord,
        'order_by': orderBy,
        'direction': direction,
        'searching_variables': searchingVariables,
        'user_detail': DB,
        'query_string': queryString,
        'page': page,
        'page_size': recordPerPage,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, 'users/index.html', content)


@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST or None)
        if form.is_valid():
            users = User()
            users.user_role_id = 2
            users.username = form.cleaned_data["username"]
            users.first_name = form.cleaned_data["first_name"]
            users.last_name = form.cleaned_data["last_name"]
            users.email = form.cleaned_data["email"]
            users.mobile_number = form.cleaned_data["mobile_number"]
            users.password = make_password(form.cleaned_data["password"])
            users.confirm_password = form.cleaned_data["confirm_password"]
            users.save()
            # Email service to send email
            # EmailService(request, users, EmailType.register.value)
            messages.success(request, UserMessages.user_has_been_added_successfully.value)
            return redirect('users.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = UserAddForm()
    context = {
        "form": form,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "users/add.html", context)


@login_required(login_url='login')
def edit(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('dashboard.index')
    initialDict = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number
    }
    form = UserForm(initial=initialDict)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, UserMessages.user_profile_has_been_updated_successfully.value)
            return redirect('users.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {
        'form': form,
        'user_data': user,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, 'users/edit.html', context)


@login_required(login_url='login')
def view(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('dashboard.index')
    context = {
        "user_data": user,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "users/view.html", context)


@login_required(login_url='login')
def status(request, id):
    user = User.objects.filter(id=id).first()
    if user is None:
        return redirect('dashboard.index')
    if user.is_active:
        user.is_active = False
        messages.success(request, UserMessages.user_deactivated.value)
    else:
        user.is_active = True
        messages.success(request, UserMessages.user_activated.value)
    user.save()
    return redirect('users.index')


@login_required(login_url='login')
def changePassword(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('dashboard.index')
    if request.method == "POST":
        form = UserPasswordChangeForm(request.POST, instance=user)
        if form.is_valid():
            user.password = make_password(form.cleaned_data['confirm_password'])
            user.confirm_password = form.cleaned_data['confirm_password']
            user.save()
            messages.success(request, UserMessages.user_password_updated_successfully.value)
            return redirect('users.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = UserPasswordChangeForm()
    context = {
        'user_data': user,
        'form': form,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "users/change_password.html", context)


@login_required(login_url='login')
def delete(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('dashboard.index')
    user.is_delete = True
    user.is_active = False
    user.email = user.email + '_deleted_' + str(id)
    user.username = user.username + '_deleted_' + str(id)
    user.save()
    messages.success(request, UserMessages.user_has_been_deleted_successfully.value)
    return redirect('users.index')


@login_required(login_url='login')
def sendCredential(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('dashboard.index')
    try:
        # Email service to send email
        EmailService(request, user, EmailType.loginCredentials.value)
        messages.success(request, LoginMessages.login_credentials_email_sent_successfully.value)
    except BadHeaderError:
        messages.error(request, LoginMessages.email_not_sent.value)
    return redirect('users.index')
