import sys
import os
import pytest
import asyncio
from python.pyjs import PyJS

# Ensure local lookups find the correct pyjs core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_function_registration():
    """Verifies that functions are successfully registered onto the PyJS engine memory."""
    bridge = PyJS()
    
    @bridge.register()
    def mock_add(a: int, b: int) -> int:
        return a + b

    assert "mock_add" in bridge.functions
    assert bridge.functions["mock_add"]["exec"](5, 10) == 15

def test_telemetry_initialization():
    """Validates that real-time system diagnostic telemetry metrics boot with flawless data."""
    bridge = PyJS()
    telemetry = bridge.get_telemetry()
    
    assert telemetry["total_calls_processed"] == 0
    assert telemetry["failed_calls_count"] == 0
    assert telemetry["success_rate_percentage"] == 100.0
