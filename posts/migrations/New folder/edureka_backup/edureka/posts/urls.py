from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('webadmin/', views.webadmin, name='webadmin'),
    path('addpost/', views.add_post, name='addpost'),
    path('category/<str:slug>/', views.post_by_category, name='catpost'),
    path('addcat/', views.add_cat, name='addcat'),
    path('add_course/', views.add_course, name='addcourse'),
    path('allposts/', views.allposts, name='allposts'),
    path('<str:category_slug>/<str:slug>/', views.post_details, name='details'),
    path('allcat/', views.allcat, name='allcat'),
    path('allcourse/', views.allcourse, name='allcourses'),
    path('editpost/<int:id>', views.edit_post, name='editpost'),
    path('deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('editcat/<int:id>', views.edit_cat, name='editcat'),
    path('deletecat/<int:id>', views.delete_cat, name='deletecat'),
    path('editcourse/<int:id>', views.edit_course, name='editcourse'),
    path('deletecourse/<int:id>', views.delete_course, name='deletecourse'),
    path('userlogin/', views.login, name='userlogin'),
    path('usersignup/', views.signup, name='usersignup'),
    path('userlogout/', views.logout, name='logout'),
    path('userdashboard/', views.userdashboard, name='userhome'),
    path('userprofile/', views.userprofile, name='profile'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
