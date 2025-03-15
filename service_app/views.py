from django.utils import timezone
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from user_app.models import *
from django.utils.timezone import now
# Create your views here.

class ServiceCentreRegistrationView(viewsets.ModelViewSet):
    queryset = Service_Centre.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ServiceCentreRegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Service Centre created successfully"
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
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            try:
                owner = Service_Centre.objects.get(username=username,status='approved')
                if password == owner.password: 
                    response_data = {
                        "status": "success",
                        "message": "Owner logged in successfully",
                        "utype": owner.utype,
                        "service_centre_id": owner.id,
                        "employee_id": None
                    }
                    request.session['id'] = owner.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials or admin haven,t approved your account"}, status=status.HTTP_401_UNAUTHORIZED)
            except Service_Centre.DoesNotExist:
                pass

            try:
                employee = Employee.objects.get(username=username)
                if password == employee.password: 
                    response_data = {
                        "status": "success",
                        "message": "Employee logged in successfully",
                        "utype": employee.utype,
                        "employee_id": employee.id,
                        "service_centre_id": None
                    }
                    request.session['id'] = employee.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Employee.DoesNotExist:
                pass

            return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "failed", "message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)


class AddEmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer  # Fix the attribute name
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        service_center_id = request.data.get('service_centre') # Get parent ID from session
        
        # Add parent ID to the request data
        data = request.data.copy()
        data['service_centre'] = service_center_id 


        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Employee created successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class UpdateEmployeeView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['patch']
    
    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates to an Employee object.
        """
        employee_id = request.data.get('id')
        try:
            employee = Employee.objects.get(id=employee_id)  # Retrieve the Employee object
        except Employee.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Perform partial update with the provided data
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Employee updated successfully",
                    "data": serializer.data,
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
        

class UpdateServiceCentreView(generics.UpdateAPIView):
    queryset = Service_Centre.objects.all()
    serializer_class = ServiceCentreRegisterSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates to a Service Centre object.
        """
        service_id = request.data.get('id')
        try:
            service_centre = Service_Centre.objects.get(id=service_id)  
        except Service_Centre.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Service centre not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ensure the image is correctly retrieved from request.FILES
        data = request.data.copy()  # Make a mutable copy of request data
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']

        serializer = ServiceCentreRegisterSerializer(service_centre, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Service centre updated successfully",
                    "data": serializer.data,
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
        

from rest_framework.parsers import MultiPartParser, FormParser

class AddProducts(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['post']
    # parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        service_center_id = request.data.get('service_centre') 
        
        # Add parent ID to the request data
        data = request.data.copy()
        data['service_centre'] = service_center_id 

        print(data)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Product added successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['patch']
    
    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates to an Employee object.
        """
        product_id = request.data.get('product_id')
        quan = request.data.get('quantity')
        try:
            product = Products.objects.get(id=product_id)  # Retrieve the Employee object
        except Products.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data.copy()
           
        if quan:
            data['quantity'] =  str(int(data['quantity'])+int(product.quantity))

        print(data)

        # Perform partial update with the provided data
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Product updated successfully",
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
            

# class DeleteProductView(generics.DestroyAPIView):
#     queryset = Products.objects.all()


class ViewProducts(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ViewProductSerializer

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
    serializer_class = ProductSerializer
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

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewPurchsedProducts(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseProduct.objects.all()
    serializer_class = ViewPurchasedProductSerializer

    def list(self, request, *args, **kwargs):
        # Extract 'service_centre' from query parameters
        service_centre_id = request.query_params.get('service_centre')
        print("Query parameters received:", request.query_params)

        if service_centre_id:
            # Filter products by the provided service_centre_id
            products = self.queryset.filter(service_centre_id=service_centre_id)
        else:
            # Return an error response if 'service_centre' is not provided
            response_data = {
                "status": "failed",
                "message": "Service Centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewRepairRequestView(viewsets.ReadOnlyModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = ViewRepairRequestSerializer

    def list(self, request, *args, **kwargs):
        sc_id = request.query_params.get('service_centre')

        if sc_id:
            repairs = Repair.objects.filter(service_centre_id = sc_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Service Centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(repairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewSingleRepairView(viewsets.ModelViewSet):
    serializer_class = ViewSingleRepairSerializer
    queryset = Repair.objects.all()

    def list(self, request, *args, **kwargs):
        repair_id = request.query_params.get('repair')
        print("Query parameters received:", request.query_params)

        if not repair_id:
            response_data = {
                "status": "failed",
                "message": "Repair ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            repair = Repair.objects.get(id=repair_id)
            print("Product found:", repair)
        except Repair.DoesNotExist:
            print("request with ID", repair_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "Requestt does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = ViewSingleRepairSerializer(repair)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ViewINEmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = ViewEmployeeSerializer

    def list(self, request, *args, **kwargs):
        # Retrieve the service_centre_id from the request body
        service_centre_id = request.query_params.get('service_centre')
        print("Query parameters received:", request.query_params)

        if service_centre_id:
            # Filter products by the provided service_centre_id
            employees = self.queryset.filter(service_centre_id=service_centre_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Service Centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ViewAllEmployees(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = ViewAllEmployeeSerializer

    def list(self, request, *args, **kwargs):
        # Extract 'service_centre' from query parameters
        service_centre_id = request.query_params.get('service_centre')
        print("Query parameters received:", request.query_params)

        if service_centre_id:
            # Filter products by the provided service_centre_id
            employees = self.queryset.filter(service_centre_id=service_centre_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Service Centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignEmployeeView(generics.UpdateAPIView):
    queryset = Repair.objects.all()
    serializer_class = AssignEmployeeSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        repair_id = request.data.get('id')
        try:
            repair = Repair.objects.get(id=repair_id)  # Retrieve the Employee object
        except Employee.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Repair request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data.copy()
        data['status'] =  "Mechanic Assigned"

        # Perform partial update with the provided data
        serializer = AssignEmployeeSerializer(repair, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Employee assigned successfully",
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
        

class EmployeeViewAssignedRepairView(viewsets.ReadOnlyModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = EmployeeViewAssignedRepairSerializer

    def list(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee')

        if employee_id:
            repairs = Repair.objects.filter(employee_id = employee_id)
        else:
            # If no service_centre_id is provided, return all products
            response_data = {
                "status": "failed",
                "message": "Employee ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # if not repairs:
        #     response_data = {
        #         "status": "failed",
        #         "message": "No repairs assigned."
        #     }
        #     return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Serialize the filtered queryset
        serializer = self.get_serializer(repairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeUpdateStatusView(generics.UpdateAPIView):
    queryset = Repair.objects.all()
    serializer_class = EmployeeUpdateStatusSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        repair_id = request.data.get('repair')
        employee_id = request.data.get('employee')
        print("Repair ID:", repair_id)
        print("Employee ID:", employee_id)
        try:
            repair = Repair.objects.get(id=repair_id,employee_id=employee_id)  # Retrieve the Employee object
        except Repair.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Repair request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data.copy()
        data['status'] =  "Repair Completed"

        # Perform partial update with the provided data
        serializer = EmployeeUpdateStatusSerializer(repair, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Repair completed successfully",
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
        

class EmployeeViewProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer

    def list(self, request, *args, **kwargs):
        employee_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if not employee_id:
            response_data = {
                "status": "failed",
                "message": "Employee ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(id=employee_id)
            print("user found:", employee)
        except Employee.DoesNotExist:
            print("employee with ID", employee_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "Employee does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeProfileSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceViewProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = ServicViewProfileSerializer

    def list(self, request, *args, **kwargs):
        service_centre_id = request.query_params.get('id')
        print("Query parameters received:", request.query_params)

        if not service_centre_id:
            response_data = {
                "status": "failed",
                "message": "Service centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_centre = Service_Centre.objects.get(id=service_centre_id)
            print("user found:", service_centre)
        except Employee.DoesNotExist:
            print("service_centre with ID", service_centre_id, "does not exist in the database.")
            response_data = {
                "status": "failed",
                "message": "service centre does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = ServicViewProfileSerializer(service_centre)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceViewFeedback(viewsets.ReadOnlyModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = ViewFeedbackSerializer

    def list(self, request, *args, **kwargs):
        service_centre = request.query_params.get('id')

        if not service_centre:
            response_data = {
                "status": "failed",
                "message": "Service centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            feedbacks = Feedback.objects.filter(service_centre_id=service_centre)
        except Feedback.DoesNotExist:
            print("no feedbacks available.")
            response_data = {
                "status": "failed",
                "message": "feedback does not exist."
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeAttendance(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = EmployeeAttendanceSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee')

        if employee_id:
            employee = Employee.objects.get(id=employee_id)

        print(employee)

        today = timezone.now().date()
        if Attendance.objects.filter(employee_id=employee.id, date=today).exists():
            return Response(
                {
                    "status": "failed",
                    "message": "Attendance already marked for today.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data['status'] = "Present"
        data['service_centre'] = employee.service_centre_id


        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Attendance marked successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

class ViewPresentEmployeesView(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = PresentEmployeeSerializer

    def list(self, request, *args, **kwargs):
        service_centre_id = request.query_params.get('service_centre')
        today = now().date()
        print("Query parameters received:", request.query_params)

        if not service_centre_id:
            return Response({"status": "failed", "message": "Service Centre ID is required."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        present_employee_ids = Attendance.objects.filter(
            service_centre_id=service_centre_id, date=today, status="Present"
        ).values_list('employee_id', flat=True)

        employees = Employee.objects.filter(id__in=present_employee_ids)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AttendanceListView(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = AttendanceListSerializer

    def list(self, request, *args, **kwargs):
        service_centre_id = request.query_params.get('service_centre')
        today = now().date()
        print("Query parameters received:", request.query_params)

        if not service_centre_id:
            return Response({"status": "failed", 
                             "message": "Service Centre ID is required."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Get all employees in the service centre
        employees = Employee.objects.filter(service_centre_id=service_centre_id)

        # Get attendance records for today
        attendance_records = Attendance.objects.filter(service_centre_id=service_centre_id, date=today)

        # Create a dictionary of employee_id -> status (Present)
        attendance_dict = {att.employee_id: att.status for att in attendance_records}

        # Serialize employees and add the status field
        serialized_data = []
        for emp in employees:
            serialized_data.append({
                "id": emp.id,
                "name": emp.name,
                "status": attendance_dict.get(emp.id, "Absent")  # Default to Absent if not found in attendance
            })

        return Response(serialized_data, status=status.HTTP_200_OK)



class ApproveLeaveView(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = ApproveLeaveSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee')
        # service_centre_id = request.data.get('service_centre')

        if not employee_id:
            response_data = {
                "status": "failed",
                "message": "Employee ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if employee_id:
            employee = Employee.objects.get(id=employee_id)

        print(employee)

        today = timezone.now().date()
        if Attendance.objects.filter(employee_id=employee.id, date=today).exists():
            return Response(
                {
                    "status": "failed",
                    "message": "Attendance already marked for today.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data['status'] = "Leave Approved"
        data['service_centre'] = employee.service_centre_id

        
        serializer = ApproveLeaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Leave Approved",
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



class RejectLeaveView(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = RejectLeaveSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee')

        if not employee_id:
            response_data = {
                "status": "failed",
                "message": "Employee ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        if employee_id:
            employee = Employee.objects.get(id=employee_id)

        print(employee)

        today = timezone.now().date()
        if Attendance.objects.filter(employee_id=employee.id, date=today).exists():
            return Response(
                {
                    "status": "failed",
                    "message": "Attendance already marked for today.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data['status'] = "Leave Rejected"
        data['service_centre'] = employee.service_centre_id

        
        serializer = RejectLeaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Leave rejected",
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


class EmployeeCountView(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()

    def list(self, request, *args, **kwargs):
        service_centre_id = request.query_params.get('service_centre')

        if not service_centre_id:
            response_data = {
                "status": "failed",
                "message": "Service centre ID is required."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        count = Employee.objects.filter(service_centre=service_centre_id).count()
        
        # Return the count in a custom response format
        response_data = {
            "status": "success",
            "service_centre_id": int(service_centre_id),
            "employee_count": count
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


class EmployeeCheckAttendanceView(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()

    def list(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee')

        date = now().date()
        
        is_present = Attendance.objects.filter(employee_id=employee_id, date=date).exists()
        response_data = {
            "attendance": is_present,
            "employee_id": int(employee_id),
        }
        return Response(response_data, status=status.HTTP_200_OK)