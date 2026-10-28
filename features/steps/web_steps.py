from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

FIELD_IDS = {"Id": "id", "Name": "name", "Description": "description",
             "Price": "price", "Available": "available", "Category": "category"}


@when('I visit the "{page_name}"')
def step_visit_page(context, page_name):
    assert page_name == "Home Page", f"Unknown page: {page_name}"
    context.driver.get(context.base_url + "/")


@when('I press the "{button_text}" button')
@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    button = context.driver.find_element(By.XPATH, f"//button[normalize-space()='{button_text}']")
    button.click()


@when('I set the "{field_name}" to "{value}"')
def step_set_field(context, field_name, value):
    element = context.driver.find_element(By.ID, FIELD_IDS[field_name])
    element.clear()
    element.send_keys(value)


@when('I change "{field_name}" to "{value}"')
def step_change_field(context, field_name, value):
    step_set_field(context, field_name, value)


@when('I select "{value}" in the "{field_name}" dropdown')
def step_select_dropdown(context, value, field_name):
    from selenium.webdriver.support.ui import Select
    Select(context.driver.find_element(By.ID, FIELD_IDS[field_name])).select_by_visible_text(value)


@when('I copy the "{field_name}" field')
def step_copy_field(context, field_name):
    context.copied_value = context.driver.find_element(By.ID, FIELD_IDS[field_name]).get_attribute("value")


@when('I paste the "{field_name}" field')
def step_paste_field(context, field_name):
    context.driver.find_element(By.ID, FIELD_IDS[field_name]).send_keys(context.copied_value)


@then('I should see "{name}" in the results')
def step_see_name_in_results(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "search_results"), name))
    assert found, f"Expected {name!r} in search results"


@then('I should not see "{name}" in the results')
def step_not_see_name_in_results(context, name):
    results = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, "search_results")))
    assert name not in results.text, f"Did not expect {name!r} in search results"


@then('I should see the message "{message}"')
def step_see_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "flash_message"), message))
    assert found, f"Expected message {message!r}"


@then('I should see "{value}" in the "{field_name}" field')
def step_see_value_in_field(context, value, field_name):
    actual = context.driver.find_element(By.ID, FIELD_IDS[field_name]).get_attribute("value")
    assert actual == value, f"Expected {field_name}={value!r}, got {actual!r}"


@then('I should see "{value}" in the "{field_name}" dropdown')
def step_see_value_in_dropdown(context, value, field_name):
    actual = context.driver.find_element(By.ID, FIELD_IDS[field_name]).get_attribute("value")
    assert actual.lower() == value.lower(), f"Expected {field_name}={value!r}, got {actual!r}"
