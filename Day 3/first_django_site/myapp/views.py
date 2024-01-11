from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Profile
import json


def welcome(request):
    return HttpResponse("This is how to customize Welcome page into plain boring one.")


def hello_world(request):
    return HttpResponse("Hello World!")


def get_profile_by_name(request, name):
    profile = get_object_or_404(Profile, name=name)
    data = {
        'name': profile.name,
        'email': profile.email,
        'address': profile.address,
        'mobile_number': profile.mobile_number,
    }

    json_data = json.dumps(data, indent=2)

    response = HttpResponse(json_data, content_type="application/json")

    return response


@require_POST
def update_email(request, name):
    try:
        data = json.loads(request.body)
        new_email = data['email']

        profile = Profile.objects.get(name=name)
        profile.email = new_email
        profile.save()

        response_data = {
            'success': True,
            'message': 'Email updated successfully.',
        }
        json_data = json.dumps(response_data, indent=2)
        return HttpResponse(json_data, content_type='application/json')
    except KeyError:
        response_data = {
            'success': False,
            'message': 'Invalid data. Please provide an email address.',
        }
        json_data = json.dumps(response_data, indent=2)
        return HttpResponse(json_data, content_type='application/json', status=400)
