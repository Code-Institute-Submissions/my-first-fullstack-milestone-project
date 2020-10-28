from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Appointment
from profiles.models import UserProfile

from .forms import AppointmentForm

# Create your views here
def display_appointments(request):

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

    # get the user info first
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # to then get the user's past appointments
    appointments = user_profile.appointments.all()

    template = 'appointments/display_appointments.html'

    context = {
        'appointments': appointments,
    }

    return render(request, template, context,)


def display_appointment_detail(request, appointment_id):

    appointment = get_object_or_404(Appointment, pk=appointment_id)

    template = 'appointments/appointment_detail.html'

    context = {
        "appointment": appointment,
    }

    return render(request, template, context)



# add a new appointment
def add_appointment(request):

    if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            # Attach the user's profile to the apointment

    if request.method == "POST":
        #  instance of the ProductProfileForm based
        #  on the request date from POST
        appointment_form_data = AppointmentForm(request.POST)
        if appointment_form_data.is_valid():
            appointment = appointment_form_data.save()
            messages.success(request, 'Appointment Saved Successfully!')
            return redirect(reverse('display_appointment_detail',
                            args=[appointment.id]))
        else:
            messages.error(request,
                           'Failed to save apointment.'
                           'Please ensure the form is correclty filled.')
    else:
        appointment_form_data = AppointmentForm()

    context = {
        'appointment_form_data': appointment_form_data,
    }

    template = 'appointments/add_appointment.html'

    return render(request, template, context)
