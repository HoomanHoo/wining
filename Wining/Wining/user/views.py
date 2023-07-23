from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.base import View

from purchasing.models import WinReceiveCode


# Create your views here.
class ShowReceiveCodeView(View):
    def get(self, request):
        template = loader.get_template("user/showReceiveCode.html")
        receive_codes = WinReceiveCode.objects.filter().values("receive_code")
        context = {"receive_codes": receive_codes}

        return HttpResponse(template.render(context, request))
