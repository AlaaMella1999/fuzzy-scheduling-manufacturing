"""
Unit tests for fuzzy logic module.
"""

import unittest
from src.fuzzy_logic import (
    TrapezoidalMF, TriangularMF, FuzzyVariable, FuzzyRule,
    FuzzyInferenceSystem, create_scheduling_fuzzy_system
)


class TestMembershipFunctions(unittest.TestCase):
    """Test fuzzy membership functions."""
    
    def test_triangular_mf_center(self):
        """Test triangular membership at peak."""
        mf = TriangularMF("test", 0, 5, 10)
        self.assertEqual(mf.calculate_membership(5), 1.0)
    
    def test_triangular_mf_boundaries(self):
        """Test triangular membership at boundaries."""
        mf = TriangularMF("test", 0, 5, 10)
        self.assertEqual(mf.calculate_membership(0), 0.0)
        self.assertEqual(mf.calculate_membership(10), 0.0)
        self.assertEqual(mf.calculate_membership(-1), 0.0)
        self.assertEqual(mf.calculate_membership(11), 0.0)
    
    def test_triangular_mf_slopes(self):
        """Test triangular membership on slopes."""
        mf = TriangularMF("test", 0, 5, 10)
        self.assertEqual(mf.calculate_membership(2.5), 0.5)
        self.assertEqual(mf.calculate_membership(7.5), 0.5)
    
    def test_trapezoidal_mf_plateau(self):
        """Test trapezoidal membership on plateau."""
        mf = TrapezoidalMF("test", 0, 3, 7, 10)
        self.assertEqual(mf.calculate_membership(5), 1.0)
        self.assertEqual(mf.calculate_membership(3), 1.0)
        self.assertEqual(mf.calculate_membership(7), 1.0)
    
    def test_trapezoidal_mf_boundaries(self):
        """Test trapezoidal membership at boundaries."""
        mf = TrapezoidalMF("test", 0, 3, 7, 10)
        self.assertEqual(mf.calculate_membership(0), 0.0)
        self.assertEqual(mf.calculate_membership(10), 0.0)


class TestFuzzyVariable(unittest.TestCase):
    """Test fuzzy variable class."""
    
    def setUp(self):
        """Set up test fuzzy variable."""
        self.var = FuzzyVariable("test_var", (0, 10))
        self.var.add_membership_function(TriangularMF("low", 0, 0, 5))
        self.var.add_membership_function(TriangularMF("medium", 2, 5, 8))
        self.var.add_membership_function(TriangularMF("high", 5, 10, 10))
    
    def test_fuzzify_low(self):
        """Test fuzzification at low value."""
        result = self.var.fuzzify(2)
        self.assertGreater(result["low"], 0)
        self.assertGreaterEqual(result["medium"], 0)
        self.assertEqual(result["high"], 0)
    
    def test_fuzzify_high(self):
        """Test fuzzification at high value."""
        result = self.var.fuzzify(8)
        self.assertEqual(result["low"], 0)
        self.assertGreaterEqual(result["medium"], 0)
        self.assertGreater(result["high"], 0)


class TestFuzzyRule(unittest.TestCase):
    """Test fuzzy rule evaluation."""
    
    def test_rule_evaluation(self):
        """Test fuzzy rule evaluation with valid inputs."""
        rule = FuzzyRule(
            {"temp": "hot", "humidity": "high"},
            ("fan_speed", "fast")
        )
        
        fuzzy_inputs = {
            "temp": {"hot": 0.8, "cold": 0.2},
            "humidity": {"high": 0.6, "low": 0.4}
        }
        
        strength = rule.evaluate(fuzzy_inputs)
        self.assertEqual(strength, 0.6)  # min(0.8, 0.6)
    
    def test_rule_evaluation_missing_input(self):
        """Test rule evaluation with missing input."""
        rule = FuzzyRule(
            {"temp": "hot", "humidity": "high"},
            ("fan_speed", "fast")
        )
        
        fuzzy_inputs = {
            "temp": {"hot": 0.8}
        }
        
        strength = rule.evaluate(fuzzy_inputs)
        self.assertEqual(strength, 0.0)


class TestFuzzyInferenceSystem(unittest.TestCase):
    """Test fuzzy inference system."""
    
    def test_scheduling_fuzzy_system_creation(self):
        """Test creation of scheduling fuzzy system."""
        fis = create_scheduling_fuzzy_system()
        
        self.assertIsNotNone(fis)
        self.assertIn("processing_time", fis.variables)
        self.assertIn("urgency", fis.variables)
        self.assertIn("machine_load", fis.variables)
        self.assertIn("priority", fis.variables)
        self.assertGreater(len(fis.rules), 0)
    
    def test_fuzzy_inference_high_priority(self):
        """Test inference for high priority scenario."""
        fis = create_scheduling_fuzzy_system()
        
        inputs = {
            "processing_time": 10,  # short
            "urgency": 9,  # high
            "machine_load": 20  # light
        }
        
        priority = fis.infer(inputs)
        self.assertGreater(priority, 70)  # Should be high priority
    
    def test_fuzzy_inference_low_priority(self):
        """Test inference for low priority scenario."""
        fis = create_scheduling_fuzzy_system()
        
        inputs = {
            "processing_time": 80,  # long
            "urgency": 1,  # low
            "machine_load": 80  # heavy
        }
        
        priority = fis.infer(inputs)
        self.assertLess(priority, 40)  # Should be low priority
    
    def test_fuzzy_inference_medium_priority(self):
        """Test inference for medium priority scenario."""
        fis = create_scheduling_fuzzy_system()
        
        inputs = {
            "processing_time": 50,  # medium
            "urgency": 5,  # medium
            "machine_load": 50  # medium
        }
        
        priority = fis.infer(inputs)
        self.assertGreater(priority, 30)
        self.assertLess(priority, 70)


if __name__ == '__main__':
    unittest.main()
