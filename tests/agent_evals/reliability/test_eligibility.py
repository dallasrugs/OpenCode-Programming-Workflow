import unittest
from eligibility import blocked
class EligibilityTests(unittest.TestCase):
    def test_pending_blocks(self):
        self.assertTrue(blocked(busy=True))
    def test_idle_allowed(self):
        self.assertFalse(blocked())
    def test_dirty_allowed(self):
        self.assertFalse(blocked(dirty=True))
