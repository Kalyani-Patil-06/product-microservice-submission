from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(3)
    context.base_url = "http://127.0.0.1:5000"
    context.wait_seconds = 5


def after_all(context):
    if getattr(context, "driver", None):
        context.driver.quit()
