"""Orders test module"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order, OrderDetail


class SetUpTests(APITestCase):
    """Enabling fixtures"""
    fixtures = ['order_details.json', 'orders.json', 'products.json']

    def setUp(self):
        """Preparing models objects"""
        self.order1 = Order.objects.get(pk=1)
        self.orders_url = reverse('orders')
        self.order_url = reverse('order', kwargs={'pk': 1})
        self.order_url2 = reverse('order', kwargs={'pk': 7})
        self.order_url3 = reverse('order', kwargs={'pk': 2})
        self.test_data = {
            "external_id": "CB-008",
            "details": [{
                "product": {"id": 4},
                "amount": 10,
                "price": "20.00"
            }]
        }
        self.wrong_test_data = {
            "external_id": "CB-008",
            "details": [{
                "product": {"id": 20},
                "amount": 10,
                "price": "12.00"
            }]
        }
        self.update_data = {
            "status": "accepted",
            "external_id": "CB-001-new",
            "details": [{
                "amount": 120,
                "price": "12.00"
            }]
        }


class OrderListCreateViewTestCase(SetUpTests):
    """Order list and order create view tests"""

    def test_orders_list_view(self):
        """Testing orders list"""
        response = self.client.get(self.orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CB-001')
        self.assertContains(response, 'CB-002')
        self.assertContains(response, 'Dropbox')
        self.assertContains(response, 'Microsoft Office')
        assert 'Content-Range' in response.headers
        assert response.headers['Content-Range'] == '1-3/7'

    def test_orders_list_pagination(self):
        """Testing pagination"""
        response = self.client.get(self.orders_url + '?offset=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CB-003')
        self.assertNotContains(response, 'CB-002')
        self.assertContains(response, 'Netflix')
        assert 'Content-Range' in response.headers
        assert response.headers['Content-Range'] == '3-5/7'

        response2 = self.client.get(self.orders_url + '?offset=5')
        assert response2.headers['Content-Range'] == '6-7/7'

        response3 = self.client.get(self.orders_url + '?offset=5&limit=1')
        self.assertEqual(len(response3.data), 1)
        self.assertContains(response3, 'CB-006')

    def test_orders_list_filters(self):
        """Test filters functionality"""
        response = self.client.get(self.orders_url + '?external_id=CB-002')
        self.assertEqual(len(response.data), 1)
        self.assertContains(response, 'CB-002')

        response2 = self.client.get(self.orders_url + '?ordering=-id')
        self.assertContains(response2, 'CB-007')
        self.assertContains(response2, 'CB-006')

    def test_order_create_error(self):
        """Test order invalid creation request"""
        data = {"external_id": "CB-003"}
        response = self.client.post(self.orders_url, data, format='json')
        error = str(response.data['external_id'][0])
        self.assertEqual(error, 'order with this external id already exists.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        requirements.txt
        response2 = self.client.post(
            self.orders_url,
            self.wrong_test_data,
            format='json'
        )
        error2 = str(response2.data['details'][0]['product'][0])
        self.assertEqual(error2, 'Product with id 20 does not exist.')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_create(self):
        """Test order creation"""
        assert Order.objects.all().count() == 7
        response = self.client.post(
            self.orders_url,
            self.test_data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert Order.objects.filter(external_id='CB-008').exists()
        assert OrderDetail.objects.filter(order__external_id='CB-008').exists()
        assert OrderDetail.objects.filter(product_id=4).exists()
        assert Order.objects.all().count() == 8


class OrderRetrieveUpdateDestroyTestCase(SetUpTests):
    """Distinct order retrieve, update and destroy test"""

    def test_retrieve_distinct_order(self):
        """Retrieve distinct order test"""
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CB-001')
        self.assertContains(response, 'Dropbox')
        self.assertContains(response, 'Microsoft Office')

    def test_update_order(self):
        """Updating order test"""
        response = self.client.put(self.order_url,
                                   self.update_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CB-001-new')
        self.assertNotContains(response, 'accepted')

    def test_delete_order_error(self):
        """Deleting order error handling test"""
        response = self.client.delete(self.order_url2)
        error = str(response.data['detail'])
        self.assertEqual(error,
                         "You can not delete orders with status 'accepted'.")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_order(self):
        """Deleting order test"""
        response = self.client.delete(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=1).exists())


class StatusChangeTestCase(SetUpTests):
    """Test changing of order status"""

    def test_status_change_error(self):
        """Testing status changing errors handling"""
        response = self.client.post(self.order_url2 + '/failed')
        error = str(response.data['detail'])
        self.assertEqual(error,
                         "You can not change order status if it is not 'new'")
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response2 = self.client.post(self.order_url + '/updated')
        error2 = str(response2.data['detail'])
        self.assertEqual(
            error2,
            "You can change order status only to 'accepted' or 'failed'"
        )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_status_change(self):
        """Test correct status change"""
        assert Order.objects.get(pk=1).status == 'new'
        response = self.client.post(self.order_url + '/accepted')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert Order.objects.get(pk=1).status == 'accepted'

        assert Order.objects.get(pk=2).status == 'new'
        response2 = self.client.post(self.order_url3 + '/failed')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        assert Order.objects.get(pk=2).status == 'failed'
