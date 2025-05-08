import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="module")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_user_booking_flow(browser):
    # 1. Go to home page
    browser.get("http://localhost:5000/")

    # 2. Fill in email and submit
    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys("john@simplylift.co")
    email_input.send_keys(Keys.RETURN)

    # 3. Check Points available == 13
    points_text = browser.find_element(By.XPATH, "//body").text
    assert "Points available: 13" in points_text

    # 4. Check Spring Festival competition info
    body_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Spring Festival" in body_text
    assert "Date: 2026-03-27 10:00:00" in body_text
    assert "Number of Places: 25" in body_text

    # 5. Click on Book Places for Spring Festival
    book_links = browser.find_elements(By.LINK_TEXT, "Book Places")
    assert len(book_links) == 1
    book_links[0].click()

    # 6. On booking page: book 4 places
    places_input = browser.find_element(By.ID, "places")
    places_input.clear()
    places_input.send_keys("4")

    submit_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # 7. After purchase, verify redirected and values updated
    updated_body_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Great, booking complete!" in updated_body_text
    assert "Points available: 9" in updated_body_text  # 13 - 4 = 9
    assert "Number of Places: 21" in updated_body_text  # 25 - 4 = 21
