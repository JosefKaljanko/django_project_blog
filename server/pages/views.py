from django.contrib import messages
from django.shortcuts import render, redirect
from.forms import ContactForm
from django.views import View
from django.http import HttpResponse

# registrace:
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomRegistrationForm
def home(request):
    # return HttpResponse("""<h1>Hello django, I´m programmer :)</h1>
    # <p>Tady je text paragrafu.</p>""")

    messages.success(request, "Message partial funguje... OK")
    messages.warning(request, "Message partial Warning funguje... OK")
    messages.info(request, "Message partial Info funguje... OK")
    messages.error(request, "Message partial Error funguje... OK")
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Díki, Zpráva byla odeslána (demo)")
            print("ODESLANO - jdeme na REDIRECT")
            # data = form.cleaned_data
            # print(data)
            return redirect("contact")
    else:
        print("není POST takže pouštím GET požadavek")
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})



# -----------okey, máme nádherný formulář a funkční, co bychom mohli dále udělat??
# něco co nás něco naučí??? nebo opakovat a zahrnout do toho nové CVB (s def get() a def post())....
# co bys doporučil ty??


# import Viev

class ContactView(View):
    """CBV view - funkce GET a POST"""
    template_name = "pages/contact.html"

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # tady pozdeji email/DB/integrtace
            messages.success(request, "Díki! Zpráva byla Odeslána (Class base view)...")
            return redirect("contact")
        messages.error(request, "Oprav prosím chyby ve Formuláři...")
        return render(request, self.template_name, {"form":form})




from django.urls import reverse_lazy
from django.views.generic.edit import FormView

class ContactFormView(FormView):
    """CBV - django way """
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        messages.success(self.request, "Díki! Zpráva byla odeslána...")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Oprav prosím chyby ve formuláři...")
        return super().form_invalid(form)


# registrace:
def signup(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        print("METHOD FBV: ",request.method)
        print("FBV POST: ",request.POST)
        form = UserCreationForm(request.POST)
        print("FORM POST: ",form)
        if form.is_valid():
            print("CL DATA: ",form.cleaned_data)
            user = form.save()      # vytvoří usera, uloží hash heslo
            print("USER: ",user)
            login(request, user)    # autologin po reg
            print("FBV AUTOLOGIN")
            messages.success(request, "Účet vytvořen, jsi přihlášen...")
            return redirect(next_url or "home")
    else:
        print("METHOD FBV: ", request.method)
        form = UserCreationForm()
        print("FORM GET: ", form)
    return render(request, "registration/signup.html", {"form": form, "next": next_url})


class SignUpView(FormView):
    print("START VIEW:")
    template_name = "registration/signup.html"
    form_class = CustomRegistrationForm
    print("ALL Form Fields: ", form_class)
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        print("Form Cleaned data: ",form.cleaned_data)
        user = form.save()
        print("View form_valid USER: ",user)
        login(self.request, user)
        print("Jsem za AUTOLOGIN")
        messages.success(self.request, "Účet vytvořen.. Jsi přihlášen")

        next_url = self.request.POST.get("next")
        print("Next URL: ", next_url)
        return redirect(next_url) if next_url else super().form_valid(form)

