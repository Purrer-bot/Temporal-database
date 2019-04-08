from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^horse/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),

    url(r'^post/(?P<pk>\d+)/cancel/$', views.post_cancel, name='post_cancel'),
    url(r'^post/(?P<pk>\d+)/restore/$', views.post_restore, name='post_restore'),
   
    url(r'^journal', views.journal_list, name='journal_list'),
    
    url(r'^fresh', views.post_fresh, name='post_fresh'),

    #Возможно не заработает
    url(r'^post/(?P<pk>\d+)/(?P<jk>\d+)/iter/$', views.post_iter, name='post_iter'),
    url(r'^post/(?P<pk>\d+)/(?P<rk>\d+)/rest/$', views.post_rest, name='post_rest')

   
    
]
#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
