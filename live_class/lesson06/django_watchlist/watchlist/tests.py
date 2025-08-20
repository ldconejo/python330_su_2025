from django.test import TestCase
from rest_framework.test import RequestsClient

from .models import Genre, Platform, Show

class WatchlistTest(TestCase):
    def setUp(self):
        self.client = RequestsClient()
        self.test_platform_id = Platform.objects.create(platform="test").pk
        self.test_genre_id = Genre.objects.create(genre="test").pk
        self.test_show_id = Show.objects.create(
            title="test", season=1, watched=False, platform_id=self.test_platform_id
        ).pk

    def test_create_show(self):
        post_response = self.client.post("http://localhost:8000/api/shows",
                                         data={
                                             'title': 'test',
                                             'season': 1,
                                             'watched': False,
                                             'platform_id': self.test_platform_id,
                                             'genre_ids': [self.test_genre_id]
                                         })
        self.assertEqual(post_response.status_code, 201)

    def test_update_show(self):
        post_response = self.client.put(f"http://locahost:8000/api/shows/{self.test_show_id}",
                                        data={
                                            'title': 'test',
                                            'season': 1,
                                            'watched': True,
                                            'platform_id': self.test_platform_id,
                                            'genre_ids': [self.test_genre_id]
                                        })
        self.assertEqual(post_response.status_code, 200)
        expected_response = {"id":1,"title":"test","season":1,"image_url":"","watched":True,"platform":"test","genres":["test"]}
        self.assertEqual(post_response.json()['title'], 'test')
