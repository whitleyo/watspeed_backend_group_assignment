import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

def test_calculator_functionality(browser):
    page = browser.new_page()
    
    # Navigate to the Flask app (update the URL if running locally)
    page.goto("http://127.0.0.1:5000/calculator")

    # Check that all input fields are present
    assert page.locator("#nCustomers").is_visible()
    assert page.locator("#size").is_visible()
    assert page.locator("#cost").is_visible()
    assert page.locator("button").is_visible()

    # Fill form with test data
    page.fill("#nCustomers", "100")
    page.fill("#size", "2000")
    page.fill("#cost", "25")

    # Click the Calculate Profit button
    page.click("button")

    # Wait for result to appear
    page.wait_for_selector("#result")

    # Validate the result text appears
    result_text = page.locator("#result").text_content()
    assert "Estimated Annual Profit" in result_text, "Profit calculation failed"

    # Print the result (optional for debugging)
    print(f"Result: {result_text}")

    # Close the page
    page.close()

def test_calculator_profit_correctness(browser):
    page = browser.new_page()
    
    # Navigate to the Flask app
    page.goto("http://127.0.0.1:5000/calculator")

    # Test input values
    n_customers = 100
    store_size = 2000
    cost_per_sqft = 25

    # Fill form
    page.fill("#nCustomers", str(n_customers))
    page.fill("#size", str(store_size))
    page.fill("#cost", str(cost_per_sqft))

    # Click the Calculate Profit button
    page.click("button")

    # Wait for result to appear
    page.wait_for_selector("#result")

    # Extract displayed profit
    result_text = page.locator("#result").text_content()
    
    # Compute expected profit. Note that this formula should match the one in your app.
    # In future implemntation, we can separate this logic into a function called by
    # both the app and the test.
    average_spending = 5
    overhead_multiplier = 2
    expected_profit = (n_customers * 4 * 365 * average_spending) - (store_size * overhead_multiplier * cost_per_sqft)

    # Verify calculation matches expected output
    assert f"${expected_profit:.2f}" in result_text, f"Incorrect profit calculation: {result_text}"

    # Print result for debugging (optional)
    print(f"Expected Profit: ${expected_profit:.2f}, Displayed Result: {result_text}")

    page.close()