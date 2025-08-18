from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from trading.models import ContactInfo, Product, Vendor
from users.models import User


class ContactTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.user = User.objects.create(email='user@user.com')
        self.contact = ContactInfo.objects.create(email='contact@info.com', country='Test', city='Test', street='Test',
                                                  house_number='1')

    def test_create_contact(self):
        """Тест создания контакта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:contacts-list')
        data = {
            'email': 'new_contact@info.com',
            'country': 'Test2',
            'city': 'Test2',
            'street': 'Test2',
            'house_number': '2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactInfo.objects.count(), 2)

    def test_update_contact(self):
        """Тест изменения контакта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:contacts-detail', args=[self.contact.pk])
        data = {
            'email': 'new_contact@info.com',
            'country': 'Test2',
            'city': 'Test2',
            'street': 'Test2',
            'house_number': '2'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ContactInfo.objects.get(pk=self.contact.pk).email, 'new_contact@info.com')

    def test_delete_contact(self):
        """Тест удаления контакта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:contacts-detail', args=[self.contact.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactInfo.objects.count(), 0)

    def test_retrieve_contacts(self):
        """Тест получения контакта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:contacts-detail', kwargs={'pk': self.contact.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.contact.email)
        self.assertEqual(response.data['country'], self.contact.country)

    def test_list_contacts(self):
        """Тест получения списка контактов"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:contacts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class ProductTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.user = User.objects.create(email='user@user.com')
        self.product = Product.objects.create(title='Test', model='Test', launched_at='2015-01-01')

    def test_create_product(self):
        """Тест создания продукта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:products-list')
        data = {
            'title': 'New Product',
            'model': 'New Model',
            'launched_at': '2015-01-02'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        """Тест изменения продукта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:products-detail', args=[self.product.pk])
        data = {
            'title': 'New Product',
            'model': 'New Model',
            'launched_at': '2015-01-02'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(pk=self.product.pk).title, 'New Product')

    def test_delete_product(self):
        """Тест удаления продукта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:products-detail', args=[self.product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_retrieve_product(self):
        """Тест получения продукта"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:products-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.product.title)
        self.assertEqual(response.data['model'], self.product.model)

    def test_list_product(self):
        """Тест получения списка продуктов"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class VendorTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.user = User.objects.create(email='user@user.com')
        self.contact = ContactInfo.objects.create(email='contact@info.com', country='Test', city='Test', street='Test',
                                                  house_number='1')
        product1 = Product.objects.create(title='Test', model='Test', launched_at='2015-01-01')
        self.vendor = Vendor.objects.create(title='Test', level=0, contact=self.contact, debt_to_supplier=100)
        self.vendor.products.add(product1)
        self.vendor.save()

    def test_update_vendor(self):
        """Тест изменения поставщика"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:vendors-detail', args=[self.vendor.pk])
        product2 = Product.objects.create(title='Test2', model='Test2', launched_at='2015-01-02')
        data = {
            'title': 'New Vendor',
            'level': 0,
            'contact': self.contact.pk,
            'products': [product2.pk],
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        """Тест удаления поставщика"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:vendors-detail', args=[self.vendor.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_retrieve_vendor(self):
        """Тест получения поставщика"""
        self.client.force_authenticate(user=self.user)
        url = reverse('trading:vendors-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.vendor.title)
        self.assertEqual(response.data['level'], self.vendor.level)
        self.assertEqual(response.data['contact'], self.vendor.contact.pk)
        self.assertEqual(response.data['products'][0]['title'], self.vendor.products.first().title)
