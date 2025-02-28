from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('service-centres/', views.list_service_centres, name='list_service_centres'),
    path('approved_centres/', views.approved_centres, name='approved_centres'),
    path('rejected_centres/', views.rejected_centres, name='rejected_centres'),
    path('service-centres/<int:centre_id>/', views.service_centre_details, name='service_centre_details'),
    path('service-centres/<int:centre_id>/products/', views.list_service_centre_products, name='list_service_centre_products'),
    path('service-centres/<int:centre_id>/employees/', views.list_service_centre_employees, name='list_service_centre_employees'),
    path('employees/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('service-centres/<int:centre_id>/<str:action>/', views.approve_or_reject_service_centre, name='approve_or_reject_service_centre'),
    path('admin_index/',views.adminindex,name='admin_index'),
    path('index/',views.index,name='index'),
    path('',views.login,name='login'),
    path('add_station/',views.add_ev_station,name='add_station'),
    path('list_ev_stations/',views.list_ev_stations,name='list_ev_stations'),
    path('ev_station_details/<int:station_id>/', views.ev_station_details, name='ev_station_details'),
    path('station_booking_count/', station_booking_count, name='station_booking_count'),
]