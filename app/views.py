from django.shortcuts import render

from .forms import SearchForm
from .models import Product


def search_product(request):
    product = None
    show_warning = False

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            tax_code = form.cleaned_data["tax_code"]
            try:
                product = Product.objects.get(tax_code=tax_code)
            except Product.DoesNotExist:
                show_warning = True
    else:
        form = SearchForm()

    return render(
        request,
        "products/search.html",
        {"form": form, "product": product, "show_warning": show_warning},
    )
