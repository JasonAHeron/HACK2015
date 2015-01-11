from django.conf.urls import patterns, include, url
from hack import views as v
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',

	url(r'^$', v.index_view),
	url(r'rest$', v.rest_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/',v.test),
    # Registration Page
    url(r'^register/$', v.register, name='register'),
    url(r'^build/',v.build_classes),

    # Twilio URLs
    url(r'^sms/$', v.sms),
)

