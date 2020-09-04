from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from home_app import forms
from products_app.models import Product


def index(request):
    """
    the homepage view --> form SearchView
    """
    try:
        request.session['language']
    except KeyError:
        request.session['language'] = 'FR'
    if request.method == 'POST':
        searchform = forms.SearchView(request.POST)
        if searchform.is_valid():
            pass
        else:
            # just display the error on console
            print(searchform.errors)
    else:
        searchform = forms.SearchView()
    context = {'searchform': searchform}
    return render(request, 'home_app/layouts/home.html/', context)


def mentions(request):
    return render(request, "home_app/layouts/mentions.html")


def autocomplete_search(request):
    if request.is_ajax():
        prod_to_search = request.GET.get('term', '')
        prods = Product.objects.filter(pname__istartswith=prod_to_search)
        result = []
        for prod in prods:
            pname_json = prod.pname
            result.append(pname_json)
        data = json.dumps(result)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def test_error(request):
    return 1/0

@csrf_exempt
def set_language(request):
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        language = str(request_data['language'])
        request.session['language'] = language
        data = {'data': 'OK'}
    return JsonResponse(data)