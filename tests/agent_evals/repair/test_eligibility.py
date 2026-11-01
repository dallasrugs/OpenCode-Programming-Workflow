import unittest
from eligibility import can_execute

class EligibilityTests(unittest.TestCase):
    def state(self, **overrides):
        return dict(dict(busy=False, active=False, conflict=False, paused=False, dirty=False), **overrides)

    def test_idle(self):
        self.assertTrue(can_execute(self.state()))

    def test_busy(self):
        self.assertFalse(can_execute(self.state(busy=True)))
