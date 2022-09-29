from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from knox.views import LogoutAllView


urlpatterns = [
     path("blogs",views.get_all),
     path("blogs/<int:id>",views.get_detail_promo),
     path("auth/user",views.UserView.as_view()),
     path("auth/login/",views.LoginUser.as_view()),
     path("auth/logout/",LogoutAllView.as_view()),
     path("auth/register/",views.RegisterUser.as_view()),
     path("auth/blogs/<int:id>", views.PromoView.as_view()),
     path("blogs/image/<int:id>", views.post_image)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# go to a slash 0, /0 to get the list of all promos.