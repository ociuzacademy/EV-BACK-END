from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from service_app.models import *
from admin_app.models import *
# Create your views here.


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(username=username)
                if password == user.password:
                    response_data = {
                        "status": "success",
                        "message": "User logged in successfully",
                        "user_id": str(user.id)
                    }
                    request.session['id'] = user.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "failed", "message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)



class RegisterVehicleView(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        print("Incoming data:", request.data)  # Debugging

        user_id = request.data.get('user')
        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Authenticated user not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = request.data.copy()
        data['user'] = user_id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()  # Save and get the created instance
            return Response(
                {
                    "status": "success",
                    "message": "Vehicle registered successfully",
                    "vehicle_id": instance.id  # Include the created vehicle ID
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": "failed", "message": "Invalid details", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListServiceCentresView(viewsets.ModelViewSet):
    queryset = Service_Centre.objects.all()
    serializer_class = list_service_centre
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ViewProducts(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = UserProductSerializer

    def list(self, request, *args, **kwargs):
        # Retrieve the service_centre_id from the request body
        service_centre_id = request.query_params.get('service_centre')
        print("Query parameters received:", request.query_params)

        if service_centre_id:
            # Filter products by the provided service_centre_id
            products = self.queryset.filter(service_centre_id=service_centre_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Service Centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ViewSingleProductView(viewsets.ModelViewSet):
    serializer_class = UserProductSerializer
    queryset = Products.objects.all()

    def list(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        print("Query parameters received:", request.query_params)

        if not product_id:
            response_data = {
                "status": "failed",
                "message": "Product ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Products.objects.get(id=product_id)
            print("Product found:", product)
        except Products.DoesNotExist:
            print("Product with ID", product_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "Product does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

 
class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if not user_id:
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            print("user found:", user)
        except Products.DoesNotExist:
            print("user with ID", user_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "User does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserVehicleView(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        print("Query parameters received:", request.query_params)

        if not user_id:
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the single vehicle for the user
            vehicle = Vehicle.objects.get(user=user_id)
        except Vehicle.DoesNotExist:
            print(f"No vehicle found for user_id: {user_id}")
            response_data = {
                "status": "failed",
                "message": "No vehicle found for the specified user."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Serialize the single vehicle object
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyProduct(viewsets.ModelViewSet):
    queryset = PurchaseProduct.objects.all()
    serializer_class = BuyProductSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))  # Default quantity is 1
        
        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not product_id:
            return Response(
                {"status": "failed", "message": "Product ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate Product
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check product availability
        if quantity <= 0:
            return Response(
                {"status": "failed", "message": "Invalid quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if int(product.quantity) < quantity:
            return Response(
                {"status": "failed", "message": "Insufficient product quantity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get service_centre_id
        service_centre = product.service_centre.id

        # Calculate total price
        total_price = product.price * quantity

        # Reduce product quantity
        product.quantity = str(int(product.quantity) - quantity)
        product.save()
        print(request.data)
        # Prepare purchase data
        purchase_data = {
            "user": user.id,
            "product": product.id,
            "quantity": quantity,
            "price": total_price,
            "service_centre": service_centre,
        }
        # print(purchase_data)

        serializer = self.get_serializer(data=purchase_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Product purchased successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": "failed", "message": "Purchase failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserPurchsedProductsView(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseProduct.objects.all()
    serializer_class = UserPurchasedProducts
    def list(self, request, *args, **kwargs):
        # Extract 'service_centre' from query parameters
        user_id = request.query_params.get('user')
        print("Query parameters received:", request.query_params)

        if user_id:
            # Filter products by the provided service_centre_id
            products = self.queryset.filter(user_id=user_id)
            
        else:
            # Return an error response if 'service_centre' is not provided
            response_data = {
                "status": "failed",
                "message": "user ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserRepairView(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = UserRepairSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        vehicle_id = request.data.get('vehicle')
        service_centre_id = request.data.get('service_centre')
        services = request.data.get('services', [])

        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not vehicle_id:
            return Response(
                {"status": "failed", "message": "Vehicle ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not service_centre_id:
            return Response(
                {"status": "failed", "message": "Service centre ID not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not services or not isinstance(services, list):
            return Response(
                {"status": "failed", "message": "Invalid or missing services list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate Vehicle
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Vehicle not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Calculate total repair cost
        total_cost = sum(service.get('amount', 0) for service in services)

        # Update the request data to include the calculated cost
        request.data['repair_cost'] = total_cost

        # Serialize and save the data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Repair request created successfully.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": "failed",
                "message": "Repair request creation failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ViewRepairRequestView(viewsets.ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = UserViewRepairRequestSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user')
        print("Query parameters received:", request.query_params)

        if user_id:
            # Filter products by the provided service_centre_id
            repairs = self.queryset.filter(user_id=user_id).order_by('-created_at')
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "User ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize the filtered queryset
        serializer = self.get_serializer(repairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ViewSingleRepairRequestView(viewsets.ReadOnlyModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = UserViewRepairRequestSerializer
    
    def list(self, request, *args, **kwargs):
        repair_id = request.query_params.get('repair')
        print("Query parameters received:", request.query_params)

        if repair_id:
            # Filter products by the provided service_centre_id
            repairs = self.queryset.get(id=repair_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Repair ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if not repairs:
            response_data = {
                "status": "failed",
                "message": "No repair request with this id exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered queryset
        serializer = self.get_serializer(repairs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserUpdateStatusView(generics.UpdateAPIView):
    queryset = Repair.objects.all()
    serializer_class = UserUpdateStatusSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        repair_id = request.data.get('repair')
        try:
            repair = Repair.objects.get(id=repair_id)  # Retrieve the Employee object
            print(repair)
        except Employee.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Repair request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data.copy()
        data['status'] =  "Vehicle Delivered"

        # Perform partial update with the provided data
        serializer = UserUpdateStatusSerializer(repair, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Status updated successfully",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "message": "Invalid Details",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class UserFeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        service_centre_id = request.data.get('service_centre')
        repair_id = request.data.get('repair')

        if not user_id:
            response_data = {
                "status": "failed",
                "message": "user ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if not service_centre_id:
            response_data = {
                "status": "failed",
                "message": "service_centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if not repair_id:
            response_data = {
                "status": "failed",
                "message": "repair ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            repair = Repair.objects.get(user_id=user_id,id=repair_id,service_centre_id=service_centre_id)
            if repair.status=="Vehicle Delivered":
                repair.status="Feedback Submitted"
                repair.save()
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {
                            "status": "success",
                            "message": "Feedback created successfully.",
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                        {
                            "status": "failed",
                            "message": "vehicle haven't been delivered.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
        except Repair.DoesNotExist:
            return Response(
                {
                    "status": "failed",
                    "message": "Feedback creation failed.",
                },
            status=status.HTTP_400_BAD_REQUEST,
            )
        

class ViewEvStationView(viewsets.ModelViewSet):
    queryset = ChargingStations.objects.all()
    serializer_class = UserViewEVStations

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ViewSingleEvStation(viewsets.ReadOnlyModelViewSet):
    queryset = ChargingStations.objects.all()
    serializer_class = UserViewEVStations

    def list(self, request, *args, **kwargs):
        ev_station_id = request.query_params.get('id')  # Get station ID from query params
        print("Query parameters received:", request.query_params)

        if not ev_station_id:
            
            return Response(
                {"status": "failed", "message": "EV station ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ev_station = self.queryset.get(id=ev_station_id)  # Fetch station
        except ChargingStations.DoesNotExist:
            return Response(
                {"status": "failed", "message": "No charging station with this ID exists."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(ev_station)  # Serialize with slots
        return Response(serializer.data, status=status.HTTP_200_OK)





class AvailableSlotsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChargingSlot.objects.all()
    serializer_class = ChargingSlotSerializer

    def list(self, request, *args, **kwargs):
        # Get the station_id and optional date from query params
        station_id = request.query_params.get('station_id')
        # date = request.query_params.get('date')  # Optional for filtering
        
        if not station_id:
            return Response({"status": "failed", "message": "Station ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter slots based on the station_id
        slots = self.queryset.filter(station_id=station_id)

        # if date:
        #     # If a date is provided, filter further by the specific date
        #     slots = slots.filter(date=date)

        if not slots.exists():
            return Response({"status": "failed", "message": "No slots available for the given criteria."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the filtered slots
        serializer = self.get_serializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class BookSlotView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        slot_id = request.data.get('slot')
        user_id = request.data.get('user')  # Assume user details are passed in the request
        connector = request.data.get('connector')

        if not slot_id or not user_id:
            return Response({"error": "Slot ID and user are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the slot if it's not already booked
            user = User.objects.get(id=user_id)
            slot = ChargingSlot.objects.get(id=slot_id, is_booked=False)
            rate = float(slot.station.rate_per_slot)
        except ChargingSlot.DoesNotExist:
            return Response({"error": "Slot is already booked or does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Create a booking
        booking = Booking.objects.create(
            slot=slot,
            user=user,
            payment_status="Completed",  # Payment completed as part of booking
            connector = connector,
            amount = rate
        )

        # Mark the slot as booked
        slot.is_booked = True
        slot.save()

        # Serialize the booking details and return the response
        serializer = BookingSerializer(booking)
        return Response(
            {   
                "status": "success",
                "message": "Slot booked successfully.",
                "booking": serializer.data
            },
            status=status.HTTP_200_OK
        )
    

class ChargingStationBookingHistoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChargingStationBookingListSerializer
    queryset = Booking.objects.all()

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        print("Query parameters received:", request.query_params)

        if not user_id:
            return Response(
                {"status": "failed", "message": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        bookings = self.queryset.filter(user_id=user_id)
        
        # if not bookings.exists():
        #     return Response(
        #         {"status": "failed", "message": "No bookings found."},
        #         status=status.HTTP_404_NOT_FOUND
        #     )

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ViewSingleStationBookingView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViewSingleStationBookingSerializer
    queryset = Booking.objects.all()

    def list(self, request, *args, **kwargs):
        booking_id = request.query_params.get('booking_id')
        print("Query parameters received:", request.query_params)

        if not booking_id:
            return Response(
                {"status": "failed", "message": "Booking ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the first (or only) booking object matching the provided booking_id
        booking = self.queryset.filter(id=booking_id).first()

        if not booking:
            return Response(
                {"status": "failed", "message": "No bookings found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartCharging(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = StartChargingSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        booking_id = request.data.get('id')

        if not booking_id:
            return Response(
                {"status": "failed", "message": "booking ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking_id:
            booking = Booking.objects.get(id=booking_id)
        else:
            return Response(
                {"status": "failed", "message": "booking with booking ID doesn't exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = request.data.copy()
        data['charging_status'] =  "Charging Started"

        # Perform partial update with the provided data
        serializer = StartChargingSerializer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Charging started ",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "message": "Invalid Details",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class FinishCharging(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = StartChargingSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        booking_id = request.data.get('id')

        if not booking_id:
            return Response(
                {"status": "failed", "message": "Booking ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Booking with the given ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.charging_status == 'Charging Started':
            data = request.data.copy()
            data['charging_status'] = "Charging Completed"

            slot = booking.slot  # Directly get the slot from the booking
            slot.is_booked = False
            slot.save()

            serializer = StartChargingSerializer(booking, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "message": "Charging Completed"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": "failed", "message": "Invalid Details", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"status": "failed", "message": "Booking is not in 'Charging Started' state."},
            status=status.HTTP_400_BAD_REQUEST
        )