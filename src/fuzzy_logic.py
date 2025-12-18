"""
Fuzzy Logic Module
Implements fuzzy logic system for priority calculation in manufacturing scheduling.
"""

import numpy as np
from typing import Dict, List, Tuple


class FuzzyMembershipFunction:
    """
    Base class for fuzzy membership functions.
    Defines how crisp values are converted to fuzzy membership degrees.
    """
    
    def __init__(self, name: str):
        """
        Initialize fuzzy membership function.
        
        Args:
            name: Name of the membership function
        """
        self.name = name
    
    def calculate_membership(self, value: float) -> float:
        """
        Calculate membership degree for a given value.
        
        Args:
            value: Input crisp value
            
        Returns:
            Membership degree between 0 and 1
        """
        raise NotImplementedError("Subclasses must implement this method")


class TrapezoidalMF(FuzzyMembershipFunction):
    """
    Trapezoidal membership function for fuzzy sets.
    """
    
    def __init__(self, name: str, a: float, b: float, c: float, d: float):
        """
        Initialize trapezoidal membership function.
        
        Args:
            name: Name of the fuzzy set
            a: Left base point
            b: Left top point
            c: Right top point
            d: Right base point
        """
        super().__init__(name)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def calculate_membership(self, value: float) -> float:
        """
        Calculate membership degree using trapezoidal function.
        
        Args:
            value: Input value
            
        Returns:
            Membership degree [0, 1]
        """
        if value <= self.a or value >= self.d:
            return 0.0
        elif self.a < value < self.b:
            return (value - self.a) / (self.b - self.a)
        elif self.b <= value <= self.c:
            return 1.0
        else:  # self.c < value < self.d
            return (self.d - value) / (self.d - self.c)


class TriangularMF(FuzzyMembershipFunction):
    """
    Triangular membership function for fuzzy sets.
    """
    
    def __init__(self, name: str, a: float, b: float, c: float):
        """
        Initialize triangular membership function.
        
        Args:
            name: Name of the fuzzy set
            a: Left base point
            b: Peak point
            c: Right base point
        """
        super().__init__(name)
        self.a = a
        self.b = b
        self.c = c
    
    def calculate_membership(self, value: float) -> float:
        """
        Calculate membership degree using triangular function.
        
        Args:
            value: Input value
            
        Returns:
            Membership degree [0, 1]
        """
        if value <= self.a or value >= self.c:
            return 0.0
        elif self.a < value < self.b:
            return (value - self.a) / (self.b - self.a)
        else:  # self.b <= value < self.c
            return (self.c - value) / (self.c - self.b)


class FuzzyVariable:
    """
    Represents a fuzzy linguistic variable with multiple fuzzy sets.
    """
    
    def __init__(self, name: str, universe_range: Tuple[float, float]):
        """
        Initialize fuzzy variable.
        
        Args:
            name: Name of the variable (e.g., 'processing_time', 'priority')
            universe_range: Tuple of (min, max) values
        """
        self.name = name
        self.universe_range = universe_range
        self.membership_functions: List[FuzzyMembershipFunction] = []
    
    def add_membership_function(self, mf: FuzzyMembershipFunction):
        """
        Add a membership function to this variable.
        
        Args:
            mf: Membership function to add
        """
        self.membership_functions.append(mf)
    
    def fuzzify(self, value: float) -> Dict[str, float]:
        """
        Convert crisp value to fuzzy membership degrees.
        
        Args:
            value: Crisp input value
            
        Returns:
            Dictionary mapping fuzzy set names to membership degrees
        """
        memberships = {}
        for mf in self.membership_functions:
            memberships[mf.name] = mf.calculate_membership(value)
        return memberships


class FuzzyRule:
    """
    Represents a fuzzy if-then rule for inference.
    """
    
    def __init__(self, antecedents: Dict[str, str], consequent: Tuple[str, str]):
        """
        Initialize fuzzy rule.
        
        Args:
            antecedents: Dictionary of variable names to fuzzy set names (IF part)
            consequent: Tuple of (variable_name, fuzzy_set_name) (THEN part)
        """
        self.antecedents = antecedents
        self.consequent = consequent
    
    def evaluate(self, fuzzy_inputs: Dict[str, Dict[str, float]]) -> float:
        """
        Evaluate rule strength using minimum (AND) operation.
        
        Args:
            fuzzy_inputs: Dictionary mapping variable names to their fuzzy memberships
            
        Returns:
            Rule firing strength [0, 1]
        """
        strengths = []
        for var_name, fuzzy_set in self.antecedents.items():
            if var_name in fuzzy_inputs and fuzzy_set in fuzzy_inputs[var_name]:
                strengths.append(fuzzy_inputs[var_name][fuzzy_set])
            else:
                return 0.0
        
        return min(strengths) if strengths else 0.0


class FuzzyInferenceSystem:
    """
    Mamdani-style fuzzy inference system for scheduling priority calculation.
    """
    
    def __init__(self):
        """Initialize fuzzy inference system."""
        self.variables: Dict[str, FuzzyVariable] = {}
        self.rules: List[FuzzyRule] = []
        self.output_variable: FuzzyVariable = None
    
    def add_variable(self, variable: FuzzyVariable):
        """
        Add a fuzzy variable to the system.
        
        Args:
            variable: Fuzzy variable to add
        """
        self.variables[variable.name] = variable
    
    def set_output_variable(self, variable: FuzzyVariable):
        """
        Set the output variable for defuzzification.
        
        Args:
            variable: Output fuzzy variable
        """
        self.output_variable = variable
        self.add_variable(variable)
    
    def add_rule(self, rule: FuzzyRule):
        """
        Add a fuzzy rule to the system.
        
        Args:
            rule: Fuzzy rule to add
        """
        self.rules.append(rule)
    
    def infer(self, inputs: Dict[str, float]) -> float:
        """
        Perform fuzzy inference and defuzzification.
        
        Args:
            inputs: Dictionary of variable names to crisp input values
            
        Returns:
            Defuzzified crisp output value
        """
        # Step 1: Fuzzification
        fuzzy_inputs = {}
        for var_name, value in inputs.items():
            if var_name in self.variables:
                fuzzy_inputs[var_name] = self.variables[var_name].fuzzify(value)
        
        # Step 2: Rule evaluation and aggregation
        output_aggregation = {}
        for mf in self.output_variable.membership_functions:
            output_aggregation[mf.name] = 0.0
        
        for rule in self.rules:
            strength = rule.evaluate(fuzzy_inputs)
            if strength > 0:
                consequent_var, consequent_set = rule.consequent
                if consequent_set in output_aggregation:
                    output_aggregation[consequent_set] = max(
                        output_aggregation[consequent_set], strength
                    )
        
        # Step 3: Defuzzification using centroid method
        return self._defuzzify_centroid(output_aggregation)
    
    def _defuzzify_centroid(self, aggregated_output: Dict[str, float]) -> float:
        """
        Defuzzify using centroid (center of gravity) method.
        
        Args:
            aggregated_output: Dictionary of fuzzy set names to activation levels
            
        Returns:
            Crisp output value
        """
        universe_min, universe_max = self.output_variable.universe_range
        resolution = 100
        x = np.linspace(universe_min, universe_max, resolution)
        
        # Calculate aggregated membership function
        aggregated_mf = np.zeros(resolution)
        for mf in self.output_variable.membership_functions:
            if mf.name in aggregated_output and aggregated_output[mf.name] > 0:
                for i, val in enumerate(x):
                    membership = mf.calculate_membership(val)
                    clipped = min(membership, aggregated_output[mf.name])
                    aggregated_mf[i] = max(aggregated_mf[i], clipped)
        
        # Calculate centroid
        numerator = np.sum(x * aggregated_mf)
        denominator = np.sum(aggregated_mf)
        
        if denominator == 0:
            return (universe_min + universe_max) / 2
        
        return numerator / denominator


def create_scheduling_fuzzy_system() -> FuzzyInferenceSystem:
    """
    Create a fuzzy inference system for manufacturing scheduling.
    
    The system considers:
    - Processing time (short, medium, long)
    - Due date urgency (low, medium, high)
    - Machine load (light, medium, heavy)
    
    Output:
    - Job priority (very_low, low, medium, high, very_high)
    
    Returns:
        Configured fuzzy inference system
    """
    fis = FuzzyInferenceSystem()
    
    # Define input variables
    # Processing Time (0-100 hours)
    proc_time = FuzzyVariable("processing_time", (0, 100))
    proc_time.add_membership_function(TriangularMF("short", 0, 0, 40))
    proc_time.add_membership_function(TriangularMF("medium", 20, 50, 80))
    proc_time.add_membership_function(TriangularMF("long", 60, 100, 100))
    fis.add_variable(proc_time)
    
    # Due Date Urgency (0-10, where 10 is most urgent)
    urgency = FuzzyVariable("urgency", (0, 10))
    urgency.add_membership_function(TriangularMF("low", 0, 0, 5))
    urgency.add_membership_function(TriangularMF("medium", 2, 5, 8))
    urgency.add_membership_function(TriangularMF("high", 5, 10, 10))
    fis.add_variable(urgency)
    
    # Machine Load (0-100%)
    load = FuzzyVariable("machine_load", (0, 100))
    load.add_membership_function(TriangularMF("light", 0, 0, 50))
    load.add_membership_function(TriangularMF("medium", 25, 50, 75))
    load.add_membership_function(TriangularMF("heavy", 50, 100, 100))
    fis.add_variable(load)
    
    # Define output variable
    # Priority (0-100)
    priority = FuzzyVariable("priority", (0, 100))
    priority.add_membership_function(TriangularMF("very_low", 0, 0, 25))
    priority.add_membership_function(TriangularMF("low", 0, 25, 50))
    priority.add_membership_function(TriangularMF("medium", 25, 50, 75))
    priority.add_membership_function(TriangularMF("high", 50, 75, 100))
    priority.add_membership_function(TriangularMF("very_high", 75, 100, 100))
    fis.set_output_variable(priority)
    
    # Define fuzzy rules
    rules = [
        # High urgency rules
        FuzzyRule({"urgency": "high", "processing_time": "short", "machine_load": "light"}, 
                  ("priority", "very_high")),
        FuzzyRule({"urgency": "high", "processing_time": "short", "machine_load": "medium"}, 
                  ("priority", "very_high")),
        FuzzyRule({"urgency": "high", "processing_time": "medium", "machine_load": "light"}, 
                  ("priority", "high")),
        FuzzyRule({"urgency": "high", "processing_time": "long", "machine_load": "light"}, 
                  ("priority", "high")),
        FuzzyRule({"urgency": "high", "machine_load": "heavy"}, 
                  ("priority", "medium")),
        
        # Medium urgency rules
        FuzzyRule({"urgency": "medium", "processing_time": "short", "machine_load": "light"}, 
                  ("priority", "high")),
        FuzzyRule({"urgency": "medium", "processing_time": "medium", "machine_load": "light"}, 
                  ("priority", "medium")),
        FuzzyRule({"urgency": "medium", "processing_time": "long", "machine_load": "medium"}, 
                  ("priority", "low")),
        FuzzyRule({"urgency": "medium", "machine_load": "heavy"}, 
                  ("priority", "low")),
        
        # Low urgency rules
        FuzzyRule({"urgency": "low", "processing_time": "short", "machine_load": "light"}, 
                  ("priority", "medium")),
        FuzzyRule({"urgency": "low", "processing_time": "medium"}, 
                  ("priority", "low")),
        FuzzyRule({"urgency": "low", "processing_time": "long"}, 
                  ("priority", "very_low")),
        FuzzyRule({"urgency": "low", "machine_load": "heavy"}, 
                  ("priority", "very_low")),
    ]
    
    for rule in rules:
        fis.add_rule(rule)
    
    return fis
