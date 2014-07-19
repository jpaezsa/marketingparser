#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
from marketingparser.website import PostInfo, DigitalBuzz, CreativeGuerrilla, CreativeCriminals, \
                                    ViralBlog, ImprovEverywhere, OnTheGroundLookingUp, ThousandHeads, \
                                    GuerrillaComm
from marketingparser.writer import CSVWriter

WEBSITES = {
    'digitalbuzzblog': DigitalBuzz(),
    'creativeguerrillamarketing': CreativeGuerrilla(),
    'creativecriminals': CreativeCriminals(),
    'viralblog': ViralBlog(),
    'improveverywhere': ImprovEverywhere(),
    'onthegroundlookingup': OnTheGroundLookingUp(),
    '1000heads': ThousandHeads(),
    'guerrillacomm': GuerrillaComm()
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Parser:

    def __init__(self, website):
        self.website = website
        self.post_links = []
        self.post_from = 0
        self.current_index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current_index < len(self.post_links):
            return self.next_post()
        success = self.load(self.post_from + len(self.post_links))
        if success:
            return self.next_post()
        else:
            raise StopIteration

    def next_post(self):
        info = self.load_post(self.post_links[self.current_index])
        self.current_index += 1
        return info

    def load(self, post_from=0):
        self.post_from = post_from
        try:
            self.post_links = self.website.load_page(post_from)
            self.current_index = 0
            logger.info('Loaded %d posts from %d' % (len(self.post_links), self.post_from))
            return len(self.post_links) > 0
        except StandardError as ex:
            logger.exception('Failed to load %d posts from %d: %s' % \
                  (len(self.post_links), self.post_from, ex.message))
            return False

    def load_post(self, url):
        try:
            success = self.website.load_post(url)
            if not success:
                logger.exception('Error loading post (%s): post body not found' % url)
                return PostInfo()
            return self.website.get_post_info()
        except StandardError as ex:
            logger.exception('Error loading post (%s): %s' % (url, ex.message))
            return PostInfo()


def parse(website, writer, post_from=0, post_count=None):
    if post_from == 0:
        writer.write_header()
    feed = Parser(website)
    feed.load(post_from)
    for post in feed:
        writer.save(post)
        logger.debug('Processed %d of %s posts' % (writer.post_count, post_count or 'all'))
        if post_count and writer.post_count == post_count:
            break
    writer.flush()


def run(sitename, post_from=0, post_count=None):
    if not WEBSITES.has_key(sitename):
        logger.exception('Unsupported website: %s\nSupported are: %s' % \
              (sitename, ', '.join(WEBSITES.keys())))
        return
    website = WEBSITES[sitename]
    logger.info('Parsing "%s", %s posts starting from %d' % (website.url, post_count or 'all', post_from))
    parse(website, CSVWriter(website), post_from, post_count)


def parse_args():
    cli = argparse.ArgumentParser()
    cli.add_argument('sitename', help='name of the website to parse')
    cli.add_argument('-f', '--post_from', help='0-based index of the first post to parse', type=int, default=0)
    cli.add_argument('-c', '--count', help='number of posts to parse', type=int, default=None)
    return cli.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run(args.sitename, args.post_from, args.count)
