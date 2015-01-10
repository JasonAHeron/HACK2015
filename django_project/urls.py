from django.conf.urls import patterns, include, url
from hack import views as v
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',

	url(r'^$', v.IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/',v.test),

    # Twilio URLs
    url(r'^sms/$', v.sms),
)

