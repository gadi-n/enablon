# TODOS tests

This project is set to test the functionality of the tasks application in https://todomvc.com/examples/react/dist/

Project Overview:

Tests are conducted using Python 3.10.11 along with pytest and selenium.
Key project files include:
* README.md: Contains project information and instructions.
* requirements.txt: Lists package dependencies.
* test_positive.py: Positive test cases.
* test_negative.py: Negative test cases.
* conftest.py: Includes fixtures for test usage.
* utils.py: Houses utility functions for testing purposes.


Installation and Test Execution:

1. Ensure you have the correct Python version installed. While the project is developed and tested with Python 3.10.11, compatibility with other Python versions may exist.
2. Confirm pip installation on your system.
3. Install project dependencies using "pip install -r requirements.txt".
4. Execute tests with "pytest test_positive.py test_negative.py --html=report.html -n 13". This command runs tests in parallel, enhancing efficiency, since tests are non-dependent. To run tests sequentially, omit "-n 13". The "--html=report.html" option generates a comprehensive test report in HTML format.
5. View the test results conveniently in the generated report.html file via any web browser.


Enhancements for Comprehensive Testing:
While this project provides valuable insights, for a complete testing solution the following additions should be made:

* API testing (if applicable).
* Performance and stress testing.
* Visual testing using tools like Applitools Eyes (https://applitools.com/platform/eyes/).
* Establishing a reporting history to track test outcomes over time.