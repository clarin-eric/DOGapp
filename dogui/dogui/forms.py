from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from typing import List

from dogapi.models import dog


class PIDField(forms.Field):
    def to_python(self, pid_candidates):
        """String to list of strings"""
        if not pid_candidates:
            return []
        return pid_candidates.split(',')

    def validate(self, pid_candidates):
        """Check if all pids"""
        super().validate(pid_candidates)
        for pid_candidate in pid_candidates:
            if dog.is_pid(pid_candidate):
                raise ValidationError(
                    _('%(pid_candidate) is not a PID accepted by DOG. Make sure it is a valid DOI, HDL or URL'),
                    params={'pid_candidate': pid_candidate},
                )


class PIDForm(forms.Form):
    """
    Input form for inserting PID and operation to perform
    """
    FUNCTIONALITIES: List[tuple] = [
        ('sniff', 'sniff'),
        ('identify', 'identify'),
        ('fetch', 'fetch'),
        ('is_pid', 'is pid')
    ]
    pid_field: PIDField = PIDField(label='PID form')
    functionality_field: forms.ChoiceField = forms.ChoiceField(widget=forms.RadioSelect, choices=FUNCTIONALITIES)
