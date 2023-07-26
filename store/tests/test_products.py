import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Product


@pytest.mark.django_db
class TestRetrieveProduct:

    @pytest.fixture
    def retrieve_product(self, api_client):
        def _retrieve_product(product):
            return api_client.get(f'/store/products/{product.id}/')

        return _retrieve_product

    def test_single_product_return_200(self, retrieve_product):
        product = baker.make(Product)

        response = retrieve_product(product)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title
        assert response.data['description'] == product.description
        assert response.data['unit_price'] == product.unit_price
        assert response.data['inventory'] == product.inventory
        assert response.data['collection'] == product.collection.id

    def test_product_list_returns_200(self, api_client):
        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_product_not_exist_return_404(self, retrieve_product):
        product = baker.make(Product, id=-1)
        response = retrieve_product(product)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteProduct:
    @pytest.fixture
    def delete_product(self, api_client, authenticate):
        def _delete_product(is_staff=False, is_anonymous=False):
            product = baker.make(Product)
            if not is_anonymous:
                authenticate(is_staff=is_staff)
            return api_client.delete(f'/store/products/{product.id}/')

        return _delete_product

    def test_if_user_not_admin_return_403(self, delete_product):
        response = delete_product(is_staff=False)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] is not None

    def test_if_user_anonymous_return401(self, delete_product):
        response = delete_product(is_anonymous=True)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] is not None

    def test_if_user_admin_return_204(self, authenticate, delete_product):
        response = delete_product(is_staff=True)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestCreateProduct:

    @pytest.fixture
    def create_product(self, api_client, authenticate):
        def _create_product(data, is_staff=False, is_anonymous=False):
            if not is_anonymous:
                authenticate(is_staff=is_staff)

            return api_client.post('/store/products/', data=data)

        return _create_product

    def test_if_user_anonymous_return_401(self, create_product):
        response = create_product(data={
            "title": "a",
            "description": "a",
            "unit_price": 3.3,
            "inventory": -2,
            "collection": 1
        }, is_anonymous=True)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_return_403(self, create_product):
        response = create_product(data={
            "title": "a",
            "description": "a",
            "unit_price": 3.3,
            "inventory": -2,
            "collection": 1
        }, is_staff=False)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_return_201(self, create_product):
        response = create_product(data={
            "title": "a",
            "description": "a",
            "unit_price": 3.3,
            "inventory": 2,
            "collection": 1
        }, is_staff=True)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_data_invalid_return_400(self, create_product):
        response = create_product(data={
            "title": "",
            "description": "",
            "unit_price": -3.3,
            "inventory": -2,
            "collection": -1
        }, is_staff=True)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        assert response.data['unit_price'] is not None
        assert response.data['inventory'] is not None
        assert response.data['collection'] is not None
