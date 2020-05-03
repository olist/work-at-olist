# import pytest
# from django.urls import reverse
#
# from olist.library.models import Author
#
#
# @pytest.fixture
# def author(db):
#     a = Author(name="Luciano Ramalho")
#     a.save()
#     return a
#
#
# @pytest.fixture
# def resp(client, author):
#     return client.get(reverse('video'))
#
#
# def test_name_author(resp):
#     assert resp.statuscode == 200
