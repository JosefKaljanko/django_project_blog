from django.contrib import messages
from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, "Přihlášení úspěšné")
        # return super(MyLoginView, self).form_valid(form)
        return super().form_valid(form)