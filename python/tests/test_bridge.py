import sys
import os
import pytest

# Multi-layered absolute lookup patch ensuring the core finds 'python.pyjs' smoothly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from python.pyjs import PyJS

def test_function_registration():
    """Verifies that functions are successfully registered onto the PyJS engine memory."""
    bridge = PyJS()
    
    @bridge.register(name="mock_add")
    def mock_add(a: int, b: int) -> int:
        return a + b

    # Confirm core integration keys and execution parameters
    assert "mock_add" in bridge.functions
    assert bridge.functions["mock_add"]["exec"](5, 10) == 15

def test_telemetry_initialization():
    """Validates that real-time system diagnostic telemetry metrics boot with flawless data."""
    bridge = PyJS()
    telemetry = bridge.get_telemetry()
    
    # Assert type presence and strict zero-baseline defaults
    assert telemetry["total_calls_processed"] == 0
    assert telemetry["failed_calls_count"] == 0
    # Soft assert for float values to prevent strict decimal point rejections
    assert float(telemetry["success_rate_percentage"]) == 100.0
