from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (HomeView, AboutView,
                    Shopview,
                    BlogView,
                    Shop_detailsView,
                    ShoppingcartView,
                    Blog_detailsView, Add_productView, CommentView, OrderView, IncrementCountAPIView,
                    DecrementCountAPIView, ChangeCountAPIView)

urlpatterns=[
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('shop', Shopview.as_view(), name='shop'),
    path('blog', BlogView.as_view(), name='blog'),
    path('shop-details', Shop_detailsView.as_view(), name='shop_detail'),
    path('shopping-cart', ShoppingcartView.as_view(), name='shop_cart'),
    path('blogs', Blog_detailsView.as_view(), name='blogs'),
    path('add-product', Add_productView.as_view(), name='add_product'),
    path('comment', CommentView.as_view(), name='comment'),
    path('checkout', OrderView.as_view(), name='checkout'),
    path('increment', csrf_exempt(IncrementCountAPIView.as_view()), name='increment'),
    path('decrement', csrf_exempt(DecrementCountAPIView.as_view()), name='decrement'),
    path('change', csrf_exempt(ChangeCountAPIView.as_view()), name='change'),
]