from django.conf.urls import url, include
# from django.contrib import admin

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^', include('user_account.urls')),
]
