# #!/usr/bin/env python

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def create_driver():
    logging.info('Starting the browser...')
    options = ChromeOptions()
    # To prevent broswer activation
    options.add_argument("--headless") 
    return webdriver.Chrome(options=options)
    

# Start the browser and login with standard_user
def test_login_function(driver, user, password):
    login_url = 'https://www.saucedemo.com/'
    inventory_url = 'https://www.saucedemo.com/inventory.html'
    logging.info('Navigating to the demo page to login {}'.format(login_url))
    driver.get(login_url)
    logging.info('Login attempt, user: {},  password: {}'.format(user, password))
    driver.find_element_by_id('user-name').send_keys(user)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('login-button').click()
    logging.info('Assert in inventory page. ')
    assert inventory_url in driver.current_url
    logging.info('Login Success.')
    

def test_cart_item_addition_function(driver):
    cart_url = 'https://www.saucedemo.com/cart.html'
    items_in_cart = []
    logging.info('Adding items to cart')
    elements = driver.find_elements_by_class_name('inventory_item')
    for item in elements:
        item_name = item.find_element_by_class_name('inventory_item_name').text
        items_in_cart.append(item_name)
        item.find_element_by_class_name('btn_inventory').click()
        logging.info('Added {} to cart'.format(item_name))
    cart_element = driver.find_element_by_class_name('shopping_cart_badge')
    assert int(cart_element.text) == len(elements)
    driver.find_element_by_class_name('shopping_cart_link').click()
    logging.info('Assert in cart page. ')
    assert cart_url in driver.current_url
    for item in driver.find_elements_by_class_name('inventory_item_name'):
        assert item.text in items_in_cart
    logging.info('Add Items in cart Success.')


def test_cart_item_removal_function(driver):
    cart_url = 'https://www.saucedemo.com/cart.html'
    logging.info('Removing items from cart')
    driver.find_element_by_class_name('shopping_cart_link').click()
    assert cart_url in driver.current_url

    logging.info("Items in Cart: {}".format(len(driver.find_elements_by_class_name('cart_item'))))
    
    for item in driver.find_elements_by_class_name('cart_item'):
        item_name = item.find_element_by_class_name('inventory_item_name').text
        item.find_element_by_class_name('cart_button').click()
        logging.info('Removed {} from cart'.format(item_name))

    assert len(driver.find_elements_by_class_name('cart_item')) == 0
    logging.info('Remove Items from cart Success.')


def ui_test():
    # configuring the logging format
    FORMAT = "[%(asctime)s-%(funcName)s()] %(message)s"
    logging.basicConfig(format=FORMAT, filename='ui-logs.log', level=logging.INFO)

    driver = create_driver()
    logging.info("UI Tests started")
    username = 'standard_user'
    password = 'secret_sauce'
    
    logging.info("Begin: login testing")
    test_login_function(driver, username, password)
    logging.info("End: login testing")
    logging.info("Begin: Adding item to cart")
    test_cart_item_addition_function(driver)
    logging.info("End: Adding item to cart")
    logging.info("Begin: Removing item from cart")
    test_cart_item_removal_function(driver)
    logging.info("END: Removing item from cart")

    logging.info("UI Tests completed.")
    driver.quit()

if __name__ == "__main__":
    ui_test()