from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response("home.html", RequestContext(request))


@login_required
def modify_entry(request, pk=None):
    return render_to_response("modify_blog_entry.html", RequestContext(request))
