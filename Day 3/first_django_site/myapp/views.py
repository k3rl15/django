from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Profile
import json
# from django.views.decorators.csrf import csrf_exempt --> testing purposes


def welcome(request):
    return HttpResponse("This is how to customize Welcome page into plain boring one.")


def hello_world(request):
    return HttpResponse("Hello World!")


def profile_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        mobile_number = request.POST.get('mobile_number', '')
        Profile.objects.create(name=name, email=email, address=address, mobile_number=mobile_number)
        return redirect('profile')
    else:
        stored_names = Profile.objects.all()
        context = {'stored_names': stored_names}
        return render(request, 'profile.html', context)


def get_profile_by_name(request, name):
    try:
        profile = Profile.objects.get(name=name)
        data = {
            'Name': profile.name,
            'Email': profile.email,
            'Address': profile.address,
            'Mobile Number': profile.mobile_number,
        }
        json_data = json.dumps(data, indent=2)

        return HttpResponse(json_data, content_type='application/json')
    except Profile.DoesNotExist:
        response_data = {
            'Error': 'Profile not found',
        }
        return JsonResponse(response_data, status=404)


# @csrf_exempt --> testing purposes
def update_email(request, name):
    try:
        data = json.loads(request.body)

        # Validate that 'email' is present in the request data
        if 'email' not in data:
            response_data = {
                'success': False,
                'message': 'Email is required in the request body.',
            }
            json_data = json.dumps(response_data, indent=2)

            return HttpResponse(json_data, content_type='application/json')

        new_email = data['email']

        # Additional validation if needed (e.g., validate email format)
        try:
            Profile.objects.get(name=name)
        except Profile.DoesNotExist:
            response_data = {
                'success': False,
                'message': 'Profile not found.',
            }
            return JsonResponse(response_data, status=404)

        # Update email in the database
        profile = Profile.objects.get(name=name)
        profile.email = new_email
        profile.save()

        data = {
            'success': True,
            'message': 'Email updated successfully.',
            'profile': {
                'name': profile.name,
                'email': profile.email,
                'address': profile.address,
                'mobile_number': profile.mobile_number,
                }
            }
        json_data = json.dumps(data, indent=2)

        return HttpResponse(json_data, content_type='application/json')

    except json.JSONDecodeError:
        response_data = {
            'success': False,
            'message': 'Invalid JSON data in the request body.',
        }
        return JsonResponse(response_data, status=400)
