#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import unittest
from marketingparser.website import PostInfo, DigitalBuzz, CreativeGuerrilla, CreativeCriminals, \
                                    ViralBlog, ImprovEverywhere, OnTheGroundLookingUp


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

    def test_viralblog(self):
        website = ViralBlog()
        self.assertEqual(len(website.load_page(0)), 12)
        self.assertTrue(website.load_post('http://www.viralblog.com/user-created-content/the-best-fan-made-game-of-thrones-credits/'))
        self.assertEqual(website.get_date(), datetime.date(2014, 6, 24))
        self.assertEqual(website.get_title(), 'The Best Fan-Made Game Of Thrones Credits')
        self.assertEqual(website.get_author(), 'Marion aan \'t Goor')
        self.assertEqual(website.get_category(), 'User Created Content')
        self.assertTrue(website.get_text().startswith('We all know Game of Thrones has'))

    def test_improveverywhere(self):
        website = ImprovEverywhere()
        self.assertEqual(len(website.load_page(0)), 5)
        self.assertTrue(website.load_post('http://improveverywhere.com/2014/04/01/spider-man-in-real-life/'))
        self.assertEqual(website.get_date(), datetime.date(2014, 4, 1))
        self.assertEqual(website.get_title(), 'Spider-Man In Real Life')
        self.assertEqual(website.get_author(), 'Charlie')
        self.assertEqual(website.get_category(), '')
        self.assertGreater(website.get_text().find('For our latest mission, we brought Spider-Man'), 0)

    def test_onthegroundlookingup(self):
        website = OnTheGroundLookingUp()
        self.assertEqual(len(website.load_page(0)), 10)
        self.assertTrue(website.load_post('http://www.onthegroundlookingup.com/2013/01/tbs-goes-tear-off-for-new-nerd-show.html'))
        self.assertEqual(website.get_date(), datetime.date(2013, 1, 24))
        self.assertEqual(website.get_title(), 'TBS Goes Tear Off For New Nerd Show')
        self.assertEqual(website.get_author(), 'Sam Ewen')
        self.assertEqual(website.get_category(), 'Advertising, Games, Guerrilla, Television')
        self.assertTrue(website.get_text().startswith('I am always a fan of the Tear-Off campaign'))


if __name__ == '__main__':
    unittest.main()
