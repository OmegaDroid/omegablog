from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from omegablog.blog.models import EntryForm, Entry


def home(request):
    """
    Generates the blog landing page

    :param request: The HttpRequest object
    :return: The HttpResponse object
    """
    return render_to_response("home.html", RequestContext(request))


@login_required
def modify_entry(request, pk=None):
    """
    Generates the page for modifying/creating a blog entry. To edit an entry the user will have to be the owner of the
    entry otherwise a HttpResponseForbidden is returned.

    :param request: The HttpRequest object
    :param pk: The primary key of the entry to edit. If None a new entry form is created
    :return: The HttpResponse object
    """
    form = EntryForm()
    if request.POST:
        form = EntryForm(request.POST)
        if form.is_valid():
            elem = form.save(commit=False)
            elem.owner = request.user
            elem.save()
            return HttpResponseRedirect("/blog_entry/" + str(elem.pk))

    return render_to_response("modify_blog_entry.html", RequestContext(request, {
        "form": form,
    }))


def view_entry(request, pk):
    try:
        entry = Entry.objects.get(id=pk)
        return render_to_response("entry.html", RequestContext(request, {
            "entry": entry,
            "editable": request.user.is_authenticated() and request.user == entry.owner,
        }))
    except Entry.DoesNotExist:
        raise Http404
