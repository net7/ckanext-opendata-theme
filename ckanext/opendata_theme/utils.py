#import ckan.lib.base as base
import ckan.plugins.toolkit as t
#from ckan.common import request

#render = base.render

def credits_index(context=None):
    data = t.request.params or {}
    vars = {'data': data}
    return t.render('credits.html', extra_vars=vars)

def infog_index(context=None):
    data = t.request.params or {}
    vars = {'data': data}
    return t.render('infografica.html', extra_vars=vars)

def reports_index():
    try:
        reports = t.get_action('report_list')({}, {})
    except t.NotAuthorized:
        t.abort(401)
    return t.render('report.html', extra_vars={'reports': reports})


