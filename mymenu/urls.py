
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views

urlpatterns = [
    path('myhome/<uuid:pk>', HomeView, name="myhome"),
        # path('exclusive/<str:pk>', ExclusiveView, name="exclusive"),
        # path('special<str:pk>', SpecialView, name="special"),
        # path('qrupdate_item/', updateItem, name = "qrupdateItem"),
        path('search', SearchView.as_view(), name="search"),
        path('login/dashboard', Dashboard, name="dashboard"),
        path('add_product/<str:pk>', AddProduct.as_view(), name="addproduct"),
        path('edit_product/<str:pk>', EditProduct, name="editproduct"),
        path('add_category', AddCategory.as_view(), name="addcategory"),
        path('edit_category/<str:pk>', EditCategory, name="editcategory"),
        path('product_list/<str:pk>', CategoryDetail, name="categorydetail"),
        path('allspecial', AllSpecial, name='allspecial'),
        path('add_special<str:pk>', AddSpecial, name="addspecial"),
        path('remove_special/<str:pk>', RemoveSpecial, name="removespecial"),
        path('allexclusive', AllExclusive, name="allexclusive"),
        path('add_exclusive/<str:pk>', AddExclusive, name="addexclusive"),
        path('delete_exclusive/<str:pk>', DeleteExclusive, name="delete-exclusive"),
        path('edit_exclusive/<str:pk>', EditExclusive, name="edit-exclusive"),
        path('deleteproduct/<str:pk>', DeleteProduct, name="deleteproduct"),
        path('deletecategory/<str:pk>', DeleteCategory, name="deletecategory"),
        path('mylogin/', LoginView.as_view(), name="mylogin"),
        path('register', RegistrationView.as_view(), name="register"),
        path('change-password/', views.change_password, name='change_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)