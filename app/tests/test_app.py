import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

class BasicTests(unittest.TestCase): # Defines a set of test cases for my application.
    def setUp(self):
        self.app = app.test_client() # Creates a test client for my Flask application. The test client allows me to
        # simulate requests to my application without needing to run a server.

        self.app.testing = True # Enables testing mode in Flask. The test mode provides better error messages and disables 
        # certain features that are not needed during testing.

    def test_home_page(self):
        response = self.app.get("/") # Sends a GET request to the root URL ("/") of my Flask application using the test client
        # created earlier.

        self.assertEqual(response.status_code, 200) # Asserts that the status code of the response is 200, which means the request 
        # was successful. Otherwise the test will fail.

        self.assertIn(b"Hello, Jenkins CI/CD!", response.data) # Checks that the string "Hello, Jenkins CI/CD!" is present in 
        # the response data. The "b" prefix is used to indicate that Flask sends the response back as bytes rather than as a regular
        # text string.

if __name__ == "__main__":
    unittest.main()