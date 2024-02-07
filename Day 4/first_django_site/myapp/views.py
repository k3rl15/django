from django.http import HttpResponse, JsonResponse
from .models import Profile
import json
from django.views.decorators.csrf import csrf_exempt


def welcome(request):
    return HttpResponse("This is how to customize Welcome page into plain boring one.")


def hello_world(request):
    return HttpResponse("Hello World!")


@csrf_exempt
def profile_view(request):
    """
        Description:
        Creates a new profile with the provided information.
        Get the list of profiles already created.

        Parameters:

        POST:
        name (str): The name of the profile.
        email (str): The email address of the profile.
        mobile_number (str): The mobile number of the profile.
        address (str): The address of the profile.

        GET: None
    """
    print("Received request:", request.method, request.POST)
    if request.method == 'GET':
        profiles = Profile.objects.all()
        data = [{'id': profile.id, 'name': profile.name, 'email': profile.email, 'address': profile.address,
                 'mobile number': profile.mobile_number} for profile in profiles]
        json_data = json.dumps(data, indent=2)
        return HttpResponse(json_data, content_type='application/json', status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        # Extract fields from JSON data
        name = data.get('name')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        address = data.get('address')

        if not name or not email:
            return JsonResponse({'message': 'Name and email are required fields'}, status=400)

        profile = Profile(name=name, email=email, address=address, mobile_number=mobile_number)
        profile.save()

        profile_data = Profile.objects.get(name=name)
        data = {'id': profile_data.id, 'name': profile_data.name, 'email': profile_data.email, 'address': profile_data.address,
                'mobile_number': profile_data.mobile_number}
        return HttpResponse(json.dumps({'message': 'Profile created successfully', 'data': data}),
                            content_type='application/json', status=201)
    else:
        return HttpResponse(json.dumps({'message': 'Method not allowed'}), status=405, content_type='application/json')


@csrf_exempt
def profile_detail_view(request, pk):
    """
    Description:
    Get the details of a specific profile by ID.
    Update the name or email of the profile.
    Delete the profile by ID.

    Parameters:

    GET:
    pk (int): The primary key of the profile.

    PUT:
    pk (int): The primary key of the profile.
    name (str): The updated name of the profile.
    email (str): The updated email address of the profile.

    DELETE:
    pk (int): The primary key of the profile.
    """
    try:
        profile = Profile.objects.get(id=pk)
    except Profile.DoesNotExist:
        return JsonResponse({'message': 'Profile not found'}, status=404)

    if request.method == 'GET':
        data = {'id': profile.id, 'name': profile.name, 'email': profile.email, 'mobile_number': profile.mobile_number,
                'address': profile.address}
        json_data = json.dumps(data, indent=2)
        return HttpResponse(json_data, content_type='application/json', status=200)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        name = data.get('name')
        email = data.get('email')

        # Update name and email
        if not name and not email:
            return JsonResponse({'message': 'At least one field (name or email) is required to update'}, status=400)
        if name:
            profile.name = name
        if email:
            profile.email = email
        profile.save()

        updated_profile = Profile.objects.get(id=pk)
        updated_data = {'id': updated_profile.id, 'name': updated_profile.name, 'email': updated_profile.email}

        return HttpResponse(json.dumps({'message': 'Profile updated successfully', 'data': updated_data}),
                            content_type='application/json', status=200)
    elif request.method == 'DELETE':
        profile.delete()
        return JsonResponse({'message': 'Profile deleted successfully'}, status=204)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


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


@csrf_exempt
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
