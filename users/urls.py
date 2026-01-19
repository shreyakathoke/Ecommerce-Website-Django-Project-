from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.base_view, name="base"),
    path("shop/", views.shop_view, name="shop"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    

    path("products/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_view, name="category_view"),

    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),
    path("cart/order-summary/", views.order_summary, name="order_summary"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("add-product/", views.add_product, name="add_product"),
   
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("product/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("product/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    


    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('checkout/success/', views.order_success, name='order_success'),
    path("search/", views.search, name="search"),
    path('update-cart-ajax/', views.update_cart_ajax, name='update_cart_ajax'),
    path('cart/update/', views.update_cart_ajax, name='update_cart_ajax'),
    path('cart/remove/', views.remove_cart_ajax, name='remove_cart_ajax'),
    path('my-orders/', views.my_orders, name='my_orders'),

    
]
