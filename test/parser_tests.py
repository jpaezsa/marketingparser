#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from parser import parse
from website import CreativeGuerrilla, CreativeCriminals
from writer import MemoryWriter


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.websites = [CreativeGuerrilla(), CreativeCriminals()]
        self.writers = [MemoryWriter(self.websites[0]), MemoryWriter(self.websites[1])]

    def test_first_page(self):
        for i in range(2):
            website = self.websites[i]
            writer = self.writers[i]
            parse(website, writer, 0, website.posts_per_page)
            self.assertEqual(len(writer.page), website.posts_per_page)
            self.assertEqual(writer.post_count, website.posts_per_page)
            third_post_title = writer.page[2].title

            writer = MemoryWriter(self.websites[i])
            parse(website, writer, 2, website.posts_per_page)
            self.assertEqual(len(writer.page), website.posts_per_page)
            self.assertEqual(writer.post_count, website.posts_per_page)
            self.assertEqual(writer.page[0].title, third_post_title)

    def test_some_page(self):
        for i in range(2):
            website = self.websites[i]
            writer = self.writers[i]
            parse(website, writer, 100, 2)
            self.assertEqual(len(writer.page), 2)

    def test_two_pages(self):
        for i in range(2):
            website = self.websites[i]
            writer = self.writers[i]
            parse(website, writer, 0, website.posts_per_page*2)
            self.assertEqual(len(writer.page), website.posts_per_page*2)

    def test_nonexisting_page(self):
        for i in range(2):
            website = self.websites[i]
            writer = self.writers[i]
            parse(website, writer, 10000, 2)
            self.assertEqual(len(writer.page), 0)
            self.assertEqual(writer.post_count, 0)


if __name__ == '__main__':
    unittest.main()
