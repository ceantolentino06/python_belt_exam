from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_user$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^register_user$', views.register),
    url(r'^jobs/new$', views.render_create),
    url(r'^jobs/new/add_job$', views.add_job),
    url(r'^jobs/edit/(?P<job_id>[0-9]+)$', views.render_edit),
    url(r'^jobs/edit/edit_job$', views.edit_job),
    url(r'^jobs/view/(?P<job_id>[0-9]+)$', views.render_view),
    url(r'^jobs/remove/(?P<job_id>[0-9]+)$', views.delete_job),
    url(r'^jobs/add/(?P<job_id>[0-9]+)$', views.add_user_job),
    url(r'^jobs/give_up/(?P<job_id>[0-9]+)$', views.remove_user_job),
]