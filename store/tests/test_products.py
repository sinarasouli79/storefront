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
