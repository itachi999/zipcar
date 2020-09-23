from django.test import TestCase
from zip.models import Reservation
# Create your tests here.

class LocationTestCase(TestCase):
    def setUp(self):
        Reservation.objects.create(rental_location="san jose")
        Reservation.objects.create(rental_location="san francisco")
    def test_locations(self):
        rental_location = Reservation.objects.get(rental_location="san jose")
        self.assertEqual(rental_location.rental_location, "san jose")
        rentalAddress = Reservation.objects.get(rental_location="san francisco")
        self.assertEqual(rentalAddress.rental_location, "san francisco")

# class vehicleTestCase(TestCase):
#     def setUp(self):
#         Vehicle.objects.create(make_model="tesla3", year=2019)
#         Vehicle.objects.create(make_model="audi", year=2018)
#     def test_locations(self):
#         v1 = Vehicle.objects.get(make_model="tesla3")
#         self.assertEqual(v1.year, 2019)
#         v2 = Vehicle.objects.get(make_model="audi")
#         self.assertEqual(v2.year, 2018)