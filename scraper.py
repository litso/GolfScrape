import os
import shutil
import uuid
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger()

class Scraper:
    def __init__(self):
        self._tmp_folder = '/tmp/{}'.format(uuid.uuid4())

        if not os.path.exists(self._tmp_folder):
            os.makedirs(self._tmp_folder)

        if not os.path.exists(self._tmp_folder + '/user-data'):
            os.makedirs(self._tmp_folder + '/user-data')

        if not os.path.exists(self._tmp_folder + '/data-path'):
            os.makedirs(self._tmp_folder + '/data-path')

        if not os.path.exists(self._tmp_folder + '/cache-dir'):
            os.makedirs(self._tmp_folder + '/cache-dir')

    def __get_default_chrome_options(self):
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
            '--headless'
        ]
    
        for argument in lambda_options:
            chrome_options.add_argument(argument)          
    
        is_local = os.environ.get('IS_LOCAL', 'false') == 'true'
    
        if not is_local:
            chrome_options.binary_location = "/opt/headless-chromium"
    
        return chrome_options

    def __get_correct_height(self, url, width=1280):
        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, 1024))
        driver = webdriver.Chrome('/opt/chromedriver',chrome_options=chrome_options)
        driver.get(url)
        height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        driver.quit()
        return height

    def __wait_for(self, driver, selector, selector_type=By.CSS_SELECTOR, timeout=10):
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.support.wait import WebDriverWait

        wait = WebDriverWait(driver, 10)
        return wait.until(
            ec.presence_of_element_located((selector_type, selector)),
            timeout
        )
        
    def __wait_for_loading_to_toggle(self, driver):
        self.__wait_for(driver, '//div[not(contains(@class,"ng-hide"))]/div/div[@class="loading-indicator"]', By.XPATH)
        self.__wait_for(driver, '//div[contains(@class,"ng-hide")]/div/div[@class="loading-indicator"]', By.XPATH)
        
    def __did_load_results(self, driver):
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.support.wait import WebDriverWait

        wait = WebDriverWait(driver, 10)
        try:
            wait.until(
                ec.presence_of_element_located((By.XPATH, '//div[@class="no-results"]')),
                10
            )
            return False
        except Exception:
            # Timed out waiting for results
            return True
        
    def scrape(self, url, filename, width=1280, height=None):
        if height is None:
            height = self.__get_correct_height(url, width=width)

        chrome_options=self.__get_default_chrome_options()
        chrome_options.add_argument('--window-size={}x{}'.format(width, height))
        chrome_options.add_argument('--hide-scrollbars')

        driver = webdriver.Chrome('/opt/chromedriver',chrome_options=chrome_options)
        logger.info('Using Chromium version: {}'.format(driver.capabilities['browserVersion']))
        driver.get(url)
        
        clear_all = self.__wait_for(driver, '.search-clear-all')
        clear_all.click()

        course = self.__wait_for(driver, '//label[text()="Rancho Park"]', By.XPATH)
        course.click()

        date = self.__wait_for(driver, '//input[@type="text"]', By.XPATH)

        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys(Keys.BACKSPACE)
        date.send_keys('12/26/2020')
        
        searchButton = self.__wait_for(driver, '//Button[text()="Search"]', By.XPATH)
        searchButton.click()

        results = []
        
        self.__wait_for_loading_to_toggle(driver)
        
        if self.__did_load_results(driver):
            print("Tee Times Found")
            result = { }
            elements = driver.find_elements_by_xpath('//ul[@class="tee-time-block"]/li')
            for element in elements:
                result["course"] = element.find_element_by_css_selector('div.course span').text
                result["time"] = element.find_element_by_css_selector('span.time').text
                results.append(result)
        else:
            print("No Tee Times Found")

        driver.save_screenshot(filename)
        driver.quit()
        return results

    def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)
