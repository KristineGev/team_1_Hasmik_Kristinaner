from selenium.webdriver.common.by import By
from helper.general_helpers import Helper
import re
from test_data import data
from selenium.webdriver.common.keys import Keys


class Home(Helper):

    search_box = (By.ID, "searchAll")
    btn_brand = (By.XPATH, "//button[@data-test-id-facet-head-name='Brand']")
    btn_price = (By.XPATH, "//button[@data-test-id-facet-head-name='Price']")
    btn_color = (By.XPATH, "//button[@data-test-id-facet-head-name='Color']")

    chkbox_brand = (
        By.XPATH, f"//ul[@aria-labelledby='brandNameFacet']//li//a[.//span[text()='{data.brand}']]")
    chkbox_price = (
        By.XPATH, f"//ul[@aria-labelledby='priceFacet']//li//a[.//span[text()='${data.max_price:.2f} and Under']]")
    chkbox_color = (
        By.XPATH, f"//ul[@aria-labelledby='colorFacet']//li//a[.//span[text()='{data.color}']]")
    items_found = (
        By.XPATH, "//select[@id='searchSort']/ancestor::span/preceding::span[@class='ns-z' and contains(text(), 'items found')][1]")
    product_desc = (
        By.XPATH, "//*[@id='products']/article/a")

    def extract_item_count(self, text):
        match = re.search(r'(\d+)\s+items?\s+found', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def search_for_item(self, search_txt):
        self.find_and_send_keys(self.search_box, search_txt)
        self.find_and_send_keys(self.search_box, Keys.ENTER)

    def apply_filters(self, brand=None, price=None, color=None):
        if brand:
            self.hover_to_element(self.btn_brand)
            self.find_and_click(self.btn_brand)
            self.find_and_click(self.chkbox_brand)
        if price:        
            self.hover_to_element(self.btn_price)
            self.find_and_click(self.btn_price)
            self.find_and_click(self.chkbox_price)
        if color:
            self.hover_to_element(self.btn_color)
            self.find_and_click(self.btn_color)
            self.find_and_click(self.chkbox_color)

    def get_filtered_item_count(self):
        text = self.find_element(self.items_found).text
        return self.extract_item_count(text)

    def get_all_products_info(self):
        products = self.find_elements(self.product_desc)
        product_info = []
        for product in products:
            try:
                product_text = product.text
                brand = product_text.split(" - ")[0].strip()                
                price_match = re.search(r"On sale for \$(\d+\.\d{2})", product_text)
                price = float(price_match.group(1)) if price_match else None
                if not price:
                    self.test_logger.error(f"Price not found in product text: {product_text}")
                    continue

                product_info.append({
                    'brand': brand,
                    'price': price,
                    'full_text': product_text
                })
            except Exception as e:
                self.test_logger.error(f"Error extracting product info: {str(e)}")
                continue
        return product_info

    def verify_products_against_filters(self, expected_brand, max_price):
        products = self.get_all_products_info()
        mismatches = []
        self.test_logger.info(f"Verifying {len(products)} products against filters...")
        self.test_logger.info(f"Expected brand: {expected_brand}, Max price: ${max_price:.2f}")
        for i, product in enumerate(products, 1):
            errors = []
            if product['brand'].lower() != expected_brand.lower():
                errors.append(f"Brand: got '{product['brand']}'")
            if product['price'] and product['price'] > max_price:
                errors.append(f"Price: ${product['price']:.2f} > max ${max_price:.2f}")
            elif not product['price']:
                errors.append("Price: Could not extract price")
            if errors:
                mismatch_msg = f"Product {i} mismatch - {', '.join(errors)}"
                self.test_logger.error(mismatch_msg)
                mismatches.append({
                    'product': i,
                    'errors': errors,
                    'text': product['full_text']
                })
        if not mismatches:
            self.test_logger.info("All products match filters!")
            return True, []
        self.test_logger.error(f"Found {len(mismatches)} mismatches out of {len(products)}")
        return False, mismatches
