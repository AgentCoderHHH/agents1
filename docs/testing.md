# Testing Documentation

This document provides information about running tests for the AgentOpenApi system.

## Test Structure

The test suite is organized as follows:

```
tests/
├── __init__.py
├── config.py
├── run_tests.py
├── test_website_analytics.py
├── test_social_media_analytics.py
├── test_comparative_analytics.py
├── test_report_generator.py
├── test_alert_manager.py
└── test_integration.py
```

- `config.py`: Contains test configuration, mock data, and setup/cleanup functions
- `run_tests.py`: Main test runner script
- Individual test files for each agent
- `test_integration.py`: Integration tests for testing agents working together

## Running Tests

### Prerequisites

1. Python 3.8 or higher
2. Required packages (install using `pip install -r requirements.txt`):
   - pandas
   - numpy
   - unittest
   - pytest (optional)

### Running All Tests

To run all tests:

```bash
python tests/run_tests.py
```

This will:
1. Set up the test environment
2. Run all unit tests and integration tests
3. Clean up the test environment
4. Display test results

### Running Specific Tests

To run specific test files:

```bash
python -m unittest tests/test_website_analytics.py
python -m unittest tests/test_social_media_analytics.py
python -m unittest tests/test_comparative_analytics.py
python -m unittest tests/test_report_generator.py
python -m unittest tests/test_alert_manager.py
python -m unittest tests/test_integration.py
```

### Running Specific Test Cases

To run specific test cases within a file:

```bash
python -m unittest tests.test_website_analytics.TestWebsiteAnalyticsAgent.test_analyze_performance
python -m unittest tests.test_integration.TestAgentIntegration.test_end_to_end_pipeline
```

### Test Output

The test runner provides detailed output including:
- Test execution status (pass/fail)
- Error messages and stack traces for failed tests
- Test coverage information (if coverage is enabled)

## Test Types

### Unit Tests

Unit tests verify the functionality of individual agents and their methods:

- `WebsiteAnalyticsAgent`: Tests for website performance analysis
- `SocialMediaAnalyticsAgent`: Tests for social media analysis
- `ComparativeAnalyticsAgent`: Tests for cross-channel analysis
- `ReportGeneratorAgent`: Tests for report generation
- `AlertManagerAgent`: Tests for alert management

### Integration Tests

Integration tests verify that agents work together correctly:

- Website analytics pipeline
- Social media analytics pipeline
- Comparative analytics pipeline
- Comprehensive analytics pipeline
- Alerting pipeline
- End-to-end pipeline

## Mock Data

The test suite uses mock data defined in `tests/config.py`:

- `MOCK_WEBSITE_DATA`: Sample website metrics
- `MOCK_ANALYTICS_DATA`: Sample analytics metrics
- `MOCK_TWITTER_DATA`: Sample Twitter metrics

## Test Environment

The test environment is set up and cleaned up automatically:

- `setup_test_environment()`: Creates necessary directories and configurations
- `cleanup_test_environment()`: Removes test files and cleans up

## Adding New Tests

To add new tests:

1. Create a new test file in the `tests` directory
2. Follow the existing test structure
3. Use the provided mock data and helper functions
4. Add the test file to the test suite

Example:

```python
import unittest
from agents.your_agent import YourAgent
from tests.config import setup_test_environment, cleanup_test_environment

class TestYourAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_test_environment()
    
    @classmethod
    def tearDownClass(cls):
        cleanup_test_environment()
    
    def setUp(self):
        self.agent = YourAgent()
    
    def test_your_method(self):
        # Your test code here
        pass

if __name__ == '__main__':
    unittest.main()
```

## Troubleshooting

Common issues and solutions:

1. **ImportError: No module named 'agents'**
   - Ensure you're running tests from the project root directory
   - Check that the project root is in your Python path

2. **FileNotFoundError**
   - Verify that test directories exist
   - Check file permissions

3. **Test failures**
   - Check the test output for specific error messages
   - Verify that mock data matches expected formats
   - Ensure all required dependencies are installed

## Continuous Integration

The test suite is designed to work with CI/CD pipelines:

1. Set up the test environment
2. Run the test suite
3. Generate test reports
4. Clean up the environment

Example CI configuration:

```yaml
test:
  script:
    - pip install -r requirements.txt
    - python tests/run_tests.py
  artifacts:
    reports:
      junit: test-results.xml
``` 