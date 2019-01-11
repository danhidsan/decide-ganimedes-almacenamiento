from base import mods
from postproc.models import PostProcType
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': PostProcType.IDENTITY,
            'questions': [
                {
                    'id': 1,
                    'options': [
                        {'option': 'Option 1', 'number': 1, 'votes': 5},
                        {'option': 'Option 2', 'number': 2, 'votes': 0},
                        {'option': 'Option 3', 'number': 3, 'votes': 3},
                        {'option': 'Option 4', 'number': 4, 'votes': 2},
                        {'option': 'Option 5', 'number': 5, 'votes': 5},
                        {'option': 'Option 6', 'number': 6, 'votes': 1},
                    ]
                },
                {
                    'id': 2,
                    'options': [
                        {'option': 'Option 1', 'number': 1, 'votes': 4},
                        {'option': 'Option 2', 'number': 2, 'votes': 2},
                        {'option': 'Option 3', 'number': 3, 'votes': 1},
                        {'option': 'Option 4', 'number': 4, 'votes': 1},
                        {'option': 'Option 5', 'number': 5, 'votes': 2},
                        {'option': 'Option 6', 'number': 6, 'votes': 0},
                    ],
                },
            ],
        }

        expected_result = {
            '1': [
                {'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5},
                {'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5},
                {'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3},
                {'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2},
                {'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1},
                {'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0},
            ],
            '2': [
                {'option': 'Option 1', 'number': 1, 'votes': 4, 'postproc': 4},
                {'option': 'Option 2', 'number': 2, 'votes': 2, 'postproc': 2},
                {'option': 'Option 5', 'number': 5, 'votes': 2, 'postproc': 2},
                {'option': 'Option 3', 'number': 3, 'votes': 1, 'postproc': 1},
                {'option': 'Option 4', 'number': 4, 'votes': 1, 'postproc': 1},
                {'option': 'Option 6', 'number': 6, 'votes': 0, 'postproc': 0},
            ],
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_seats(self):
        data = {
            'type': PostProcType.SEATS,
            'questions': [
                {
                    'id': 1,
                    'seats': 6,
                    'options': [
                        {'option': 'Option 1', 'number': 1, 'votes': 10},
                        {'option': 'Option 2', 'number': 2, 'votes': 5},
                        {'option': 'Option 3', 'number': 3, 'votes': 13},
                        {'option': 'Option 4', 'number': 4, 'votes': 2},
                    ],
                },
            ],
        }

        expected_result = {
            '1': [
                {'option': 'Option 3', 'number': 3, 'votes': 13, 'postproc': 3},
                {'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 2},
                {'option': 'Option 2', 'number': 2, 'votes': 5, 'postproc': 1},
                {'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 0},
            ],
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_team(self):
        data = {
            'type': PostProcType.TEAM,
            'questions': [
                {
                    'id': 1,
                    'options': [
                        {'option': 'Option 1', 'number': 1, 'votes': 5, 'team': 0},
                        {'option': 'Option 2', 'number': 2, 'votes': 0, 'team': 1},
                        {'option': 'Option 3', 'number': 3, 'votes': 3, 'team': 0},
                        {'option': 'Option 4', 'number': 4, 'votes': 2, 'team': 1},
                        {'option': 'Option 5', 'number': 5, 'votes': 5, 'team': 2},
                        {'option': 'Option 6', 'number': 6, 'votes': 1, 'team': 3},
                    ],
                },
            ],
        }

        expected_result = {
            '1': [
                {'option': 'Option 1', 'number': 1, 'votes': 5, 'team': 0},
                {'option': 'Option 3', 'number': 3, 'votes': 3, 'team': 0},
                {'option': 'Option 5', 'number': 5, 'votes': 5, 'team': 2},
                {'option': 'Option 4', 'number': 4, 'votes': 2, 'team': 1},
                {'option': 'Option 2', 'number': 2, 'votes': 0, 'team': 1},
                {'option': 'Option 6', 'number': 6, 'votes': 1, 'team': 3},
            ],
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_weight(self):
        data = {
            'type': PostProcType.WEIGHT,
            'questions': [
                {
                    'id': 1,
                    'options': [
                        {'option': 'Option 1', 'number': 1, 'votes': 5, 'weight': 5},
                        {'option': 'Option 2', 'number': 2, 'votes': 0, 'weight': 5},
                        {'option': 'Option 3', 'number': 3, 'votes': 3, 'weight': 5},
                        {'option': 'Option 4', 'number': 4, 'votes': 2, 'weight': 5},
                        {'option': 'Option 5', 'number': 5, 'votes': 5, 'weight': 5},
                        {'option': 'Option 6', 'number': 6, 'votes': 1, 'weight': 5},
                    ],
                },
            ],
        }

        expected_result = {
            '1': [
                {'option': 'Option 1', 'number': 1, 'votes': 5, 'weight': 5, 'postproc': 25},
                {'option': 'Option 5', 'number': 5, 'votes': 5, 'weight': 5, 'postproc': 25},
                {'option': 'Option 3', 'number': 3, 'votes': 3, 'weight': 5, 'postproc': 15},
                {'option': 'Option 4', 'number': 4, 'votes': 2, 'weight': 5, 'postproc': 10},
                {'option': 'Option 6', 'number': 6, 'votes': 1, 'weight': 5, 'postproc': 5},
                {'option': 'Option 2', 'number': 2, 'votes': 0, 'weight': 5, 'postproc': 0},
            ],
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)