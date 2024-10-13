# tests/test_security.py

import unittest
from features.security import check_security_vulnerabilities

class TestSecurity(unittest.TestCase):
    def test_check_security_vulnerabilities(self):
        # Test with proper arguments
        try:
            check_security_vulnerabilities({"username": "user123", "email": "user@example.com"})
            self.assertTrue(True)  # This should pass if no exception is raised
        except Exception:
            self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
