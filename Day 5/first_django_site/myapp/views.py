from django.http import HttpResponse
from .models import Profile, Product
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder


def welcome(request):
    """
    Welcome view.
    """
    return HttpResponse("This is how to customize the Welcome page into a plain boring one.")


def hello_world(request):
    """
    Hello World view.
    """
    return HttpResponse("Hello World!")


@csrf_exempt
def profile_view(request):
    """
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
            return HttpResponse(json.dumps({'message': 'Invalid JSON data'}), status=400,
                                content_type='application/json')

        # Extract fields from JSON data
        name = data.get('name')
        email = data.get('email')
        mobile_number = data.get('mobile_number')
        address = data.get('address')

        if not name or not email:
            return HttpResponse(json.dumps({'message': 'Name and email are required fields'}), status=400,
                                content_type='application/json')

        profile = Profile(name=name, email=email, address=address, mobile_number=mobile_number)
        profile.save()

        profile_data = Profile.objects.get(name=name)
        data = {'id': profile_data.id, 'name': profile_data.name, 'email': profile_data.email,
                'address': profile_data.address,
                'mobile_number': profile_data.mobile_number}
        return HttpResponse(json.dumps({'message': 'Profile created successfully', 'data': data}),
                            content_type='application/json', status=201)
    else:
        return HttpResponse(json.dumps({'message': 'Method not allowed'}), status=405, content_type='application/json')


@csrf_exempt
def profile_detail_view(request, pk):
    """
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
        return HttpResponse(json.dumps({'message': 'Profile not found'}), status=404, content_type='application/json')

    if request.method == 'GET':
        data = {'id': profile.id, 'name': profile.name, 'email': profile.email, 'mobile_number': profile.mobile_number,
                'address': profile.address}
        json_data = json.dumps(data, indent=2)
        return HttpResponse(json_data, content_type='application/json', status=200)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(json.dumps({'message': 'Invalid JSON data'}), status=400,
                                content_type='application/json')

        name = data.get('name')
        email = data.get('email')

        # Update name and email
        if not name and not email:
            json_data = json.dumps({'message': 'At least one field (name or email) is required to update'}, indent=2)
            return HttpResponse(json_data, status=400, content_type='application/json')
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
        json_data = json.dumps({'message': 'Profile deleted successfully'}, indent=2)
        return HttpResponse(json_data, status=204, content_type='application/json')
    else:
        json_data = json.dumps({'message': 'Method not allowed'}, indent=2)
        return HttpResponse(json_data, status=405, content_type='application/json')


def get_profile_by_name(request, name):
    """
    Get profile details by name.

    Parameters:
    name (str): The name of the profile.
    """
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
        json_data = json.dumps({'Error': 'Profile not found'}, indent=2)
        return HttpResponse(json_data, status=404, content_type='application/json')


@csrf_exempt
def update_email(request, name):
    """
    Update email for a profile.

    Parameters:
    name (str): The name of the profile.
    """
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
            json_data = json.dumps({
                'success': False,
                'message': 'Profile not found.'}, indent=2)
            return HttpResponse(json_data, status=404, content_type='application/json')

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
        json_data = json.dumps({
            'success': False,
            'message': 'Invalid JSON data in the request body.'}, indent=2)
        return HttpResponse(json_data, status=400, content_type='application/json')


@csrf_exempt
def product_view(request):
    """
    Get the list of products or create a new product.

    Parameters:

    GET: None

    POST:
    name (str): The name of the product.
    price (float): The price of the product.
    description (str): The description of the product.
    category (str): The category of the product.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                 'description': product.description,
                 'category': product.category, 'created_at': (product.created_at - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')}
                for product in products]
        json_data = json.dumps(data, indent=2, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type='application/json')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = json.dumps({'message': 'Invalid JSON data'}, indent=2)
            return HttpResponse(json_data, status=400, content_type='application/json')

        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        category = data.get('category')

        if not name and not price:
            json_data = json.dumps({'message': 'Name and Price are required fields'}, indent=2)
            return HttpResponse(json_data, status=400, content_type='application/json')

        product = Product(name=name, price=price, description=description, category=category)
        product.save()
        product_data = {'id': product.id, 'name': product.name, 'price': float(product.price),
                        'description': product.description,
                        'category': product.category, 'created_at': (product.created_at - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')}
        return HttpResponse(json.dumps({'message': 'Product created successfully', 'data': product_data}),
                            content_type='application/json', status=201, cls=DjangoJSONEncoder)
    else:
        return HttpResponse(json.dumps({'message': 'Method not allowed'}), status=405, content_type='application/json')


@csrf_exempt
def product_detail_view(request, pk):
    """
    Get, update, or delete a specific product by ID.

    Parameters:

    GET:
    pk (int): The primary key of the product.

    PUT:
    pk (int): The primary key of the product.
    name (str): The updated name of the product.
    price (float): The updated price of the product.
    description (str): The updated description of the product.
    category (str): The updated category of the product.

    DELETE:
    pk (int): The primary key of the product.
    """
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        json_data = json.dumps({'message': 'Product not found'}, indent=2)
        return HttpResponse(json_data, status=404, content_type='application/json')

    if request.method == 'GET':
        product_data = {'id': product.id, 'name': product.name, 'price': float(product.price),
                        'description': product.description,
                        'category': product.category, 'created_at': (product.created_at - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')}
        json_data = json.dumps(product_data, indent=2, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type='application/json', status=200)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = json.dumps({'message': 'Invalid JSON data'}, indent=2)
            return HttpResponse(json_data, status=400, content_type='application/json')

        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        category = data.get('category')

        # Update product fields
        product.name = name or product.name
        product.price = price or product.price
        product.description = description or product.description
        product.category = category or product.category

        # ORM Query: Save the updated product
        product.save()
        updated_product_data = {'id': product.id, 'name': product.name, 'price': float(product.price),
                                'description': product.description, 'category': product.category,
                                'created_at': (product.created_at - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M')}
        return HttpResponse(json.dumps({'message': 'Product updated successfully', 'data': updated_product_data}),
                            content_type='application/json', status=200)
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(json.dumps({'message': 'Product deleted successfully'}, status=204,
                                       content_type='application/json'))
    else:
        return HttpResponse(json.dumps({'message': 'Method not allowed'}), status=405, content_type='application/json')


@csrf_exempt
def products_by_price_desc(request):
    """
    Get a list of products ordered by price in descending order.
    """
    price_desc_products = Product.objects.order_by('-price')
    if price_desc_products:
        product_data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                         'category': product.category, 'description': product.description}
                        for product in price_desc_products]
        json_data = json.dumps(product_data, indent=2)
        return HttpResponse(json_data, status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'No Product Found'}), status=404, content_type='application/json')


@csrf_exempt
def products_in_price_range(request, min_price, max_price):
    """
    Get a list of products within a specified price range.

    Parameters:
    min_price (float): The minimum price of the products.
    max_price (float): The maximum price of the products.
    """
    price_range_products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    if price_range_products:
        product_data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                         'category': product.category, 'description': product.description}
                        for product in price_range_products]
        json_data = json.dumps(product_data, indent=2)
        return HttpResponse(json_data, status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'No Product Found'}),  status=404, content_type='application/json')


@csrf_exempt
def products_recently_added(request):
    """
    Get a list of products added in the last seven days.
    """
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_products = Product.objects.filter(created_at__gte=seven_days_ago)
    if recent_products:
        product_data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                         'category': product.category, 'description': product.description}
                        for product in recent_products]
        json_data = json.dumps(product_data, indent=2)
        return HttpResponse(json_data, status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'No Product Found'}),  status=404, content_type='application/json')


@csrf_exempt
def products_by_keyword(request, keyword):
    """
    Get a list of products containing a specified keyword in their name.

    Parameters:
    keyword (str): The keyword to search for in product names.
    """
    keyword_products = Product.objects.filter(name__icontains=keyword)
    if keyword_products:
        product_data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                         'category': product.category, 'description': product.description}
                        for product in keyword_products]
        json_data = json.dumps(product_data, indent=2)
        return HttpResponse(json_data, status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': f'No Product Found with keyword: {keyword}'}),
                            status=404, content_type='application/json')


@csrf_exempt
def products_by_category(request, category):
    """
    Get a list of products belonging to a specific category.

    Parameters:
    category (str): The category to filter products.

    GET: None
    """
    category_products = Product.objects.filter(category__iexact=category)
    if category_products:
        product_data = [{'id': product.id, 'name': product.name, 'price': float(product.price),
                         'category': product.category, 'description': product.description}
                        for product in category_products]
        json_data = json.dumps(product_data, indent=2, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': f'No Product Found in category: {category}'}),
                            status=404, content_type='application/json')
