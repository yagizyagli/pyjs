"""
bridge.ids

Identifier generation utilities.
"""

from __future__ import annotations

from uuid import uuid4
from time import time_ns


def generate_id() -> str:
    """
    Generate unique identifier.
    """
    return uuid4().hex


def generate_request_id() -> str:
    """
    Generate RPC request identifier.
    """
    return f"req_{uuid4().hex}"


def generate_session_id() -> str:
    """
    Generate session identifier.
    """
    return f"ses_{uuid4().hex}"


def generate_trace_id() -> str:
    """
    Generate distributed tracing identifier.
    """
    return f"trace_{uuid4().hex}"


def generate_correlation_id() -> str:
    """
    Generate request correlation identifier.
    """
    return f"corr_{uuid4().hex}"


def timestamp_id() -> str:
    """
    Time based identifier.
    """
    return str(time_ns())
