from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from user_account import views


urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view(template_name='bootstrapous/login.html',
                                            redirect_authenticated_user=True), name='login', ),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='bootstrapous/login.html',
                                                  redirect_authenticated_user=True), name='login', ),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/$', login_required(views.user_account_page), name='user_account'),
    url(r'^accounts/profile/edit/$', login_required(views.edit_user_fields), name='edit_user_account'),
    url(r'^accounts/profile/hashtags/$', login_required(views.hashtags), name='hashtags'),
    url(r'^accounts/profile/hashtags/add/$', login_required(views.add_hashtag), name='add_hashtag'),
    url(r'^accounts/profile/hashtags/(?P<pk>[-\w]+)/$', login_required(views.edit_hashtag), name='edit_hashtag'),
    url(r'^accounts/profile/hashtags/delete/(?P<pk>[-\w]+)/$', login_required(views.delete_hashtag), name='delete_hashtag'),
    url(r'^accounts/profile/posts/$', login_required(views.posts), name='posts'),
    url(r'^accounts/profile/posts-data/$', login_required(views.posts_raw), name='posts-data'),
    url(r'^accounts/profile/posts-likes/$', login_required(views.posts_likes), name='posts-likes'),
    url(r'^accounts/profile/posts-shares/$', login_required(views.posts_shares), name='posts-shares'),
    url(r'^accounts/profile/posts-recent/$', login_required(views.posts_recent), name='posts-recent'),
    url(r'^accounts/profile/top_post_likes/$', login_required(views.top_post_likes), name='top-post-likes-count'),
    url(r'^accounts/profile/top_post_shares/$', login_required(views.top_post_shares), name='top-post-shares-count'),
    url(r'^accounts/profile/help/$', login_required(views.help), name='help'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
