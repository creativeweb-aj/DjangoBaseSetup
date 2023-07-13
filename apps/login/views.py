from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import BadHeaderError
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from apps.login.form import (ForgotPasswordForm, PasswordChangeForm, PasswordRestOtpForm,
                             PasswordRestForm, ProfileEditForm, UserLoginForm)
from apps.users.models import User
from DjangoBaseSetup.common_modules.emailService import EmailService, EmailType
from DjangoBaseSetup.common_modules.mainService import MainService
from apps.permissions.models import AdminModule, AdminModuleAction
from DjangoBaseSetup.messages.messages import LoginMessages


@csrf_exempt
def login(request):
    if request.method == "GET":
        nextUrl = request.GET.get('next', None)
        request.session['next_url'] = nextUrl

    if request.user.is_authenticated:
        return redirect('dashboard.index')

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None and user.is_delete == 0 and user.user_role_id != 2:
                auth_login(request, user)

                if user.user_role_id == 3:
                    request.session['isAdmin'] = False
                    setUserDataSession(request, user)
                elif user.user_role_id == 1:
                    request.session['isAdmin'] = True
                    setUserDataSession(request, user)
                else:
                    request.session['isAdmin'] = False
                redirectUrl = request.session.get('next_url', None)
                if redirectUrl:
                    if redirectUrl != '/logout/':
                        del request.session['next_url']
                        messages.success(request, LoginMessages.you_are_now_logged_in.value)
                        return redirect(redirectUrl)
                    else:
                        messages.success(request, LoginMessages.you_are_now_logged_in.value)
                        return redirect("dashboard.index")
                else:
                    messages.success(request, LoginMessages.you_are_now_logged_in.value)
                    return redirect("dashboard.index")
            else:
                messages.error(request, LoginMessages.invalid_username_and_password.value)
                return redirect("login")
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = UserLoginForm()
    context = {
        "form": form
    }
    return render(request, "login/login.html", context)


@login_required(login_url='login')
def logOut(request):
    logout(request)
    messages.success(request, LoginMessages.you_are_now_logged_out.value)
    return redirect("login")


def forgotPassword(request):
    if request.user.is_authenticated:
        return redirect('dashboard.index')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = User.objects.filter(email=email)
            if len(users) > 0:
                user = users.first()
                # Create password forgot url and save in db
                service = MainService(request)
                user = service.passwordForgotLink(user)
                try:
                    # Email service to send email
                    try:
                        EmailService(request, user, EmailType.forgotPassword.value)
                    except Exception as e:
                        print("error is ====>",e)
                    messages.success(request, LoginMessages.forgot_password_email_sent_success.value)
                except BadHeaderError:
                    messages.error(request, LoginMessages.email_not_sent.value)
                return redirect('/')
            else:
                messages.error(request, LoginMessages.email_not_registered.value)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = ForgotPasswordForm()
    context = {
        "form": form
    }
    return render(request, 'login/forgot_password.html', context)


def passwordReset(request, token):
    userObj = User.objects.filter(forgot_password_string=token).first()
    if not userObj:
        return redirect('login')
    form = PasswordRestForm()
    if request.method == "POST":
        form = PasswordRestForm(request.POST, userObj)
        if form.is_valid():
            password = make_password(form.cleaned_data.get("confirm_password"))
            userObj.password = password
            userObj.confirm_password = form.cleaned_data.get("confirm_password")
            userObj.forgot_password_string = None
            userObj.save()
            try:
                # Email service to send email
                EmailService(request, userObj, EmailType.passwordReset.value)
                messages.success(request, LoginMessages.password_reset_successfully.value)
            except BadHeaderError:
                messages.error(request, LoginMessages.email_not_sent.value)
            return redirect('login')

        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {
        "form": form,
        "user_detail": userObj,
        "token": token
    }
    return render(request, 'login/reset_password.html', context)


def passwordResetOtp(request):
    form = PasswordRestOtpForm()
    if request.method == "POST":
        form = PasswordRestOtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            userObj = User.objects.filter(forgot_password_otp=otp).first()
            if userObj:
                password = make_password(form.cleaned_data.get("confirm_password"))
                userObj.password = password
                userObj.confirm_password = form.cleaned_data.get("confirm_password")
                userObj.forgot_password_string = None
                userObj.forgot_password_otp = None
                userObj.save()
                # Email service to send email
                EmailService(request, userObj, EmailType.passwordReset.value)
                messages.success(request, LoginMessages.password_reset_successfully.value)
                return redirect('login')
            else:
                messages.error(request, 'error')
                return redirect('login')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {
        "form": form,
        # "user_detail": userObj,
        # "token": token
    }
    return render(request, 'login/reset_password_otp.html', context)


@login_required(login_url='login')
def profile(request):
    userDetail = User.objects.filter(id=request.user.id, is_active=True, is_delete=False).first()
    if not userDetail:
        return redirect('dashboard.index')
    initialDict = {
        "email": userDetail.email,
        "first_name": userDetail.first_name,
        "last_name": userDetail.last_name,
    }
    form = ProfileEditForm(initial=initialDict)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=userDetail)
        if form.is_valid():
            form.save()
            messages.success(request, LoginMessages.profile_update_successfully.value)
            return redirect('dashboard.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {
        "form": form
    }
    return render(request, "login/user_profile.html", context)


@login_required(login_url='login')
def updatePassword(request):
    userDetail = User.objects.get(id=request.user.id)
    if not userDetail:
        return redirect('dashboard.index')
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, instance=userDetail)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            userDetail.password = make_password(new_password)
            userDetail.confirm_password = new_password
            userDetail.save()
            messages.success(request, LoginMessages.password_has_been_updated_successfully.value)
            return redirect('dashboard.index')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = PasswordChangeForm()
    context = {
        "form": form
    }
    return render(request, "login/change_password.html", context)


# Set UserApi data in session from UserApi and modules
def setUserDataSession(request, user):
    userData = dict()
    userData['user_role_id'] = user.user_role_id
    userData['user_id'] = user.id
    userData['email'] = user.email
    # Make modules list and urls list by calling this method
    # if request.session['isAdmin']:
    #     moduleData = makeAdminUserModuleData()
    # else:
    #     moduleData = makeUserModuleData(UserApi)
    moduleData = makeAdminUserModuleData()
    urlsList = moduleData['moduleUrls']
    urlsSets = set(urlsList)
    urlsList = list(urlsSets)
    userData['module_urls'] = urlsList
    userData['modules'] = moduleData['modules']
    request.session['userData'] = userData
    return True


# Making segments list
def makeSegmentsList(segmentString):
    if segmentString is not None:
        try:
            segments = [segments.strip() for segments in segmentString.split(',')]
        except NotImplementedError:
            print('Exception ==> ', NotImplementedError)
            segments = [segmentString]
    else:
        segments = list()
    return segments


# def makeUserModuleData(UserApi):
#     userModulesIds = UserPermission.objects.filter(UserApi=UserApi).values_list('module', flat=True)
#     userPermissionActObjs = UserPermissionAction.objects.filter(UserApi=UserApi).values_list('module_action', flat=True)
#     module_objs = AdminModule.objects.filter(id__in=userModulesIds).filter(parent_id=None).order_by('module_order')
#     module_action_objs = AdminModuleAction.objects.filter(id__in=userPermissionActObjs)
#     modules = []
#     moduleUrls = []
#     parent_urls = []
#     parent_act_url = []
#     child_urls = []
#     for module in module_objs:
#         moduleData = dict()
#         parent_urls.append(module.path)
#         moduleData['module_id'] = module.id
#         moduleData['module_title'] = module.title
#         moduleData['module_path'] = module.path
#         moduleData['module_segment'] = makeSegmentsList(module.segment)
#         moduleData['module_order'] = module.module_order
#         moduleData['module_icon'] = module.icon

#         sub_moduleids = UserPermission.objects.filter(module__parent_id=module).values_list('module', flat=True)
#         sub_modules = AdminModule.objects.filter(id__in=sub_moduleids).order_by('module_order')
#         sub_module_data = []
#         if sub_modules is not None:
#             for sub_module in sub_modules:
#                 child_urls.append(sub_module.path)
#                 sub_module_arr = dict()
#                 sub_module_arr['sub_module_id'] = sub_module.id
#                 sub_module_arr['sub_module_title'] = sub_module.title
#                 sub_module_arr['sub_module_path'] = sub_module.path
#                 sub_module_arr['sub_module_segment'] = makeSegmentsList(sub_module.segment)
#                 sub_module_arr['sub_module_order'] = sub_module.module_order
#                 sub_module_arr['sub_module_icon'] = sub_module.icon
#                 sub_module_data.append(sub_module_arr)

#         for module_action in module_action_objs:
#             parent_act_url.append(module_action.function_name)

#         moduleData['sub_modules'] = sub_module_data

#         if module.parent_id is None or module.parent_id == '':
#             modules.append(moduleData)
#     moduleUrls += parent_urls
#     moduleUrls += parent_act_url
#     moduleUrls += child_urls
#     data = {
#         'moduleUrls': moduleUrls,
#         'modules': modules,
#     }
#     return data


def makeAdminUserModuleData():
    modulesObj = AdminModule.objects.all().order_by("module_order")
    modules = []
    moduleUrls = []
    parent_urls = []
    parent_act_url = []
    child_urls = []
    child_act_urls = []
    for module in modulesObj:
        moduleData = dict()
        parent_urls.append(module.path)
        moduleData['module_id'] = module.id
        moduleData['module_title'] = module.title
        moduleData['module_path'] = module.path
        moduleData['module_segment'] = makeSegmentsList(module.segment)
        moduleData['module_order'] = module.module_order
        moduleData['module_icon'] = module.icon
        sub_modules = AdminModule.objects.filter(parent_id=module).order_by("module_order")
        sub_module_data = []
        if sub_modules is not None:
            for sub_module in sub_modules:
                child_urls.append(sub_module.path)
                sub_module_arr = dict()
                sub_module_arr['sub_module_id'] = sub_module.id
                sub_module_arr['sub_module_title'] = sub_module.title
                sub_module_arr['sub_module_path'] = sub_module.path
                sub_module_arr['sub_module_segment'] = makeSegmentsList(sub_module.segment)
                sub_module_arr['sub_module_order'] = sub_module.module_order
                sub_module_arr['sub_module_icon'] = sub_module.icon
                module_actions = AdminModuleAction.objects.filter(admin_module_id=sub_module)
                module_action_data = []
                for module_action in module_actions:
                    child_act_urls.append(module_action.function_name)
                    module_action_arr = {'id': module_action.id, 'name': module_action.name,
                                         'function_name': module_action.function_name}
                    module_action_data.append(module_action_arr)
                sub_module_arr['actions'] = module_action_data
                sub_module_data.append(sub_module_arr)

        module_action_data = []
        module_actions = AdminModuleAction.objects.filter(admin_module_id=module)
        for module_action in module_actions:
            parent_act_url.append(module_action.function_name)
            module_action_arr = {'id': module_action.id, 'name': module_action.name,
                                 'function_name': module_action.function_name}
            module_action_data.append(module_action_arr)

        moduleData['sub_modules'] = sub_module_data
        moduleData['actions'] = module_action_data

        if module.parent_id is None or module.parent_id == '':
            modules.append(moduleData)
    moduleUrls += parent_urls
    moduleUrls += parent_act_url
    moduleUrls += child_urls
    moduleUrls += child_act_urls

    data = {
        'moduleUrls': moduleUrls,
        'modules': modules,
    }
    return data
