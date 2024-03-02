from django.urls import path
from .  import views
urlpatterns=[
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login_page,name="login_page"),
    path('logout/',views.logout_page,name="logout_page"),
    path('collection',views.collection,name="collection"),
    path('collections/<str:name>',views.collectionview,name='collections'),
    path('collections/<str:name>/<str:pname>',views.product_detail,name='product_detail'),
    path('addtocart',views.add_to_cart,name='add_to_cart'),
    path('veiwcart',views.viewcart,name="viewcart"),
    path('removecart/<str:id>',views.removecart,name="removecart"),
    path('favorite',views.favorite,name ="favorite"),
    path('viewfavorite',views.viewfavorite,name="viewfavorite"),
    path('removefavorite/<str:id>',views.removefavorite,name="removefavorite"),



]
