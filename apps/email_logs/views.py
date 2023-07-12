from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from DjangoBaseSetup.common_modules.mainService import MainService
from apps.email_logs.models import EmailLog
from django.db.models import Q

MODEL_NAME_SINGULAR = 'Email Log'
MODEL_NAME_PLURAL = 'Email Logs'


@login_required(login_url='login')
def index(request):
    DB = EmailLog.objects.all()

    if request.GET.get('email'):
        email = request.GET.get('email').strip()
        DB = DB.filter(Q(email_from__icontains=email) | Q(email_to__icontains=email))

    if request.GET.get('subject'):
        subject = request.GET.get('subject').strip()
        DB = DB.filter(subject__icontains=subject)

    fromDate = request.GET.get('registered_from')
    toDate = request.GET.get('registered_to')
    if fromDate and toDate:
        fromDate = fromDate + ' 00:00'
        toDate = toDate + ' 23:59'
        DB = DB.filter(created_at__gte=fromDate)
        DB = DB.filter(created_at__lte=toDate)
    elif fromDate:
        fromDate = fromDate + ' 00:00'
        DB = DB.filter(created_at__gte=fromDate)
    elif toDate:
        toDate = toDate + ' 23:59'
        DB = DB.filter(created_at__lte=toDate)

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
    return render(request, "email_logs/index.html", context)


@login_required(login_url='login')
def view(request, id):
    emailLog = EmailLog.objects.get(id=id)
    if not emailLog:
        return redirect('dashboard.index')
    context = {
        "result": emailLog,
        'model_name_singular': MODEL_NAME_SINGULAR,
        'model_name_plural': MODEL_NAME_PLURAL
    }
    return render(request, "email_logs/popup.html", context)
