from playwright.sync_api import Page, expect
from lib.model_definition import User, Peep
from seeds.seed_db import seed_database

# Tests for your routes go here

def test_redirect_home(page, test_web_address):
    page.goto(test_web_address)
    assert page.url == f'http://{test_web_address}/home'

def test_home_page(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/home')

    title = page.locator('.navbar-brand')
    expect(title).to_have_text('Chitter')

    peeps = page.locator('.peep')
    expect(peeps).to_have_count(6)

def test_search_user(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/home')

    search_bar = page.locator('#search-user')
    search_bar.fill('twalker')

    search_button = page.locator('#search-button')
    search_button.click()

    peeps = page.locator('.peep')
    expect(peeps).to_have_count(2)

def test_search_user_not_found(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/home')

    search_bar = page.locator('#search-user')
    search_bar.fill('not_a_user')

    search_button = page.locator('#search-button')
    search_button.click()

    error_msg = page.locator('#error-msg')
    expect(error_msg).to_have_text('@not_a_user could not be found.')

def test_sign_up_form_displays(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/home')

    signup_btn = page.locator('#signup-button')
    signup_btn.click()

    page.screenshot(path='screenshot.png', full_page=True)

    boxes = page.locator('.mb-3')
    expect(boxes).to_have_count(5)

def test_sign_up_fail(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/signup')

    email = page.locator('#email')
    email.fill('twalker@gmail.com')

    username = page.locator('#username')
    username.fill('twalker')

    password = page.locator('#password')
    password.fill('Password@1')

    name = page.locator('#name')
    name.fill('Tom Walker')

    password_confirmation = page.locator('#password-confirm')
    password_confirmation.fill('Password@2')

    submit = page.locator('#sign-up-button')
    submit.click()

    page.screenshot(path='screenshot.png', full_page=True)

    error_msgs = page.locator('.text-danger')
    expect(error_msgs).to_have_count(3)