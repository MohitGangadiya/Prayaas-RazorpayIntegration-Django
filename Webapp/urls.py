# Importing necessary modules
from django.urls import path
from django.contrib import admin
from Webapp import views

# Admin site settings
admin.site.site_header = 'Prayaas'
admin.site.site_title = ' Prayaas'
admin.site.index_title = 'Database'

# Specifying path
urlpatterns = [
    path('', views.index, name='index'),
    path('donate', views.donate, name='donate'),
    path('pay', views.pay, name='pay'),
    path('success', views.success, name='success'),
]