from django import forms


class ReportForm(forms.Form):
    unverified_nationality_field = forms.CharField(required=False)
    verified_nationality_field = forms.CharField(required=False)
    score_field = forms.FloatField(required=False)
