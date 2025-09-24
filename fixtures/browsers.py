from typing import Any, Generator

import allure
import pytest
from _pytest.fixtures import SubRequest
from playwright.sync_api import Page, Playwright

from pages.authentication.registration_page import RegistrationPage


@pytest.fixture
def chromium_page(request: SubRequest, playwright: Playwright) -> Generator[Page, Any, None]:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir='./videos')
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')
    browser.close()
    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)

@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    registration_page = RegistrationPage(page)
    registration_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")
    registration_page.registration_form.fill(email="user.name@gmail.com", username="username", password="password")
    registration_page.click_registration_button()
    context.storage_state(path="browser-state.json")
    browser.close()


@pytest.fixture(scope="function")
def chromium_page_with_state(request: SubRequest, initialize_browser_state, playwright: Playwright) -> Generator[Page, Any, None]:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json", record_video_dir='./videos')
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    yield page
    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')
    browser.close()
    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)