from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.forms import AuthenticationForm
from djangoapp.restapis import get_dealer_reviews_from_cf, get_dealers_from_cf, post_request
from django.contrib.auth.decorators import login_required


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_page(request):
    return render(request, 'djangoapp/index.html')


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        
        else:
            context['error_message'] = 'Invalid username or password'
            return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        # Get user information from request.POST
        username = request.POST.get('username')
        password = request.POST.get('psw')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            context['error_message'] = 'Username already taken'
            return render(request, 'djangoapp/registration.html', context)

        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        
        # Login the user and redirect to a different page (e.g., index)
        login(request, user)
        return redirect("djangoapp:index")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name

        context = {'dealerships': dealerships}

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
from django.http import JsonResponse

def get_dealer_details(request, dealer_id):
    # print(dealer_id)
    if request.method == "GET":
        dealers_url = "http://127.0.0.1:3000/dealerships/get"
        review_url = "http://127.0.0.1:5000/api/get_reviews"
        
        dealer_details = get_dealers_from_cf(url=dealers_url, dealer_id=dealer_id)
        dealer_reviews = get_dealer_reviews_from_cf(url=review_url, dealer_id=dealer_id)


        if dealer_details:
            context = {'dealer_details': dealer_details, "dealer_reviews": dealer_reviews}
            return render(request, 'djangoapp/dealer_details.html', context)
        else:
            return JsonResponse({"error": "Dealer details not found"}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        review_payload = {
            "id": dealer_id,
            "name": request.POST.get('name'),
            "dealership": request.POST.get('dealer_label'),
            "review": request.POST.get('review'),
            "purchase": request.POST.get('purchase'),
            "purchase_date": request.POST.get('purchase_date'),
            "car_make": request.POST.get('car_make'),
            "car_model": request.POST.get('car_model'),
            "car_year": request.POST.get('car_year')
        }

        url = "http://127.0.0.1:5000/api/post_review"

        try: 
            response = post_request(url, json_payload=review_payload)
            if response and response.get('success'):
                            return redirect('success_page')  # Redirect to a success page
            else:
                return HttpResponse("Failed to submit review", status=500)
        except Exception as e:
            # Handle any errors that occur during the request
            print("Error occurred:", e)
            return HttpResponse("An error occurred while submitting the review", status=500)

    else:
        # Handle GET requests (you might want to redirect or render a form)
        return HttpResponse("GET requests are not supported for this endpoint", status=405)
# ...

