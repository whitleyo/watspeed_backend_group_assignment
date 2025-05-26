import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

def test_cash_register_transactions(browser):
    page = browser.new_page()
    
    # Navigate to the cash register API page with test parameters
    page.goto("http://127.0.0.1:5001/transactions?store_id=2&start_time=2025-05-25T10:00:00&end_time=2025-05-25T10:10:00")

    # Extract the API response
    response = page.content()
    
    # Validate that the response contains transactions
    assert "transactions" in response, "Cash register API did not return transaction data."

    # Print for debugging (optional)
    print(f"API Response: {response}")

    page.close()

def test_cash_register_transaction_details(browser):
    page = browser.new_page()
    
    # Navigate to the cash register API page with test parameters
    page.goto("http://127.0.0.1:5001/transactions?store_id=1&start_time=2025-05-25T10:00:00&end_time=2025-05-25T10:10:00")

    # Extract JSON response
    response_text = page.content()
    response_data = page.evaluate("JSON.parse(document.body.innerText)")

    # Verify 'transactions' key exists
    assert "transactions" in response_data, "API response does not contain transactions."

    # Validate each transaction
    for transaction in response_data["transactions"]:
        assert "time" in transaction, "Transaction missing 'time' field."
        assert "amount" in transaction, "Transaction missing 'amount' field."
        assert 2.00 <= transaction["amount"] <= 20.00, f"Invalid amount: {transaction['amount']}"

    print("✅ Transaction data is correctly formatted and within expected ranges.")

    page.close()

def test_missing_parameters(browser):
    page = browser.new_page()
    
    # Try calling the API without required parameters
    page.goto("http://127.0.0.1:5001/transactions")

    # Extract response data
    response_data = page.evaluate("JSON.parse(document.body.innerText)")

    # Validate that an error appears
    assert "error" in response_data, "API did not return an error for missing parameters."
    assert response_data["error"] == "Missing required parameters: store_id, start_time, end_time", "Incorrect error message."

    page.close()

def test_invalid_date_format(browser):
    page = browser.new_page()
    
    # Call the API with an incorrect date format
    page.goto("http://127.0.0.1:5001/transactions?store_id=2&start_time=25-05-2025 10:00&end_time=25-05-2025 10:10")

    # Extract response data
    response_data = page.evaluate("JSON.parse(document.body.innerText)")

    # Validate error message
    assert "error" in response_data, "API did not return an error for invalid date format."
    assert "Invalid date format" in response_data["error"], "Incorrect error message for invalid date format."

    page.close()

def test_start_time_after_end_time(browser):
    page = browser.new_page()
    
    # Call the API with start_time greater than end_time
    page.goto("http://127.0.0.1:5001/transactions?store_id=1&start_time=2025-05-25T10:10:00&end_time=2025-05-25T10:00:00")

    # Extract response data
    response_data = page.evaluate("JSON.parse(document.body.innerText)")

    # Validate error message
    assert "error" in response_data, "API did not return an error for incorrect time order."
    assert response_data["error"] == "start_time must be before end_time", "Incorrect error message for time order."

    page.close()