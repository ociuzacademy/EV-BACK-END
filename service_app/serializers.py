from .models import *
from rest_framework import serializers
from rest_framework import serializers
from .models import Service_Centre
from user_app.models import *
from django.utils.timezone import now

class ServiceCentreRegisterSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Add a custom field for media path

    class Meta:
        model = Service_Centre
        fields = [
            'name', 'username', 'address', 'phone', 'email', 
            'password', 'latitude', 'longitude', 'utype', 'image'
        ]

    def get_image(self, obj):
        # Customize the media path
        if obj.image:  # Replace `image` with the field you use for media files
            return f"/media/{obj.image.name}"
        return None


# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service_Centre
#         fields = ['username','password']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'



class ViewProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image.name}"
        return None


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

        def get_image(self, obj):
        # Return relative path starting with /media/ instead of full URL
            if obj.image:
                return f"/media/{obj.image.name}"
            return None

        def validate_image(self, value):
            if not value:
                raise serializers.ValidationError("Image is required.")
            return value
    

class ViewPurchasedProductSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseProduct
        fields = '__all__'

    def get_user_name(self, obj):
        # Get the user's name from the related User model
        return obj.user.name if obj.user else None

    def get_product_name(self, obj):
        # Get the product's name from the related Products model
        return obj.product.name if obj.product else None

    def get_unit_price(self, obj):
        # Assume price per unit is the same as the product's price field
        return str(obj.product.price) if obj.product else None
    

class ViewRepairRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    vehicle_num = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = ['user_name','vehicle_num','id','status']

    def get_user_name(self,obj):
        return obj.user.name if obj.user else None
    def get_vehicle_num(self,obj):
        return obj.vehicle.registration_num if obj.vehicle else None
    

class ViewSingleRepairSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    vehicle_num = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = ['id','user_name','vehicle_num','employee_name','services','created_at','status','updated_at','repair_cost','service_centre']

    def get_user_name(self,obj):
        return obj.user.name if obj.user else None
    def get_vehicle_num(self,obj):
        return obj.vehicle.registration_num if obj.vehicle else None
    def get_employee_name(self,obj):
        return obj.employee.name if obj.employee else ""
    

class ViewEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name']

class ViewAllEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','username','email','phone_number','service_centre']


class AssignEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['employee','status']


class EmployeeViewAssignedRepairSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    vehicle_num = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = ['user_name','vehicle_num','id','status']

    def get_user_name(self,obj):
        return obj.user.name if obj.user else None
    def get_vehicle_num(self,obj):
        return obj.vehicle.registration_num if obj.vehicle else None
    

class EmployeeUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['status']

class EmployeeProfileSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee  # Corrected `models` to `model`
        fields = ['id', 'username', 'name', 'email', 'phone_number', 'service_name']

    def get_service_name(self, obj):
        return obj.service_centre.name if obj.service_centre else None
    

class ServicViewProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service_Centre
        fields = ['name','username','address','phone','email','image','id']

    def get_image(self, obj):
        # Customize the media path
        if obj.image:  # Replace `image` with the field you use for media files
            return f"/media/{obj.image.name}"
        return None

class ViewFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['user_name','feedback','repair','date']

    def get_user_name(self,obj):
        return obj.user.name if obj.user else None
    

class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class PresentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'username', 'email', 'phone_number', 'service_centre']


class AttendanceListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'status']

    def get_status(self, obj):
        today = now().date()
        is_present = Attendance.objects.filter(employee=obj, date=today).exists()
        return "Present" if is_present else "Absent"
    
class ApproveLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class RejectLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


