from django import template
from apps.settings.models import Setting
from django.contrib.sites.shortcuts import get_current_site
import datetime


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


register = template.Library()
register.tag('assign', do_assign)


class SegmentNode(template.Node):
    def __init__(self, name, value, segmentCount):
        self.name = name
        self.value = value
        self.segmentCount = segmentCount

    def render(self, context):
        context[self.name] = self.value.resolve(context, True).split("/")[self.segmentCount]
        return ''


def get_segment(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return SegmentNode(bits[1], value, 0)


register.tag('get_segment', get_segment)


def get_segment1(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return SegmentNode(bits[1], value, 1)


register.tag('get_segment1', get_segment1)


def get_segment2(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return SegmentNode(bits[1], value, 2)


register.tag('get_segment2', get_segment2)


def get_segment3(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return SegmentNode(bits[1], value, 3)


register.tag('get_segment3', get_segment3)


@register.simple_tag(name='site_title')
def site_title():
    try:
        setting = Setting.objects.get(key__icontains="Site.title")
        return setting.value
    except:
        return ""


@register.simple_tag(name='site_logo', takes_context=True)
def site_logo(context):
    request = context['request']
    baseUrl = str(get_current_site(request))
    baseUrl = 'http://' + baseUrl
    try:
        setting = Setting.objects.get(key__icontains="Site.logo")
        url = baseUrl + setting.value
        return url
    except:
        return ""


@register.simple_tag(name='site_favicon', takes_context=True)
def site_favicon(context):
    request = context['request']
    baseUrl = str(get_current_site(request))
    baseUrl = 'http://' + baseUrl
    try:
        setting = Setting.objects.get(key__icontains="Site.favicon")
        url = baseUrl + setting.value
        return url
    except:
        return ""


@register.simple_tag(name='date_format')
def dateFormat():
    try:
        setting = Setting.objects.get(key__icontains="Reading.date_format")
        dateFormatString = setting.value
        return dateFormatString
    except None:
        return ""


@register.filter()
def to_int(value):
    return int(value)


@register.filter()
def set_date(value):
    try:
        if type(value) == datetime.datetime or type(value) == datetime.date:
            setting = Setting.objects.get(key__icontains="Reading.date_format")
            readingDateFormat = setting.value.strip()
            date = value.strftime(readingDateFormat)
        else:
            setting = Setting.objects.get(key__icontains="Reading.date_format")
            readingDateFormat = setting.value.strip()
            try:
                convert = datetime.datetime.fromisoformat(value)
                date = convert.strftime(readingDateFormat)
            except Exception as e:
                print(f'Exception ==> {e}')
                return ""
        return date
    except Exception as e:
        print(f'Exception ==> {e}')
        return ""


@register.filter()
def set_date_time(value):
    try:
        if type(value) == datetime.datetime or type(value) == datetime.date:
            setting = Setting.objects.get(key__icontains="Reading.date_time_format")
            readingDateFormat = setting.value.strip()
            date = value.strftime(readingDateFormat)
            print(f'{type(value)} date, value, readingDateFormat ==> {date}, {value}, {readingDateFormat}')
        else:
            setting = Setting.objects.get(key__icontains="Reading.date_time_format")
            readingDateFormat = setting.value.strip()
            try:
                convert = datetime.datetime.fromisoformat(value)
                date = convert.strftime(readingDateFormat)
                print(f'{type(value)} date, value, readingDateFormat ==> {date}, {value}, {readingDateFormat}')
            except Exception as e:
                print(f'Exception ==> {e}')
                return ""
        return date

    except Exception as e:
        print(f'Exception ==> {e}')
        return ""


@register.simple_tag(name='modules', takes_context=True)
def Module(context):
    request = context['request']
    try:
        data = request.session['userData']
        modules = data['modules']
    except:
        modules = []
    return modules


@register.simple_tag(name='actions_list', takes_context=True)
def getCurrentModule(context):
    request = context['request']
    try:
        data = request.session['userData']
        actionsList = data['module_urls']
    except:
        actionsList = []
    return actionsList


@register.simple_tag(name='isAdmin', takes_context=True)
def getIsAdmin(context):
    request = context['request']
    try:
        data = request.session['userData']
        roleId = data['user_role_id']
        if roleId == 1:
            isAdmin = True
        else:
            isAdmin = False
    except:
        isAdmin = False
    return isAdmin


@register.simple_tag(name='current_url', takes_context=True)
def settingsUrls(context):
    request = context['request']
    currentUrlName = request.path_info.split('/')[-1]
    return currentUrlName


@register.filter
def check_segment(value):
    if value:
        segment = value
    else:
        segment = 'index'
    return segment
