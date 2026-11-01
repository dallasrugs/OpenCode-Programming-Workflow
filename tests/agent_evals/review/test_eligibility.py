import unittest
from eligibility import can_execute

class EligibilityTests(unittest.TestCase):
    def test_paused(self):
        self.assertFalse(can_execute(dict(paused=True, busy=False, active=False, conflict=False, dirty=False)))
