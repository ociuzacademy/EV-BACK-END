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
router.register(r"service_register",ServiceCentreRegistrationView,basename='service_register')
router.register(r"add_employee",AddEmployeeView,basename='add_employee')
router.register(r"add_product",AddProducts,basename='add_product')
router.register(r"employee_attendance",EmployeeAttendance,basename='employee_attendance')
router.register(r"approve_leave",ApproveLeaveView,basename='approve_leave')
router.register(r"reject_leave",RejectLeaveView,basename='reject_leave')

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
    path('update_employee/',UpdateEmployeeView.as_view(),name='update_employee'),
    path('view_products/',ViewProducts.as_view({'get':'list'}),name='view_products'),
    path('update_product/',UpdateProductView.as_view(),name='update_product'),
    path('update_service_centre/',UpdateServiceCentreView.as_view(),name='update_service_centre'),
    path('view_single_product/',ViewSingleProductView.as_view({'get':'list'}),name='view_single_product'),
    path('view_purchased_products/',ViewPurchsedProducts.as_view({'get':'list'}),name='view_purchased_products'),
    path('view_repair_requests/',ViewRepairRequestView.as_view({'get':'list'}),name='view_repair_requests'),
    path('view_single_repair/',ViewSingleRepairView.as_view({'get':'list'}),name='view_single_repair'),
    path('view_employees/',ViewINEmployeeView.as_view({'get':'list'}),name='view_employees'),
    path('view_all_employees/',ViewAllEmployees.as_view({'get':'list'}),name='view_all_employees'),
    path('assign_employee/',AssignEmployeeView.as_view(),name='assign_employee'),
    path('employee_view_assigned_repairs/',EmployeeViewAssignedRepairView.as_view({"get":'list'}),name='employee_view_assigned_repairs'),
    path('employee_update_status/',EmployeeUpdateStatusView.as_view(),name='employee_update_status'),
    path('employee_view_profile/',EmployeeViewProfileView.as_view({'get':'list'}),name='employee_view_profile'),
    path('service_centre_view_profile/',ServiceViewProfileView.as_view({'get':'list'}),name='service_centre_view_profile'),
    path('view_feedback/',ServiceViewFeedback.as_view({'get':'list'}),name='view_feedback'),
    path('view_present_employees/',ViewPresentEmployeesView.as_view({'get':'list'}),name='view_present_employees'),
    path('attendance_record/',AttendanceListView.as_view({'get':'list'}),name='attendance_record'),
    path('employee_count/',EmployeeCountView.as_view({'get':'list'}),name='employee_count'),
    path('check_attendance/',EmployeeCheckAttendanceView.as_view({'get':'list'}),name='check_attendance')
]