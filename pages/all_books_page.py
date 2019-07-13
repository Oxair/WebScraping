from bs4 import BeautifulSoup
import re
import logging

from locators.all_books_page import AllBooksPageLocators
from parsers.book_parser import BookParser

logger = logging.getLogger('scrapping.all_books_page')

class AllBooksPage:
    logger.debug('Parsing page content with beautiful soup...')
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Finding all the books in the page {AllBooksPageLocators.BOOKS}.')
        return [BookParser(e) for e in self.soup.select(AllBooksPageLocators.BOOKS)]


    @property
    def page_count(self):
        logger.debug('Finding the number of available pages in catalog...')
        content = self.soup.select_one(AllBooksPageLocators.PAGER).string
        logger.info(f"Found number of catalog pages available '{content}'.")
        pattern = 'Page [0-9]+ of ([0-9]+)'
        matcher = re.search(pattern, content)
        pages = int(matcher.group(1))
        logger.debug(f'Extracted number of pages as integer "{pages}".')
        return pages