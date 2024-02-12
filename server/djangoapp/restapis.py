import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    try:
        dealer_id = kwargs.get('dealer_id')
        response = requests.get(url, params={'id': dealer_id}, headers={'Content-Type': 'application/json'},)
        # print(response.text)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        json_data = response.json()  # Extract JSON data from the response
        return json_data
    except requests.exceptions.RequestException as e:
        # If any error occurs during the request
        print("Error occurred during POST request:", e)
        return None


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    dealer_id = kwargs.get('dealer_id')
    # Call get_request with a URL parameter
    if dealer_id:
        json_result = get_request(url, dealer_id=dealer_id)
        # print(json_result)
    else:
        json_result = get_request(url)
        # print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    # print(dealer_id)
    results = []
    json_result = get_request(url, dealer_id=dealer_id)
    

    if json_result:
        reviews = json_result
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(
                dealership=review_doc['dealership'],
                name=review_doc['name'],
                purchase=review_doc['purchase'],
                review=review_doc['review'],
                purchase_date=review_doc['purchase_date'],
                car_make=review_doc['car_make'],
                car_model=review_doc['car_model'],
                car_year=review_doc['car_year'],
                id=review_doc['id'],
                sentiment=""
            )
            
            review_obj.sentiment = analyze_review_sentiments(review_doc['review'])
            # print(review_obj.sentiment)

            results.append(review_obj)
    return results



# Base URL of the NLU service
NLU_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/8d7937e6-4159-462e-b729-d5133682b024/v1/analyze"

# IAM API Key
IAM_API_KEY = "XA0pY-hVA-ctqzqwbYg02nezhfgWeZCz4GTA87mRNKZ7"

# Function to analyze review sentiments
def analyze_review_sentiments(text):
    # print("parameter = " + text)
    # Parameters for the NLU service
    params = {
        "text": text,
        "version": "2022-04-07",
        "features": {
            "sentiment": {},
        },
    }

    # Make the API request
    response = requests.get(NLU_URL, params=params, auth=("apikey", IAM_API_KEY))

    # Check the response status
    if response.status_code == 200:
        # Parse the JSON response
        json_result = response.json()
        
        # Extract sentiment label
        sentiment_label = json_result.get('sentiment', {}).get('document', {}).get('label')
        # print(sentiment_label)
        return sentiment_label
    else:
        # If request fails, return None or handle the error as needed
        return None







