from django import forms


class SearchForm(forms.Form):
    tax_code = forms.CharField(max_length=50, label='Tax Code', widget=forms.TextInput(attrs={
        'placeholder': 'Vui lòng nhập mã tra cứu',
        'class': 'form-control'
    }))
