import config
from pages.home import Home
from test_data import data


def test_search_item(test_driver, test_logger):

    home_obj = Home(test_driver, test_logger)   
    home_obj.go_to_page(config.url)
    home_obj.search_for_item(data.search_text)
    home_obj.apply_filters(data.brand, data.max_price, color=None)
    result_count = home_obj.get_filtered_item_count()
    test_logger.info(f"Number of items found: {result_count}")

    all_info_matches, mismatches = home_obj.verify_products_against_filters(
        expected_brand=data.brand,
        max_price=data.max_price)

    assert all_info_matches, f"Filtered items do not match expected brand and price. Mismatches: {mismatches}"
    test_logger.info("Test completed successfully. All items match the expected filters.")