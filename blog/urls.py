from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='post_list'),
    path('detail/<slug:slug>', views.ArticleDetailView.as_view(), name='detail'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.ArticleSearchView.as_view(), name='search'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
]
