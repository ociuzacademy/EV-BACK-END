from django.contrib import admin
from .import views
from django.urls import path,include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from  rest_framework.routers import DefaultRouter
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Service App API(ev_care)",
        default_version="v1",
        description="API documentation for the Service App.",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"user_register",UserRegistrationView,basename="user_register")
router.register(r"user_register_vehicle",RegisterVehicleView,basename="user_regiter_vehicle")
router.register(r"buy_product",BuyProduct,basename='buy_product')
router.register(r"repair_request",UserRepairView,basename='repair_request')
router.register(r"feedback",UserFeedbackView,basename='feedback')
router.register(r"book_slot",BookSlotView,basename='book_slot')

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    path('',include(router.urls)),
    path('login/',LoginView.as_view(),name="login"),
    path('list_service_centres/', ListServiceCentresView.as_view({'get': 'list'}), name='list_service_centres'),
    path('view_products/',ViewProducts.as_view({'get':'list'}),name='view_products'),
    path('view_single_product/',ViewSingleProductView.as_view({'get':'list'}),name='view_single_product'),
    path('user_view_profile/',UserProfileView.as_view({'get':'list'}),name='user_view_profile'),
    path('user_vehicle_profile/',UserVehicleView.as_view({'get':'list'}),name='user_vehicle_profile'),
    path('user_purchased_products/',UserPurchsedProductsView.as_view({'get':'list'}),name='user_purchased_products'),
    path('view_repair_requests/',ViewRepairRequestView.as_view({'get':'list'}),name='view_repair_requests'),
    path('view_single_repair_request/',ViewSingleRepairRequestView.as_view({'get':'list'}),name='view_single_repair_requests'),
    path('user_update_status/',UserUpdateStatusView.as_view(),name='user_update_status'),
    path('view_ev_stations/',ViewEvStationView.as_view({'get':'list'},name='view_ev_stations')),
    path('view_single_charging_station/',ViewSingleEvStation.as_view({'get':'list'}),name='view_single_ev_station'),
    path('booking_history/',ChargingStationBookingHistoryView.as_view({'get':'list'}),name='booking_history'),
    path('single_booking/',ViewSingleStationBookingView.as_view({'get':'list'}),name='single_booking'),
    path('start_charging/',StartCharging.as_view(),name='start_charging'),
    path('stop_charging/',FinishCharging.as_view(),name='stop_charging'),
]   