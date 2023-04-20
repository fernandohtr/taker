import unittest
from courts.tj.al.taker import TakerTJAL

class TestTakerTJAL(unittest.TestCase):

    def setUp(self):
        process_number = '0710802-55.2018.8.02.0001'
        self.taker = TakerTJAL(process_number)

    def test_get_process_data(self):
        self.taker.first_instance.get_process_data = lambda: {'data': 'from FirstInstance'}
        self.taker.second_instance.get_process_data = lambda: {'data': 'from SecondInstance'}

        expected = [
            {'data': 'from FirstInstance'},
            {'data': 'from SecondInstance'}
        ]
        self.assertEqual(self.taker.get_process_data(), expected)

    def test_get_process_data_handles_exceptions(self):
        self.taker.first_instance.get_process_data = lambda: {'data': 'from FirstInstance'}
        self.taker.second_instance.get_process_data = lambda: 1/0

        expected = [{'data': 'from FirstInstance'}]
        self.assertEqual(self.taker.get_process_data(), expected)
