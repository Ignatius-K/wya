"""Sample test"""
import unittest


class TestSample(unittest.TestCase):
    """Test sample"""

    def setUp(self):
        """Set up"""
        print("setUp")

    def tearDown(self):
        """Tear down"""
        print("tearDown")

    def test_sample(self):
        """Test sample"""
        self.assertEqual(1, 1)
