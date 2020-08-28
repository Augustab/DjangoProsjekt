from django import forms

class sumForm(forms.Form):
    '''Formen til der man legger inn et utlegg/inntekt'''
    kategori = forms.IntegerField
    sum = forms.IntegerField
    beskrivelse = forms.CharField
    date = forms.DateField

class slettForm(forms.Form):
    '''Formen for å slette en booking'''
    sumid = forms.IntegerField


class AccountForm(forms.Form):
    name = forms.CharField
    belop = forms.IntegerField
    interest = forms.CharField