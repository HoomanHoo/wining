from django.urls.conf import path
from store import views

urlpatterns = [
    path(
        "store-registration",
        views.StoreRegistrationView.as_view(),
        name="storeRegistration",
    ),
    path(
        "product-addition", views.ProductAdditionView.as_view(), name="productAddition"
    ),
    path("store-mypage", views.StoreMyPageView.as_view(), name="storeMyPage"),
    path("search-product", views.SearchProduct.as_view(), name="searchProduct"),
]
