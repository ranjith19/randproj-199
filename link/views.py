from django.http import JsonResponse, HttpResponse
import json
import urllib.parse as parse
from django.shortcuts import render
import random
from .models import UPILink
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import os

hosted_at = os.environ.get("HOST", "http://localhost:8000")


@csrf_exempt
def create_vpa_link(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        request_data = json.loads(request.body)
        vpa = request_data.get('vpa')
        amount = request_data.get('amount')
        name = parse.quote(request_data.get('name'))
        notes = parse.quote(request_data.get('notes'))
        tid = int(random.random() * 10000000000)
        s = "upi://pay?cu=INR&mode=01&pa={vpa}&pn={name}&am={amount}&tr={tid}&tn={notes}".format(
            vpa=vpa, amount=amount, name=name, notes=notes, tid=tid
        )
        host = request.META.get("HTTP_HOST", hosted_at)
        upiLink = UPILink.objects.create(
            link=s, json_data=json.dumps(request_data))
        l = "{0}/pay/{1}".format(hosted_at, upiLink.identifier)
        return JsonResponse(status=200, data={"link": l})
    return JsonResponse(status=405, data={})


def linkpage(request, payId):
    x = UPILink.objects.get(identifier=payId)
    if UPILink.objects.filter(identifier=payId).exists():
        upiLink = UPILink.objects.get(identifier=payId)
        context = dict(upiLink=upiLink.link)
        return render(request, 'link/index.html', context)
    return HttpResponse("Not found", status=404)


def data_view(request, payId):
    x = UPILink.objects.get(identifier=payId)
    print(UPILink.objects.filter(identifier=payId).exists())
    if UPILink.objects.filter(identifier=payId).exists():
        upiLink = UPILink.objects.get(identifier=payId)
        data = {}
        try:
            data = json.loads(str(upiLink.json_data))
        except Exception as e:
            print(e)
        return JsonResponse(status=200, data=data)
    return HttpResponse("Not found", status=404)
