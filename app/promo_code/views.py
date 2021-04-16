from django.shortcuts import render

from .forms import NewCodeForm
from .services import generate_promo_code, get_code_group



def generate_code(request):
    codes = None
    if request.method == "POST":
        form = NewCodeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            group = form.cleaned_data["group"]
            codes = generate_promo_code(amount, group)

    form = NewCodeForm()
    return render(
        request,
        "promo_code/index.html",
        {
            "form": form,
            "codes": codes
        })



# def get_group(request):
#     codes = None
#     if request.method == "POST":
#         form = NewCodeForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data["amount"]
#             group = form.cleaned_data["group"]
#             codes = generate_promo_code(amount, group)

#     form = NewCodeForm()
#     return render(
#         request,
#         "promo_code/index.html",
#         {
#             "form": form,
#             "codes": codes
#         })
