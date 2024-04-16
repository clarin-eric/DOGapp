from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from typing import List

from dogapi.models import dog


class PIDField(forms.CharField):
    def to_python(self, pid_candidates):
        """String to list of strings"""
        if not pid_candidates:
            return []
        return pid_candidates.split(',')

    def validate(self, pid_candidates):
        """Check if all pids"""
        super().validate(pid_candidates)
        # TODO ask for local validation vs api call
        # for pid_candidate in pid_candidates:
        #     if dog.is_pid(pid_candidate):
        #         raise ValidationError(
        #             '%(pid_candidate) is not a PID accepted by DOG. Make sure it is a valid DOI, HDL or URL',
        #             params={'pid_candidate': pid_candidate},
        #         )

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        return value


class PIDForm(forms.Form):
    """
    Input form for inserting PID and operation to perform
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pid_field'].label = ""
        self.fields['functionality_field'].label = ""

    FUNCTIONALITIES: List[tuple] = [
        ('sniff', 'sniff'),
        # ('identify', 'identify'),
        ('fetch', 'fetch'),
        ('ispid', 'is pid'),
    ]
    pid_field: PIDField = PIDField(required=True,
                                   widget=forms.TextInput(attrs={'required': 'True'}))
    functionality_field: forms.ChoiceField = forms.ChoiceField(choices=FUNCTIONALITIES, required=True,
                                                               widget=forms.RadioSelect(
                                                                   attrs={'class': 'form-check-inline',
                                                                          'required': 'True'}), )
