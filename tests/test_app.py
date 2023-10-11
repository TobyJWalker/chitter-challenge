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

    page.screenshot(path='screenshot.png', full_page=True)

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

def test_sign_up_form(page, test_web_address):
    seed_database()

    page.goto(f'http://{test_web_address}/signup')

    boxes = page.locator('.mb-3')
    expect(boxes).to_have_count(4)