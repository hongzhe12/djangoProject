from .urls import *

urlpatterns += [
    prefixed_path("article/", include("article.urls")),
    prefixed_path("users/", include("users.urls")),
]
