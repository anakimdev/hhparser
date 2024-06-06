from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.apies.company_info.configs import COMMAND_EXECUTOR

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Remote(
    command_executor= COMMAND_EXECUTOR,
    options=options,
)
