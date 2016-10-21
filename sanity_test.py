import unittest
from bs4 import BeautifulSoup
import requests
import sys
import lxml
import urllib
import os

# Needed on AG, should be commented out when running locally
# import group_urls


class P1_Sanity_Tests(unittest.TestCase):

    # This runs before every single test case
    def setUp(self):
        
        # This line should be used on the autograder
        # self.base_url = group_urls.URLS[os.environ['usernames']]
        
        # This line should be used locally
        self.base_url = "http://localhost:3000/p2gkisj6/p1"
        
        self.url = self.base_url


    def get_html(self, url):
        try:
            r = requests.get(urllib.parse.urljoin(self.url, url))
            r.raise_for_status()
        except Exception:
            r = requests.get(url)

        self.assertTrue(r.status_code != 404)
        return r.text

    def make_soup(self, url):
        return BeautifulSoup(self.get_html(url), "lxml")

    # Check to make sure the meta, head, and footer tags are present
    def test_meta_tags(self):
        html = self.get_html(self.url)
        self.assertIn("meta",  html, "Missing meta tags")
        self.assertIn("footer", html, "Missing footer tags")
        self.assertIn("head", html, "Missing head tags")
        print("Passed test tag check")

    # Check to make sure "Cool Space Shorts" is on spacejunkie's page
    def test_spacejunkie(self):
        soup = self.make_soup(self.url)
        objs = soup.find_all(id='user_albums_spacejunkie')
        self.assertTrue(objs, "Missing id user_albums_<x>")
        for obj in objs:
            new_url = obj.get('href')
            new_html = self.get_html(new_url)
            self.assertIn("Cool Space Shots", new_html, "Missing starter files")
        print("Passed test spacejunkie")

    # Check to make sure "I love sports" and "football" is on sportslovers page
    def test_sportslover(self):
        soup = self.make_soup(self.url)
        objs = soup.find_all(id='user_albums_sportslover')
        self.assertTrue(objs, 'Missing id user_album_<x>')
        for obj in objs:
            new_url = obj.get('href')
            new_html = self.get_html(new_url)
            self.assertIn("I love football", new_html, "Missing starter files")
            self.assertIn("I love sports", new_html, "Missing starter files")
        print("Passed test sportslover")

    # Check to make sure "Around the world" is on travelers page
    def test_traveler(self):
        soup = self.make_soup(self.url)
        objs = soup.find_all(id='user_albums_traveler')
        self.assertTrue(objs, 'Missing id user_album_<x>')
        for obj in objs:
            new_url = obj.get('href')
            new_html = self.get_html(new_url)
            self.assertIn("Around The World", new_html, "Missing starter files")
        print("Passed test traveler")


if __name__ == "__main__":
    unittest.main()
