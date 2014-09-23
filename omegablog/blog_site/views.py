from django.shortcuts import render_to_response
from django.template import RequestContext


def view_404(request):
    return render_to_response("404.html", RequestContext(request))
