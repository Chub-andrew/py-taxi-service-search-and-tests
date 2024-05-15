from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test", country="test_country")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEquals(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEquals(list(response.context["manufacturer_list"]), list(manufacturers),)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")