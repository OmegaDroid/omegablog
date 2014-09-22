from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home'),

    url(r'^login$', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^logout$', 'django.contrib.auth.views.logout', {"next_page": "/"}),
)
