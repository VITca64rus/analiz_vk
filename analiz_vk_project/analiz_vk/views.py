from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests

# Create your views here.
def auth(request):
    code = request.GET.get("code", "null")
    if code == "null":
        return HttpResponseRedirect ("https://oauth.vk.com/authorize?client_id=8030169&display=page&redirect_uri=http://127.0.0.1:8000/auth&scope=friends,groups,offline,wall&response_type=code&v=5.131")
    else:
        payload = {'client_id': 8030169, 'client_secret': "5nm9ZnkUNtEKOoukDh9q", 'redirect_uri': "http://127.0.0.1:8000/auth", 'code': code}
        r = requests.get ("https://oauth.vk.com/access_token", params=payload)
        request.session['token_vk'] = r.json()['access_token']
        return HttpResponse("Авторизация успешна")


def index(request):
    token = request.session.get('token_vk')
    if token is None:  # Cookie is not set
        return HttpResponse("Вам необходимо авторизоваться")
    else:
        payload = {'owner_id': 90269231, 'offset': 0, 'count': 1, 'access_token': token, 'v': 5.131}
        r = requests.get("https://api.vk.com/method/wall.get", params=payload)
        return HttpResponse(r.json()['response']['items'][0]['text'])
