from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django import forms

from blog_utils.date_time import now


class Entry(models.Model):
    """
    Class describing a blog entry
    """
    title = models.CharField(unique=True, blank=False, null=False, max_length=100)
    creation_time = models.DateTimeField(default=None, null=True)
    last_edit_time = models.DateTimeField(default=None, null=True)
    content = models.TextField(blank=False, null=False)
    owner = models.ForeignKey(get_user_model())


@receiver(pre_save, sender=Entry, dispatch_uid="blog_entry_pre_save_signal")
def _entry_post_save_update_dates(sender, **kwargs):
    """
    Updates the created and last edited times for the entry

    :param sender: The model class sending the commit
    :param kwargs: Keyword arguments sent by the signal (https://docs.djangoproject.com/en/1.5/ref/signals/#pre-save)
    """
    current_time = now()
    entry = kwargs["instance"]
    if not entry.creation_time:
        entry.creation_time = current_time
    entry.last_edit_time = current_time


class EntryForm(forms.ModelForm):
    """
    Form used for creating and updating blog entries
    """
    class Meta:
        model = Entry

        exclude = (
            "creation_time",
            "last_edit_time",
            "owner",
        )