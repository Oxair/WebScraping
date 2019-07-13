from bs4 import BeautifulSoup
import re
from locators.books_locators import BookLocator
import logging

logger = logging.getLogger('scraping.book_parser')

class BookParser:

    RATINGS = {
        'One' : 1,
        'Two' : 2,
        'Three' : 3,
        'Four' : 4,
        'Five' : 5
    }

    def __init__(self, parent):
        logger.debug(f'New book parser created from "{parent}".')
        self.parent = parent

    def __repr__(self):
        return f'<Book {self.name}, ${self.price}, ({self.rating} stars)>'

    @property
    def name(self):
        logger.debug('Finding book name...')
        locator = BookLocator.NAME_LOCATOR
        item_name = self.parent.select_one(locator).attrs['title']
        logger.debug(f'Found book name, "{item_name}".')
        return item_name

    @property
    def link(self):
        logger.debug('Finding book link...')
        locator = BookLocator.LINK_LOCATOR
        item_link = self.parent.select_one(locator).attrs['href']
        logger.debug(f'Found book link, "{item_link}".')
        return item_link

    @property
    def price(self):
        logger.debug('Finding book price...')
        locator = BookLocator.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string

        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        float_price = float(matcher.group(1))
        logger.debug(f'Found book price, "{float_price}".')
        return float_price

    @property
    def rating(self):
        logger.debug('Finding book rating...')
        locator = BookLocator.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)
        classes = star_rating_element.attrs['class']
        rating_classes = [r for r in classes if r != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_classes[0])
        logger.debug(f'Found book rating, "{rating_number}".')
        return rating_number