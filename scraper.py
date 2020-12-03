#! /usr/bin/env python3
# coding: utf-8

''' The purpose of this module is to scrape the content of
    the http://books.toscrape.com/ website.
'''

from urllib.request import urljoin

from book import Book
from category import Category
from utils import connect_with_bs4, progress_monitor, FileIO

##################################################
# Scraper
##################################################


class Scraper():
    """ The purpose of this class is to collect
        and store the whole books of the website

    Attributes
    ----------
    site_url : str
    categories : list
    links : list
    num_books : int

    Methods
    -------
    collect()
        connect to the given url and collect the data
    """

    def __init__(self, url):
        self.site_url = url
        self.links = []
        self.categories = []
        self.num_books = 0

        if(url is not None):
            self.collect()

    def collect(self):
        """ Connect to the home-page and grab the information """

        self._soup = connect_with_bs4(self.site_url)

        self.num_books = self.__scrap_num_books()
        self.links = self.__scrap_links()
        self.categories = self.__scrap_categories()

    # --- PRIVATE METHODS ---

    def __scrap_num_books(self):
        try:
            return int(self._soup.select('form strong')[0].string)
        except Exception:
            return 0

    def __scrap_links(self):
        try:
            ahrefs = self._soup.select('div[class=side_categories] li ul a')
            base_url = urljoin(self.site_url, '.')
            return [(urljoin(base_url, x.attrs['href']), x.string.strip())
                    for x in ahrefs]
        except Exception:
            return []

    def __scrap_categories(self, to_csv=False):

        FileIO.init_root('data')
        categories = []

        progress_monitor.allbooks_init(self.num_books, self.site_url)

        for link in self.links:

            progress_monitor.category_update(
                    len(categories),
                    len(self.links),
                    link[1])

            category = Category(link[0])
            categories.append(category)

            FileIO.open_category(category.name)
            category.write_csv()
            FileIO.close_category()

        return categories


##################################################
# Main
##################################################


if __name__ == '__main__':

    # # play with Book class
    # prod_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    # book = Book(prod_url)
    # book.write_csv('OnProductAppend')
    # book.collect()
    # book.write_csv('OnProductAlone', 'w')
    # book.write_csv('OnProductAlone', 'w')
    # book.write_csv('OnProductAppend')

    # # play with Category class
    # cat_url = 'http://books.toscrape.com/catalogue/category/books/fiction_10/index.html'
    # cat1 = Category(cat_url)
    # cat1.write_csv('cat1')
    # cat1.write_csv('cat1')

    # play with Scraper class
    site_url = 'http://books.toscrape.com'
    site = Scraper(site_url)
