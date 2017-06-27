from django.conf.urls import url
from . import views

app_name = 'trav'
urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^add', views.add_page, name="add_page"),
    url(r'^new_trip', views.new_trip, name="new_trip"),
    url(r'^travels/join/(?P<tripid>[0-9]+)', views.join, name="join"),
    url(r'^travels/destination/(?P<tripid>[0-9]+)', views.destination, name="dest"),
]
