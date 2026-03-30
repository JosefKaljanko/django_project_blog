from django.urls import path
from.views import (home, about, contact,
                   ContactView,
                   )
#login:
from django.contrib.auth import views as auth_views
from .forms import StyledAuthenticationForm
from .auth_views import MyLoginView
# registrace:
from .views import (signup,
                    SignUpView,
                    )

urlpatterns = [
    # path('', FVB_or_.as_view(), name="url_name"),
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/fvb/', contact, name="contact/fvb"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('login/', MyLoginView.as_view(
        template_name="registration/login.html",
        authentication_form=StyledAuthenticationForm),
         name="login"
         ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path("signup/fbv/", signup, name="signup/fbv"),
    path("signup/", SignUpView.as_view(), name="signup"),
]