from django.http import JsonResponse, HttpResponse
import json
import urllib.parse as parse
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
        upiLink = UPILink.objects.create(link=s)
        l = "{0}/pay/{1}".format(hosted_at, upiLink.identifier)
        return JsonResponse(status=200, data={"link": l})
    return JsonResponse(status=405, data={})


template = """
<HTML>
<HEAD>
<TITLE>Your Title Here</TITLE>
</HEAD>
<BODY BGCOLOR="FFFFFF">
<HR>
<div>
Pay bill
</div>
<img id="top-logo" style="width: 100px; margin: 20px;" src="https://setu.co/static/media/logo-dp-on-tp.52e425de.svg" alt="Setu logo">

<a style="font-size:30px;" href="{upiLink}">Open UPI to pay</a>

<HR>

</BODY>

</HTML>
"""


def linkpage(request, payId):
    x = UPILink.objects.get(identifier=payId)
    print(UPILink.objects.filter(identifier=payId).exists())
    if UPILink.objects.filter(identifier=payId).exists():
        upiLink = UPILink.objects.get(identifier=payId)
        content = template.format(upiLink=upiLink.link)
        return HttpResponse(content)
    return HttpResponse("Not found", status=404)
