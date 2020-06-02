from django.urls import path
from . import views

urlpatterns = [
    path('',views.userDetails),
    path('logout',views.logout),
    path('new', views.makeWish),
    path('stats', views.checkStats),
    path('remove_wish/<int:wish_id>', views.removeWish),
    path('edit_wish/<int:wish_id>', views.editWish),
    path('grant_wish/<int:wish_id>', views.grantWish),
    path('like_wish/<int:wish_id>', views.likeWish),

]