from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.users.models import User

MODEL_NAME_SINGULER = 'User'
MODEL_NAME_PLURAL = 'Users'


@login_required(login_url='login')
def index(request):
    users = User.objects.filter(user_role_id=2, is_active=True, is_delete=False)
    totalUsers = users.count()
    content = {
        "users": users,
        "total_user": totalUsers,
        'model_name_singular': MODEL_NAME_SINGULER,
        'model_name_plural': MODEL_NAME_PLURAL,
    }
    return render(request, "dashboard/index.html", content)
