#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import unittest
from website import PostInfo, DigitalBuzz, CreativeGuerrilla, CreativeCriminals


class WebsiteTestCase(unittest.TestCase):

    def test_digitalbuzz(self):
        website = DigitalBuzz()
        self.assertEqual(len(website.load_page(0)), 15)
        self.assertTrue(website.load_post('http://www.digitalbuzzblog.com/coca-cola-cokedrones-bring-happiness-by-air/'))

        self.assertEqual(website.get_date(), datetime.date(2014, 5, 11))
        self.assertEqual(website.get_title(), 'Coca-Cola: CokeDrones Bring Happiness By Air')
        self.assertEqual(website.get_author(), 'Aden Hepburn')
        self.assertEqual(website.get_rating(), '3.63')
        self.assertEqual(website.get_category(), '')
        self.assertEqual(website.has_media(), '1')
        self.assertEqual(website.get_comment_count(), '1')
        self.assertGreater(website.get_tweet_count(), 160)
        self.assertGreater(website.get_fb_count(), 110)
        self.assertTrue(website.get_text().startswith('Coca-Cola is the latest company to use Drones'))
        self.assertTrue(website.get_comments().startswith('Very lame'))

    def test_creativeguerrilla(self):
        website = CreativeGuerrilla()
        self.assertEqual(len(website.load_page(0)), 10)
        self.assertTrue(website.load_post('http://www.creativeguerrillamarketing.com/guerrilla-marketing/coca-cola-phone-booth-turns-bottle-caps-currency/'))

        self.assertEqual(website.get_date(), datetime.date(2014, 5, 12))
        self.assertEqual(website.get_title(), 'Coca-Cola Phone Booth Turns Bottle Caps Into Currency')
        self.assertEqual(website.get_author(), 'Ryan Lum')
        self.assertEqual(website.get_rating(), '')
        self.assertEqual(website.get_category(), 'Guerrilla Marketing')
        self.assertEqual(website.has_media(), '1')
        # cannot parse Disqus comments
        # self.assertEqual(website.get_comment_count(), '1')
        self.assertGreater(website.get_tweet_count(), 90)
        self.assertGreater(website.get_fb_count(), 70)
        self.assertTrue(website.get_text().startswith(u'A large portion of the UAE’s population'))
        # cannot parse Disqus comments
        # self.assertTrue(website.get_comments().startswith('If they want to call again'))

    def test_creativecriminals(self):
        website = CreativeCriminals()
        self.assertGreater(len(website.load_page(0)), 100)
        self.assertTrue(website.load_post('http://creativecriminals.com/the-sunday-times/fat-cats'))

        self.assertEqual(website.get_date(), datetime.date(2014, 5, 11))
        self.assertEqual(website.get_title(), 'The Sunday Times: Fat Cats')
        self.assertEqual(website.get_author(), 'Rindert Dalstra')
        self.assertEqual(website.get_rating(), '6')
        self.assertEqual(website.get_category(), 'Media & Publishing')
        self.assertEqual(website.has_media(), '1')
        self.assertEqual(website.get_comment_count(), '1')
        self.assertGreater(website.get_tweet_count(), 0)
        self.assertGreater(website.get_fb_count(), 0)
        self.assertTrue(website.get_text().startswith('Team News, has taken a humorous approach'))
        self.assertTrue(website.get_comments().startswith('Reminds me of the Top Magazine'))


if __name__ == '__main__':
    unittest.main()
