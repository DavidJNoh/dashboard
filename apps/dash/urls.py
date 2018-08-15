from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^wall/(?P<id>\d+)$', views.wall),
    url(r'^edit$', views.edit),
    url(r'^adminedit/(?P<id>\d+)$', views.adminedit),
    url(r'^adminadd$', views.adminadd),
    url(r'^login$', views.login),
    url(r'^register_process$', views.register_process),
    url(r'^add$', views.add),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^updatepassword/(?P<id>\d+)$', views.updatepassword),
    url(r'^adminupdate/(?P<id>\d+)$', views.adminupdate),
    url(r'^adminupdatepassword/(?P<id>\d+)$', views.adminupdatepassword),
    url(r'^updatestatus/(?P<id>\d+)$', views.updatestatus),
    url(r'^message/(?P<id>\d+)$', views.message),
    url(r'^comment/(?P<id>\d+)$', views.comment),
    url(r'^clear$', views.clear),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^deletemessage/(?P<id>\d+)$', views.deletemessage),
    url(r'^deletecomment/(?P<id>\d+)$', views.deletecomment)
]    