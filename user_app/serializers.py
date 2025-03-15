from .models import *
from rest_framework import serializers
from service_app.models import *
from admin_app.models import *
from django.utils.timezone import now

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
    
class list_service_centre(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Service_Centre
        fields = '__all__'
    def get_image(self, obj):
            if obj.image:
                return f"/media/{obj.image.name}"
            return None

class UserProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'

    def get_image(self, obj):
            if obj.image:
                return f"/media/{obj.image.name}"
            return None


class BuyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseProduct
        fields = '__all__'


class UserPurchasedProducts(serializers.ModelSerializer):
    product_name =serializers.SerializerMethodField()

    class Meta:
        model = PurchaseProduct
        fields = '__all__'

    def get_product_name(self,obj):
        return obj.product.name if obj.product else None
    
class UserRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'

class UserViewRepairRequestSerializer(serializers.ModelSerializer):
    service_name = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = ['service_name','services','status','repair_cost','id','service_centre']

    def get_service_name(self,obj):
        return obj.service_centre.name if obj.service_centre else None
    
    
class UserUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['status']
        

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class ChargingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingSlot
        fields = '__all__'

from django.utils.timezone import localtime
class UserViewEVStations(serializers.ModelSerializer):
    slots = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ChargingStations
        fields = '__all__'

    def get_slots(self, obj):
        current_time = localtime().time()  # Get timezone-aware current time
        available_slots = obj.slots.filter(start_time__gt=current_time, is_booked=False)
        return ChargingSlotSerializer(available_slots, many=True).data


    def get_image(self, obj):
        if obj.image:
            return f"/media/{obj.image.name}"
        return None
    

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'slot', 'user', 'payment_status','connector']


class ChargingStationBookingListSerializer(serializers.ModelSerializer):
    charging_station_name = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id','charging_station_name','amount','booking_date','start_time']

    def get_charging_station_name(self, obj):
        return obj.slot.station.name if obj.slot else None
    def get_start_time(self,obj):
        return obj.slot.start_time if obj.slot else None
    
class ViewSingleStationBookingSerializer(serializers.ModelSerializer):
    charging_station_name = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['charging_station_name','amount','booking_date','start_time','end_time','address','charging_status']

    def get_charging_station_name(self, obj):
        return obj.slot.station.name if obj.slot else None

    def get_start_time(self, obj):
        return obj.slot.start_time if obj.slot else None

    def get_end_time(self, obj):
        return obj.slot.end_time if obj.slot else None

    def get_address(self, obj):
        return obj.slot.station.address if obj.slot else None


class StartChargingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['charging_status']


