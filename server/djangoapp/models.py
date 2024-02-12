from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    CAR_TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.car_make.name})"

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
    

class DealerReview():
    def __init__(self, car_make, car_model, car_year, dealership, name, purchase, review, sentiment, id, purchase_date=None):
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Dealership id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Purchase status
        self.purchase = purchase
        # Purchase date
        self.purchase_date = purchase_date
        # Review text
        self.review = review
        # Sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return f"{self.name} - {self.car_make} {self.car_model}"
