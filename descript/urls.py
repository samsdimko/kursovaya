from django.conf.urls import url

from descript import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/(?P<page_id>\d+)/(?P<ima>\w+\.\w+)/$', views.Page1View.as_view(), name='page'),
    url(r'^(?P<page_id>\d+)/(?P<ima>\w+\.\w+)/name/$', views.name, name='name'),
    url(r'^(?P<page_id>\d+)/(?P<ima>\w+\.\w+)/quest/$', views.quest, name='quest'),
#    url('modal/', views.ModalView.as_view(), name='mymodal'),    
    url(r'^modal/(?P<pk>\d+)/(?P<page_id>\d+)/$', views.ModalView.as_view(), name='mymodal'),
    url(r'^(?P<page_id>\d+)/(?P<one>\d+)/next_page/$', views.next_page, name='next_page'),
]
