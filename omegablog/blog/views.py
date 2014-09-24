from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from blog.models import EntryForm, Entry
from blog_utils.queries import first_or_none


def home(request):
    """
    Generates the blog landing page

    :param request: The HttpRequest object
    :return: The HttpResponse object
    """
    latest = first_or_none(Entry.objects.all().order_by("-last_edit_time"))
    return render_to_response("home.html", RequestContext(request, {
        "entry": latest,
    }))


@login_required
def modify_entry(request, pk=None):
    """
    Generates the page for modifying/creating a blog entry. To edit an entry the user will have to be the owner of the
    entry otherwise a HttpResponseForbidden is returned.

    :param request: The HttpRequest object
    :param pk: The primary key of the entry to edit. If None a new entry form is created
    :return: The HttpResponse object
    """
    elem = get_object_or_404(Entry, id=int(pk)) if pk else None
    if elem and elem.owner != request.user or not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.POST:
        form = EntryForm(request.POST, instance=elem)
        if form.is_valid():
            elem = form.save(commit=False)
            elem.owner = request.user
            elem.save()
            return HttpResponseRedirect("/blog_entry/" + str(elem.pk))
    else:
        form = EntryForm(instance=elem)

    return render_to_response("modify_blog_entry.html", RequestContext(request, {
        "form": form,
    }))


def view_entry(request, pk):
    """
    Generates the page for viewing the requested blog entry.

    :param request: The HttpRequest object
    :param pk: The primary key of the entry to edit. If None a new entry form is created
    :return: The HttpResponse object
    """
    entry = get_object_or_404(Entry, id=pk)
    return render_to_response("entry.html", RequestContext(request, {
        "entry": entry,
        "editable": request.user.is_authenticated() and request.user == entry.owner,
    }))


def delete_entry(request, pk):
    """
    Handles deleting a blog post and redirecting home.

    :param request: The HttpRequest object
    :param pk: The primary key of the entry to edit. If None a new entry form is created
    :return: The HttpResponse object
    """
    elem = get_object_or_404(Entry, id=int(pk))
    if elem and elem.owner != request.user or not request.user.is_authenticated():
        return HttpResponseForbidden()

    elem.delete()
    return HttpResponseRedirect("/")