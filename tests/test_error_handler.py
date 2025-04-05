import pytest
from datetime import datetime
from agents.error_handler import ErrorHandler, ErrorSeverity, ErrorContext

@pytest.fixture
def error_handler():
    return ErrorHandler("test_agent")

@pytest.fixture
def sample_error():
    try:
        raise ValueError("Test error message")
    except ValueError as e:
        return e

def test_error_handler_initialization(error_handler):
    """Test that ErrorHandler initializes correctly"""
    assert error_handler.agent_name == "test_agent"
    assert isinstance(error_handler.error_log, dict)
    assert len(error_handler.error_log) == 0

def test_handle_error(error_handler, sample_error):
    """Test error handling with basic error"""
    error_context = error_handler.handle_error(
        sample_error,
        "test_operation",
        ErrorSeverity.ERROR
    )
    
    assert isinstance(error_context, ErrorContext)
    assert error_context.agent_name == "test_agent"
    assert error_context.operation == "test_operation"
    assert error_context.severity == ErrorSeverity.ERROR
    assert error_context.error_type == "ValueError"
    assert error_context.error_message == "Test error message"
    assert error_context.stack_trace is not None
    assert error_context.additional_data is None

def test_handle_error_with_additional_data(error_handler, sample_error):
    """Test error handling with additional data"""
    additional_data = {"key": "value", "number": 42}
    error_context = error_handler.handle_error(
        sample_error,
        "test_operation",
        ErrorSeverity.ERROR,
        additional_data
    )
    
    assert error_context.additional_data == additional_data

def test_error_severity_levels(error_handler, sample_error):
    """Test different error severity levels"""
    severities = [
        ErrorSeverity.DEBUG,
        ErrorSeverity.INFO,
        ErrorSeverity.WARNING,
        ErrorSeverity.ERROR,
        ErrorSeverity.CRITICAL
    ]
    
    for severity in severities:
        error_context = error_handler.handle_error(
            sample_error,
            "test_operation",
            severity
        )
        assert error_context.severity == severity

def test_get_error_history(error_handler, sample_error):
    """Test retrieving error history"""
    # Add multiple errors
    for i in range(3):
        error_handler.handle_error(
            sample_error,
            f"operation_{i}",
            ErrorSeverity.ERROR
        )
    
    history = error_handler.get_error_history()
    assert len(history) == 3
    assert all(isinstance(key, str) for key in history.keys())
    assert all(isinstance(value, ErrorContext) for value in history.values())

def test_clear_error_history(error_handler, sample_error):
    """Test clearing error history"""
    # Add an error
    error_handler.handle_error(
        sample_error,
        "test_operation",
        ErrorSeverity.ERROR
    )
    
    assert len(error_handler.error_log) == 1
    error_handler.clear_error_history()
    assert len(error_handler.error_log) == 0

def test_error_context_timestamp(error_handler, sample_error):
    """Test that error context includes correct timestamp"""
    error_context = error_handler.handle_error(
        sample_error,
        "test_operation",
        ErrorSeverity.ERROR
    )
    
    assert isinstance(error_context.timestamp, datetime)
    assert error_context.timestamp <= datetime.now()

def test_error_context_serialization(error_handler, sample_error):
    """Test that error context can be serialized"""
    error_context = error_handler.handle_error(
        sample_error,
        "test_operation",
        ErrorSeverity.ERROR,
        {"key": "value"}
    )
    
    # Test that all attributes can be converted to string
    assert isinstance(str(error_context.timestamp), str)
    assert isinstance(error_context.agent_name, str)
    assert isinstance(error_context.operation, str)
    assert isinstance(error_context.severity.value, str)
    assert isinstance(error_context.error_type, str)
    assert isinstance(error_context.error_message, str)
    assert isinstance(error_context.stack_trace, str)
    assert isinstance(str(error_context.additional_data), str) 