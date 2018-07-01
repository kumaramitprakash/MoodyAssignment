from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^medals_data', views.medal_data_list, name='medal_data_list'),
    url(r'^chart_data', views.analytics_data, name='analytics_data'),
]


