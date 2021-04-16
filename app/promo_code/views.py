from django.shortcuts import render

from .forms import NewCodeForm



def create_code(request):
    if request.method == "POST":
        form = NewCodeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            group = form.cleaned_data["group"]
            

    form = NewCodeForm()
    return render(
        request,
        "promo_code/index.html",
        {
            "form": form
        })

