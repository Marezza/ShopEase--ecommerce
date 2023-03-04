from django.contrib.auth.models import User
from rest_framework import status
from store.models import Collection
from model_bakery import baker
import pytest
from store.tests.conftest import api_client


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anontmous_returns_401(self, create_collection):
        # Arrange - prepare sysptem for a test
        # Act- a behaviour we want to test
        #client = APIClient()
        # send post (request to, request body)
        #response = api_client.post('/store/collections/', {'title': 'a'})
        response = create_collection({'title': 'a'})
        # Assert- what do we expect, what behaviour
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):
        #client = APIClient()
        # api_client.force_authenticate(user={})
        authenticate(is_stuff=False)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        # api_client.force_authenticate(user=User(is_staff=True))
        authenticate(is_stuff=True)

        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_collection):
        # api_client.force_authenticate(user=User(is_staff=True))
        authenticate(is_stuff=True)

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_the_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0
        }
