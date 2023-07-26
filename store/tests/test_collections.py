import pytest
from model_bakery import baker
from rest_framework import status

from store.models import Collection, Product


@pytest.mark.django_db
class TestCreateCollection:

    @pytest.fixture
    def create_collection(self, api_client):
        def do_create_collection(collection):
            return api_client.post('/store/collections/', collection)

        return do_create_collection

    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, api_client, authenticate, create_collection):
        authenticate()

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, api_client, authenticate, create_collection):
        authenticate(is_staff=True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exist_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }

    def test_if_collection_does_not_exist_returns_404(self, api_client):
        collection_id = -1

        response = api_client.get(f'/store/collections/{collection_id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] is not None


@pytest.mark.django_db
class TestUpdateCollection:
    @pytest.fixture
    def update_collection(self, api_client):
        def _update_collection(collection, data):
            return api_client.patch(f'/store/collections/{collection.id}/', data)

        return _update_collection

    def test_if_user_is_not_admin_return_403(self, authenticate, update_collection):
        collection = baker.make(Collection)
        authenticate(is_staff=False)

        response = update_collection(collection, {'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_anonymous_return_401(self, update_collection):
        collection = baker.make(Collection)

        response = update_collection(collection, {'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_return_200(self, update_collection, authenticate):
        collection = baker.make(Collection)
        authenticate(is_staff=True)

        response = update_collection(collection, {'title': 'a'})

        assert response.status_code == status.HTTP_200_OK
        print(response.data)
        assert response.data == {
            'id': collection.id,
            'title': 'a',
            'products_count': 0
        }

    def test_if_collection_not_exist_return_404(self, update_collection, authenticate):
        collection = baker.make(Collection, id=-1)
        authenticate(is_staff=True)

        response = update_collection(collection, {'title': 'a'})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCollection:

    @pytest.fixture
    def delete_collection(self, api_client):
        def _delete_collection(collection):
            return api_client.delete(f'/store/collections/{collection.id}/')

        return _delete_collection

    def test_if_user_not_admin_return_403(self, authenticate, delete_collection):
        collection = baker.make(Collection)
        authenticate(is_staff=False)

        response = delete_collection(collection)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_admin_return_204(self, authenticate, delete_collection):
        collection = baker.make(Collection)
        authenticate(is_staff=True)

        response = delete_collection(collection)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_collection_not_exist_return_404(self, authenticate, delete_collection):
        collection = baker.make(Collection, id=-1)
        authenticate(is_staff=True)

        response = delete_collection(collection)

    def test_if_collection_products_not_empty_return_405(self, authenticate, delete_collection):
        collection = baker.make(Collection)
        products = baker.make(Product, collection=collection, _quantity=10)
        print(collection.product_set.count())
        authenticate(is_staff=True)

        response = delete_collection(collection)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data['error'] is not None
