from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def __get_default_chrome_options():
    chrome_options = webdriver.ChromeOptions()

    lambda_options = [
        '--autoplay-policy=user-gesture-required',
        '--disable-background-networking',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-breakpad',
        '--disable-client-side-phishing-detection',
        '--disable-component-update',
        '--disable-default-apps',
        '--disable-dev-shm-usage',
        '--disable-domain-reliability',
        '--disable-extensions',
        '--disable-features=AudioServiceOutOfProcess',
        '--disable-hang-monitor',
        '--disable-ipc-flooding-protection',
        '--disable-notifications',
        '--disable-offer-store-unmasked-wallet-cards',
        '--disable-popup-blocking',
        '--disable-print-preview',
        '--disable-prompt-on-repost',
        '--disable-renderer-backgrounding',
        '--disable-setuid-sandbox',
        '--disable-speech-api',
        '--disable-sync',
        '--disk-cache-size=33554432',
        '--hide-scrollbars',
        '--ignore-gpu-blacklist',
        '--ignore-certificate-errors',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-default-browser-check',
        '--no-first-run',
        '--no-pings',
        '--no-sandbox',
        '--no-zygote',
        '--password-store=basic',
        '--use-gl=swiftshader',
        '--use-mock-keychain',
        '--single-process',
        '--headless']

    for argument in lambda_options:
        chrome_options.add_argument(argument)          

    chrome_options.binary_location = "/opt/headless-chromium" 

    return chrome_options

def hello(event, context):
    options=__get_default_chrome_options()

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    driver.get('https://www.apple.com/')
    body = f"Headless Chrome Initialized, Page title: {driver.title}"

    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": body
    }

    return response
