from django.shortcuts import render,redirect,get_object_or_404
from service_app.models import *
from django.contrib import messages
from .models import *
from django.utils.timezone import now
from django.db.models import Count
# Create your views here.


def index(request):
    return render (request,'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username=='admin' and password == 'admin':
            return redirect ('admin_index')
    return render(request,'login.html')
# def admin_view_approved_service_centre(request):
#     service_centre = Service_Centre.objects.filter(status='approved')
#     return redirect(request,'index.html',{'service_centre':service_centre})

# def admin_view_rejected_service_centre(request):
#     service_centre = Service_Centre.objects.filter(status='rejected')
#     return redirect(request,'index.html',{'service_centre':service_centre})

# def admin_view_approved_service_centre(request):
#     service_centre = Service_Centre.objects.filter(status='pending')
#     return redirect(request,'index.html',{'service_centre':service_centre})

# def approve_service_centre(request):
#     service_centre_id = request.GET.get('id')
#     service_centre = Service_Centre.objects.get(id=service_centre_id)
#     service_centre.status = 'approved'
#     service_centre.save()
#     return redirect(request,'index.html')

# def reject_service_centre(request):
#     service_centre_id = request.GET.get('id')
#     service_centre = Service_Centre.objects.get(id=service_centre_id)
#     service_centre.status = 'reject'
#     service_centre.save()
#     return redirect(request,'index.html')

# 1. List all service centers
def list_service_centres(request):
    service_centres = Service_Centre.objects.filter(status='pending')
    return render(request, 'admin/list_service_centres.html', {'service_centres': service_centres})

def approved_centres(request):
    service_centres = Service_Centre.objects.filter(status='approved')
    return render(request, 'admin/approved_centres.html', {'service_centres': service_centres})

def rejected_centres(request):
    service_centres = Service_Centre.objects.filter(status='rejected')
    return render(request, 'admin/rejected_centres.html', {'service_centres': service_centres})
    
# 2. View details of a specific service center
def service_centre_details(request, centre_id):
    service_centre = get_object_or_404(Service_Centre, id=centre_id)
    return render(request, 'admin/service_centre_details.html', {'service_centre': service_centre})

# 3. List the products sold by a specific service center
def list_service_centre_products(request, centre_id):
    service_centre = get_object_or_404(Service_Centre, id=centre_id)
    products = Products.objects.filter(service_centre=service_centre)
    return render(request, 'admin/list_service_centre_products.html', {
        'service_centre': service_centre,
        'products': products,
    })

# 4. View the list of employees in a specific service center
def list_service_centre_employees(request, centre_id):
    service_centre = get_object_or_404(Service_Centre, id=centre_id)
    employees = Employee.objects.filter(service_centre=service_centre)
    return render(request, 'admin/list_service_centre_employees.html', {
        'service_centre': service_centre,
        'employees': employees,
    })

# 5. View details of a specific employee
def employee_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'admin/employee_details.html', {'employee': employee})

def approve_or_reject_service_centre(request, centre_id, action):
    service_centre = get_object_or_404(Service_Centre, id=centre_id)

    if action == "approve":
        service_centre.status = "approved"
        messages.success(request, f"Service Centre '{service_centre.name}' has been approved.")
    elif action == "reject":
        service_centre.status = "rejected"
        messages.error(request, f"Service Centre '{service_centre.name}' has been rejected.")
    else:
        messages.warning(request, "Invalid action specified.")
        return redirect('list_service_centres')  # Redirect to the service centres list

    service_centre.save()
    return redirect('list_service_centres')


def adminindex(request):
    return render(request,'admin/admin_index.html')


def add_ev_station(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        working_hours = request.POST.get('working_hours')
        
        # Convert connectors to a list (assuming input is comma-separated)
        connectors = request.POST.get('connectors', '').split(',')
        
        rate_per_min = request.POST.get('rate_per_min')
        capacity = request.POST.get('capacity')

        # Save the data to the model
        ChargingStations(
            name=name,
            image=image,
            address=address,
            working_hours=working_hours,
            connectors=connectors,  # List stored in JSONField
            rate_per_slot=rate_per_min,
            capacity=capacity
        ).save()

        return redirect('admin_index')

    return render(request, 'admin/add_station.html')



from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

@receiver(post_save, sender=ChargingStations)
def generate_slots(sender, instance, created, **kwargs):
    if created:
        print(f"Charging station created: {instance.name}")  # Debugging line
        try:
            start_time, end_time = instance.working_hours.split('-')
            start_time = start_time.strip()
            end_time = end_time.strip()

            # Fix 24:00 issue
            if end_time == "24:00":
                end_time = "23:59"

            start_time = datetime.strptime(start_time, '%H:%M')
            end_time = datetime.strptime(end_time, '%H:%M')
            
            print(f"Working hours format: {instance.working_hours}") 

            if end_time <= start_time:
                raise ValueError("End time must be after start time")

            current_time = start_time
            while current_time + timedelta(hours=1) <= end_time:
                ChargingSlot.objects.create(
                    station=instance,
                    start_time=current_time.time(),
                    end_time=(current_time + timedelta(hours=1)).time(),
                    is_booked=False
                )
                current_time += timedelta(hours=1)

        except ValueError as e:
            print(f"Error in working hours format: {e}")



def list_ev_stations(request):
    ev_stations = ChargingStations.objects.all()
    return render(request, 'admin/list_ev_stations.html', {'ev_stations': ev_stations})

def ev_station_details(request, station_id):
    ev_station = get_object_or_404(ChargingStations, id=station_id)
    return render(request, 'admin/ev_station_details.html', {'ev_station': ev_station})



def station_booking_count(request):
    today = now().date()
    station_counts = ChargingStations.objects.annotate(
        today_bookings=Count('slots__booking', filter=models.Q(slots__booking__booking_date=today))
    )

    return render(request, 'admin/station_booking_count.html', {'station_counts': station_counts})