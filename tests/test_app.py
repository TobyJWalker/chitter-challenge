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

    page.screenshot(path='screenshot.png', full_page=True)

    title = page.locator('.navbar-brand')
    expect(title).to_have_text('Chitter')

    peeps = page.locator('.peep')
    expect(peeps).to_have_count(6)