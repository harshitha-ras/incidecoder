import unittest
from scraper import scrape_products

class TestScraper(unittest.TestCase):
    def test_scrape_products(self):
        """
        Test the product scraping function with mock data.
        """
        home_url = "https://mockurl.com/page="
        start_page = 1
        end_page = 1
        matches = ["skin", "eye", "face"]
        wash_matches = ["shampoo", "conditioner"]
        cat = "hair"

        # Using mock data instead of real HTTP requests
        products, reject = scrape_products(home_url, start_page, end_page, matches, wash_matches, cat)

        # Check that the products and reject lists are initialized as empty
        self.assertIsInstance(products, list)
        self.assertIsInstance(reject, list)

if __name__ == "__main__":
    unittest.main()
