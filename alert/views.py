import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetags.alert_tags import is_admin, is_curator
from utils import site_strings
from django_odc import api as odc


def signin(request):
    template_data = {'username': request.COOKIES.get('username', '')}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            response = redirect('home')
            response.set_cookie('username', username, max_age=365*24*60*60)
            return response
        template_data['errors'] = [site_strings()['login']['error_username_or_password']]
        template_data['username'] = username
    return render_to_response(
        'signin.html',
        template_data,
        context_instance=RequestContext(request))


@login_required(login_url='/signin')
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='/signin')
def home(request):
    template_data = {}
    if is_admin(request.user):
        return render_to_response(
            'home_admin.html',
            template_data,
            context_instance=RequestContext(request))
    elif is_curator(request.user):
        template_data['datasets'] = odc.get_datasets_for_user(request.user)
        return render_to_response(
            'home_curator.html',
            template_data,
            context_instance=RequestContext(request))
    else:
        return Http404()


@login_required(login_url='/signin')
def curate_dataset(request, dataset_id):
    dataset = odc.get_dataset_for_user_by_id(request.user, dataset_id)
    if request.method == 'POST':
        if not dataset:
            return_data = json.dumps({
                'status': 'error',
                'errors': site_strings()['curate_dataset']['error_no_access_to_dataset']})
            return HttpResponse(return_data, content_type='application/json')
        raw_search_data = json.loads(request.POST.get('search_data', '{}'))
        search_data = {
            'sources': [{'guid': s['guid']} for s in raw_search_data['sources']],
            'filters': [],
            'facets': [],
            'pivots': [],
            'pagination': {'rows': 20}}
        search_results = odc.run_query_for_dataset(request.user, dataset_id, search_data)
        content_template = render_to_string(
            'controls/curation_content_list.html', search_results,
            context_instance=RequestContext(request))
        return_data = {'status': 'ok', 'content_template': content_template}
        return HttpResponse(json.dumps(return_data), content_type='application/json')
    if not dataset:
        messages.add_message(request, messages.ERROR, site_strings()['curate_dataset']['error_no_access_to_dataset'])
        return redirect('home')
    template_data = {'dataset': dataset}
    return render_to_response(
        'curate_dataset.html',
        template_data,
        context_instance=RequestContext(request))


@login_required(login_url='/signin')
def admin_users_summary(request):
    all_users = User.objects.filter(is_active=True).all()
    curators = [u for u in all_users if is_curator(u) and not is_admin(u)]
    admins = [u for u in all_users if is_admin(u)]
    template_data = {'admins': admins, 'curators': curators}
    return render_to_response(
        'controls/admin_users_summery.html',
        template_data,
        context_instance=RequestContext(request))