from django.db import models
from django.db.models.signals import pre_save

from omegablog.utils.date_time import now


class Entry(models.Model):
    title = models.CharField(unique=True, blank=False, null=False, max_length=100)
    creation_time = models.DateTimeField(default=None, null=True)
    last_edit_time = models.DateTimeField(default=None, null=True)
    content = models.TextField(blank=False, null=False)


def _entry_post_save_update_dates(sender, **kwargs):
    current_time = now()
    entry = kwargs["instance"]
    if not entry.creation_time:
        entry.creation_time = current_time
    entry.last_edit_time = current_time

pre_save.connect(_entry_post_save_update_dates, sender=Entry)