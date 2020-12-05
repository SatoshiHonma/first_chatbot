from django.urls import path
from .views import listfunc, formfunc, detailfunc

urlpatterns = [
    path('', listfunc, name='list'),
    path('form/', formfunc, name='form'),
    path('detail/<int:pk>', detailfunc, name='detail'),
]
