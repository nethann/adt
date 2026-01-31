from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

# Configuration
LOGIN_URL = "https://adtreferral.com/login/"
EMAIL = "nethan.nagendran@gmail.com"
PASSWORD = "Helloschool1!"

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("Starting browser...")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    # Step 1: Navigate to login page
    print(f"Step 1: Navigating to {LOGIN_URL}")
    driver.get(LOGIN_URL)
    print(f"Page loaded: {driver.title}")

    # Step 2: Find and fill login form
    print("\nStep 2: Filling login form...")

    # Wait for username field and fill it
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "LoginUsername")))
    username_field.clear()
    username_field.send_keys(EMAIL)
    print(f"  ✓ Entered username: {EMAIL}")

    # Find and fill password field
    password_field = driver.find_element(By.NAME, "LoginPassword")
    password_field.clear()
    password_field.send_keys(PASSWORD)
    print(f"  ✓ Entered password: {'*' * len(PASSWORD)}")

    # Step 3: Submit the form
    print("\nStep 3: Submitting login...")

    # Find and click the login button
    # Try different selectors for the login button
    login_button = None
    button_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, ".login-button"),
        (By.CSS_SELECTOR, "button.btn-primary"),
        (By.XPATH, "//button[contains(text(), 'Log')]"),
        (By.XPATH, "//button[contains(text(), 'Sign')]"),
        (By.XPATH, "//input[@value='Log In']"),
    ]

    for selector_type, selector in button_selectors:
        try:
            login_button = driver.find_element(selector_type, selector)
            if login_button.is_displayed():
                print(f"  Found login button using: {selector}")
                break
        except:
            continue

    if login_button:
        login_button.click()
        print("  ✓ Clicked login button")
    else:
        # Try submitting the form directly
        print("  No button found, submitting form via Enter key...")
        password_field.submit()

    # Step 4: Wait for response and check result
    print("\nStep 4: Waiting for login response...")
    time.sleep(3)  # Wait for AJAX response

    current_url = driver.current_url
    print(f"  Current URL: {current_url}")

    # Check if login was successful
    if 'login' not in current_url.lower() or current_url != LOGIN_URL:
        print("\n✓ LOGIN SUCCESSFUL - Redirected away from login page!")
    else:
        # Check for error messages on page
        print("\nStill on login page, checking for errors...")
        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert, .validation-error, [class*='error']")
            for err in error_elements:
                if err.text.strip():
                    print(f"  Error found: {err.text.strip()}")
        except:
            pass

    # Step 5: Save cookies
    print("\n" + "="*60)
    print("Step 5: Saving session cookies...")
    print("="*60)

    cookies = driver.get_cookies()
    print(f"\nSession Cookies ({len(cookies)}):")
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
        value_preview = cookie['value'][:50] + '...' if len(cookie['value']) > 50 else cookie['value']
        print(f"  {cookie['name']}: {value_preview}")

    with open('cookies.json', 'w') as f:
        json.dump(cookies_dict, f, indent=2)
    print("\n✓ Saved to cookies.json")

    # Test accessing main page
    print("\n" + "="*60)
    print("Testing access to main site...")
    print("="*60)
    driver.get("https://adtreferral.com/")
    time.sleep(2)
    print(f"Main page URL: {driver.current_url}")
    print(f"Page title: {driver.title}")

    # Check for logout link as sign of being logged in
    try:
        logout_link = driver.find_element(By.XPATH, "//*[contains(text(), 'Logout') or contains(text(), 'Log Out') or contains(text(), 'Sign Out')]")
        print("✓ LOGGED IN - Found logout link!")
    except:
        print("⚠ Could not find logout link - may not be logged in")

except Exception as e:
    print(f"\nError: {e}")

finally:
    print("\nKeeping browser open for 10 seconds so you can see the result...")
    time.sleep(10)
    driver.quit()
    print("Browser closed.")
