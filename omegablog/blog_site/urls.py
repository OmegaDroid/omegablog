from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home'),
    url(r'^blog_entry/(\d+)$', 'blog.views.view_entry'),
    url(r'^create_blog_entry$', 'blog.views.modify_entry'),
    url(r'^modify_blog_entry/(\d+)$', 'blog.views.modify_entry'),
    url(r'^delete_blog_entry/(\d+)$', 'blog.views.delete_entry'),
    url(r'^browse$', 'blog.views.browse_entries'),

    url(r'^accounts/login', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
    url(r'^accounts/logout', 'django.contrib.auth.views.logout', {"next_page": "/"}),
)

