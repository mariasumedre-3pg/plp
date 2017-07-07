' add polls url patterns so server can direct requests to the correct views '
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/results$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<pk>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<slug>[-\w]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'$', views.IndexView.as_view(), name='index'),
]
