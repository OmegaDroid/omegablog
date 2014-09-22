from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home'),
    url(r'^create_blog_entry$', 'blog.views.modify_entry'),
    url(r'^modify_blog_entry/(\d+)$', 'blog.views.modify_entry'),

    url(r'^accounts/login', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {"next_page": "/"}),
)
