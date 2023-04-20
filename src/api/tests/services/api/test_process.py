import unittest
from unittest.mock import MagicMock, patch

import falcon
# import json

# from routes.api import Api
from services.api.process import Process


class TestProcess(unittest.TestCase):

    def setUp(self):
        fake_response = MagicMock(spec=falcon.Response)
        self.process = Process('0710802-55.2018.8.02.0001', fake_response)

    def test_check_existence_process_number_bad_request(self):
        with self.assertRaises(falcon.HTTPBadRequest):
            self.process._check_existence_process_number(None)

    def test_validate_process_number_bad_request(self):
        with self.assertRaises(falcon.HTTPBadRequest):
            self.process._validate_process_number('1234567-12.2018.1.01.12345')

    @patch('court_numbering.NUMBERING')
    def test_get_court_by_numbering_with_matching_court(self, mock_numbering):
        process_number = '0710802-55.2018.8.02.0001'
        court = self.process._get_court_by_numbering(process_number)
        self.assertEqual(court, 'TJAL')

    @patch('court_numbering.NUMBERING')
    def test_get_court_by_numbering_with_non_matching_court(self, mock_numbering):
        process_number = '0710802-55.2018.0.00.0001'
        court = self.process._get_court_by_numbering(process_number)
        self.assertEqual(court, '')
