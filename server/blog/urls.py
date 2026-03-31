from django.urls import path
from .views import (post_list, post_detail,             # FBV - funkční view
                    post_mine,post_publish,
                    PostListView, PostDetailView,        # CVB - class View
                    post_create,post_update,
                    )

app_name = "blog"
#        = v HTML volame template name "blog:name"   npř.: "blog:post_detail"
#        = redirect("app_name:template_name"

urlpatterns = [
    path("mine/fvb/", post_mine, name="post_mine"),  # FVB
    path("<slug:slug>/publish/", post_publish, name="post_publish"),  # FVB
    path('fvb/', post_list, name="post_list"),                      # FVB
    path("", PostListView.as_view(), name="post_list"),         # CVB
    path("new/", post_create, name="post_create"),  # FVB CREATE - musí být před slug
    path("<slug:slug>/edit/", post_update, name="post_update"),  # FVB UPDATE

    path('<slug:slug>/fvb/', post_detail, name="post_detail"),      # FVB
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),     # CVB
]