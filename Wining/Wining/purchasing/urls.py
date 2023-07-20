from django.urls.conf import path
from purchasing import views

urlpatterns = [
    path("store-list", views.StoreListView.as_view(), name="storeList"),
    path(
        "detail-product-info",
        views.DetailProductInfoView.as_view(),
        name="detailProductInfo",
    ),
    path("buy-list", views.BuyListView.as_view(), name="buyList"),
    path("add-cart-list", views.AddPickListView.as_view(), name="addCartList"),
    path("cart-list", views.PickListView.as_view(), name="cartList"),
    path("order-page", views.OrderPageView.as_view(), name="orderPage"),
]
