# -*- coding: utf-8 -*-

import codecs
import logging
import os.path

SEP = '|'
BASE_DIR = 'data'
ENCODING = 'utf-8'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Writer:
    """
    Post writer.
    """

    def __init__(self, website):
        self.filename = website.filename
        self.page = []
        self.page_size = website.posts_per_page
        self.post_count = 0

    def save(self, post):
        pass

    def write_header(self):
        pass

    def flush(self):
        pass


class MemoryWriter(Writer):
    """
    Saves posts to in-memory array.
    """

    def __init__(self, website):
        Writer.__init__(self, website)

    def save(self, post):
        self.page.append(post)
        self.post_count += 1


class CSVWriter(Writer):
    """
    Saves posts to a CSV file.
    """

    def __init__(self, website):
        Writer.__init__(self, website)

    def save(self, post):
        self.page.append(post)
        self.post_count += 1
        if len(self.page) == self.page_size:
            self.flush()

    def write_header(self):
        f = codecs.open(os.path.join(BASE_DIR, self.filename), 'w', ENCODING)
        f.write(SEP.join(
            ('Date', 'Title', 'Author', 'Rating', 'Category', 'Media', 'Comment#',
             'Tweet#', 'FB#', 'Text', 'Comments')))
        f.write('\n')
        f.close()

    def flush(self):
        f = codecs.open(os.path.join(BASE_DIR, self.filename), 'a', ENCODING)
        for p in self.page:
            f.write(SEP.join(
                (str(p.date), p.title, p.author, p.rating, p.category, p.media, p.comment_count,
                p.tweet_count, p.fb_count, p.text, p.comments)))
            f.write('\n')
        f.close()
        logger.info('Saved %d posts, total %d...' % (len(self.page), self.post_count))
        self.page = []
