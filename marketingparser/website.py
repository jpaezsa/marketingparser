# -*- coding: utf-8 -*-

import datetime
import json
import logging
import re
import urllib2
from bs4 import BeautifulSoup

DIGITS_ONLY = re.compile(r'\d+')
LINE_BREAK = re.compile(r'[\r\n]+')
TIMEOUT = 10
RETRY_COUNT = 10

TWEET_COUNT = 'http://urls.api.twitter.com/1/urls/count.json?url=%s'
FB_COUNT = 'https://graph.facebook.com/fql?q=select%%20like_count%%20from%%20link_stat%%20where%%20url=%%22%s%%22'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def urlopen(url):
    """
    Load specified url resource, retrying on error.
    """
    tries = 0
    response = None
    while not response and tries < RETRY_COUNT:
        try:
            if tries > 0:
                logger.warning('Retry #%d for "%s"' % (tries, url))
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            con = urllib2.urlopen(req, timeout=TIMEOUT)
            response = con.read()
        except StandardError:
            pass
        finally:
            tries += 1
    if not response:
        raise IOError('Failed to open url: %s' % url)
    return response


class PostInfo:
    """
    Information about a blog post.
    """

    def __init__(self):
        self.date = None
        self.title = ''
        self.author = ''
        self.rating = ''
        self.category = ''
        self.media = ''
        self.comment_count = ''
        self.tweet_count = ''
        self.fb_count = ''
        self.text = ''
        self.comments = ''

    def __unicode__(self):
        return '  ' + str(self.date) + ' by ' + self.author + \
            '\n  Rating: ' + self.rating + \
            '\n  Category: ' + self.category + \
            '\n  Title: ' + self.title + \
            '\n  Comments/twitter/fb: ' + self.comment_count + ' ' + self.tweet_count + ' ' + self.fb_count + \
            '\n  Has media: ' + self.media + \
            '\n  ' + self.text + \
            '\n  Comments: ' + self.comments


class Website:
    """
    Parsing methods for specific website.
    """

    def __init__(self):
        self.url = ''
        self.post_url = ''

    def get_page_url(self, page_num):
        """
        Construct page url based on its number.
        """
        return ''

    def load_page(self, post_from):
        """
        Load a list of post urls on a page, starting from specified post index.
        """
        return []

    def load_post(self, url):
        """
        Load and parse a post, returning True on success, False otherwise.
        """
        return False

    def get_title(self):
        return ''

    def get_date(self):
        return None

    def get_author(self):
        return ''

    def get_rating(self):
        return ''

    def get_category(self):
        return ''

    def has_media(self):
        return ''

    def get_comment_count(self):
        return '0'

    def get_tweet_count(self):
        try:
            tweets = json.loads(urlopen(TWEET_COUNT % self.post_url))
            return str(tweets['count'])
        except StandardError:
            return ''

    def get_fb_count(self):
        try:
            likes = json.loads(urlopen(FB_COUNT % self.post_url))
            return str(likes['data'][0]['like_count'])
        except StandardError:
            return ''

    def get_text(self):
        return ''

    def get_comments(self):
        return ''

    def get_post_info(self):
        info = PostInfo()
        info.title = self.get_title()
        logger.info(u'Processing "%s"...' % info.title)
        info.date = self.get_date()
        info.author = self.get_author()
        info.rating = self.get_rating()
        info.category = self.get_category()
        info.media = self.has_media()
        info.text = self.get_text()
        info.comment_count = self.get_comment_count()
        info.tweet_count = self.get_tweet_count()
        info.fb_count = self.get_fb_count()
        info.comments = self.get_comments()
        return info


class DigitalBuzz(Website):

    RATING = re.compile(r'average: ([\d.]+)')

    def __init__(self):
        self.url = 'http://www.digitalbuzzblog.com'
        self.filename = 'digitalbuzzblog.csv'
        self.posts_per_page = 15
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%a, %b %d, %Y').date()

    def get_page_url(self, page_num):
        return self.url if page_num == 0 else \
            '%s/page/%d' % (self.url, page_num + 1)

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        links = soup.find(id='centercol').find_all('a', rel='bookmark')
        return [l['href'] for l in links][from_index:]

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(class_='post box')
        self.comments = self.soup.find(id='social-tabs-comments')
        return True if self.post else False

    def get_title(self):
        return self.post.h2.a.text.strip()

    def get_date(self):
        return self.parse_date(
            self.post.find(class_='date-comments').td.text.strip()
        )

    def get_author(self):
        return self.post.find(class_='author_info').h3.text.replace('Posted by:', '').strip()

    def get_rating(self):
        rating_match = DigitalBuzz.RATING.search(
            self.post.find(class_='date-comments').find(class_='post-ratings').text)
        return rating_match.group(1) if rating_match else ''

    def has_media(self):
        media = self.post.find('img')
        if not media:
            media = self.post.find('video')
        return '1' if media else '0'

    def get_comment_count(self):
        count = self.comments.find(class_='social-wordpress')
        return DIGITS_ONLY.search(count.span.text).group(0).strip() if count else '0'

    def get_text(self):
        containers = self.post.find(class_='entry').find_all('p')
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub('', p) for p in paragraphs]).strip()

    def get_comments(self):
        containers = self.comments.find_all(name='li', class_='wordpress')
        comments = [c.find(class_='social-comment-body').text.strip() for c in containers]
        return ' '.join([LINE_BREAK.sub('', c) for c in comments]).strip()


class CreativeGuerrilla(Website):

    def __init__(self):
        self.url = 'http://www.creativeguerrillamarketing.com/'
        self.filename = 'creativeguerrillamarketing.csv'
        self.posts_per_page = 10
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%B %d, %Y').date()

    def get_page_url(self, page_num):
        return self.url if page_num == 0 else \
            '%s/page/%d' % (self.url, page_num + 1)

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        thumbnails = soup.find_all(class_='post-thumbnail')
        if thumbnails:
            return [t.find('a')['href'] for t in thumbnails][from_index:]
        else:
            return []

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(id='post-content')
        self.comments = self.soup.find(id='disqus_thread')
        return True if self.post else False

    def get_title(self):
        return self.soup.find(class_='page-title').text.strip()

    def get_date(self):
        return self.parse_date(
            self.soup.find(class_='meta-date').text.strip()
        )

    def get_author(self):
        return self.soup.find(class_='meta-author').text.strip()

    def get_category(self):
        cats = self.soup.find(class_='meta-cats')
        return cats.find('a').text.strip() if cats else ''

    def has_media(self):
        media = self.post.find('img')
        if not media:
            media = self.post.find('video')
        return '1' if media else '0'

    def get_comment_count(self):
        count = self.comments.find(class_='comment-count')
        return DIGITS_ONLY.search(count.text).group(0).strip() if count else '0'

    def get_text(self):
        containers = self.post.find_all('p')
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub('', p) for p in paragraphs]).strip().replace('|', '')

    def get_comments(self):
        comments = self.comments.find_all(class_='post-message')
        return ' '.join([LINE_BREAK.sub('', c.text) for c in comments]).strip().replace('|', '')


class CreativeCriminals(Website):

    STATIC_PAGE_COUNT = 8

    def __init__(self):
        self.url = 'http://creativecriminals.com'
        self.filename = 'creativecriminals.csv'
        self.posts_per_page = 10
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()

    def get_page_url(self, page_num):
        return '%s/sitemap.xml' % self.url if page_num == 0 \
            else '%s/404' % self.url

    def load_page(self, post_from):
        url = self.get_page_url(0)
        soup = BeautifulSoup(urlopen(url))
        locs = soup.find_all('loc')
        links = []
        for l in locs[CreativeCriminals.STATIC_PAGE_COUNT + post_from:]:
            # these are companies' and members' pages
            if l.text.startswith('http://creativecriminals.com//'):
                break
            links.append(l.text)
        return links

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(id='content')
        return True if self.post else False

    def get_title(self):
        return self.post.h1.span.text.strip()

    def get_date(self):
        date = self.post.find(class_='date')
        return self.parse_date(date.span['content']) if date else ''

    def get_author(self):
        author = self.post.find(class_='author')
        return author.a.text.strip() if author else ''

    def get_rating(self):
        loves = self.post.h1.find(class_='loves')
        return loves.text.strip() if loves else ''

    def get_category(self):
        industry = self.post.find(class_='industry')
        return industry.a.text.strip() if industry else ''

    def has_media(self):
        media = self.post.find('img')
        if not media:
            media = self.post.find('video')
        return '1' if media else '0'

    def get_comment_count(self):
        comments = self.post.find_all(class_='comment_div')
        return str(len(comments))

    def get_text(self):
        containers = self.post.find(itemprop='articleBody').find_all('p')
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub(' ', p) for p in paragraphs]).strip()

    def get_comments(self):
        containers = self.post.find_all(class_='comment_div')
        comments = [c.find(class_='comment_text').text.strip() for c in containers]
        return ' '.join([LINE_BREAK.sub(' ', c) for c in comments]).strip()


class ViralBlog(Website):

    DATE = re.compile(r'[\d/]+')

    def __init__(self):
        self.url = 'http://www.viralblog.com/'
        self.filename = 'viralblog.csv'
        self.posts_per_page = 12
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        date_match = ViralBlog.DATE.search(str_date)
        if date_match:
            return datetime.datetime.strptime(date_match.group(0), '%d/%m/%Y').date()
        else:
            return None

    def get_page_url(self, page_num):
        return self.url if page_num == 0 else \
            '%s/page/%d' % (self.url, page_num + 1)

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        thumbs = soup.find_all(class_='item-list-small')
        links = [thumb.find('a') for thumb in thumbs]
        return [l['href'] for l in links][from_index:]

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(id='single-post')
        self.pre_post = self.post.find(class_='pre-post')
        return True if self.post else False

    def get_title(self):
        return self.post.find('h1').text.strip()

    def get_date(self):
        return self.parse_date(
            self.pre_post.find(class_='date').text.strip()
        )

    def get_author(self):
        return self.pre_post.find(class_='author').a.span.text.strip()

    def get_category(self):
        return self.pre_post.find(class_='category').a.span.text.strip()

    def get_text(self):
        containers = self.post.find(class_='post-all').find_all(['p', 'h2', 'h3'])
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub('', p) for p in paragraphs]).strip()


class ImprovEverywhere(Website):

    def __init__(self):
        self.url = 'http://improveverywhere.com/'
        self.filename = 'improveverywhere.csv'
        self.posts_per_page = 5
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%B %d, %Y').date()

    def get_page_url(self, page_num):
        return self.url if page_num == 0 else \
            '%s/page/%d' % (self.url, page_num + 1)

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        thumbs = soup.find_all('h2', class_='entry-title')
        links = [thumb.find('a') for thumb in thumbs]
        return [l['href'] for l in links][from_index:]

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(class_='type-post')
        self.meta = self.soup.find(class_='entry-meta')
        return True if self.post else False

    def get_title(self):
        return self.post.find('h1', class_='entry-title').text.strip()

    def get_date(self):
        return self.parse_date(
            self.meta.find(class_='entry-date').text.strip()
        )

    def get_author(self):
        return self.meta.find(class_='author').a.text.strip()

    def get_text(self):
        containers = self.post.find(class_='entry-content').find_all(['p', 'h2', 'h3'])
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub('', p) for p in paragraphs]).strip()


class OnTheGroundLookingUp(Website):

    def __init__(self):
        self.url = 'http://www.onthegroundlookingup.com/'
        self.filename = 'onthegroundlookingup.csv'
        self.posts_per_page = 10
        self.soup = None
        self.post = None
        self.comments = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%d %B %Y').date()

    def get_page_url(self, page_num):
        return self.url if page_num == 0 else \
            '%s/page/%d' % (self.url, page_num + 1)

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        thumbs = soup.find_all('h3', class_='entry-header')
        links = [thumb.find('a') for thumb in thumbs]
        return [l['href'] for l in links][from_index:]

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(id='alpha-inner')
        return True if self.post else False

    def get_title(self):
        return self.post.find('h3', class_='entry-header').text.strip()

    def get_date(self):
        return self.parse_date(
            self.post.find('h2', class_='date-header').text.strip()
        )

    def get_author(self):
        return 'Sam Ewen'

    def get_category(self):
        footer = self.post.find(class_='post-footers')
        cats = [cat.text.strip() for cat in footer.find_all('a')] if footer else []
        return ', '.join(cats) if cats else ''

    def get_text(self):
        containers = self.post.find(class_='entry-body').find_all(['p', 'h2', 'h3'])
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub('', p) for p in paragraphs]).strip()


class ThousandHeads(Website):

    BLOG_LINK = re.compile('^http://1000heads.com/\d{4}/')

    def __init__(self):
        self.url = 'http://1000heads.com'
        self.filename = '1000heads.csv'
        self.posts_per_page = 10
        self.soup = None
        self.post = None

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%d %B %Y').date()

    def get_page_url(self, page_num):
        return '%s/sitemap.xml' % self.url if page_num == 0 \
            else '%s/404' % self.url

    def load_page(self, post_from):
        url = self.get_page_url(0)
        soup = BeautifulSoup(urlopen(url))
        locs = soup.find_all('loc')
        links = []
        for l in locs[post_from:]:
            # skip static pages
            if ThousandHeads.BLOG_LINK.match(l.text):
                links.append(l.text)
        return links

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(class_='type-post')
        self.meta = self.post.find(class_='blog-meta') if self.post else None
        return True if self.post else False

    def get_title(self):
        return self.meta.h2.a.text.strip()

    def get_date(self):
        author_and_date = self.meta.find_all('i')
        return self.parse_date(author_and_date[1].text.strip()) if author_and_date else ''

    def get_author(self):
        author_and_date = self.meta.find_all('i')
        return author_and_date[0].text.strip() if author_and_date else ''

    def get_text(self):
        containers = self.post.find_all('p', recursive=False)
        paragraphs = [c.text.strip() or '' for c in containers]
        return ' '.join([LINE_BREAK.sub(' ', p) for p in paragraphs]).strip()


class GuerrillaComm(Website):

    BLOG_LINK = re.compile('^http://blog.guerrillacomm.com/\d{4}/.+html$')

    def __init__(self):
        self.url = 'http://blog.guerrillacomm.com'
        self.filename = 'guerrillacomm.csv'
        self.posts_per_page = 10
        self.soup = None
        self.post = None
        self.next_url = '%s/search?updated-max=2015-01-01T00:00:00-04:00&max-results=10' % self.url

    def parse_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%B %d, %Y').date()

    def get_page_url(self, page_num):
        return self.next_url

    def load_page(self, post_from):
        page_num = post_from / self.posts_per_page
        from_index = post_from % self.posts_per_page
        url = self.get_page_url(page_num)
        soup = BeautifulSoup(urlopen(url))
        next_url_container = soup.find(id='blog-pager-older-link')
        self.next_url = next_url_container.a['href'] if next_url_container else '%s/404' % self.url
        thumbs = soup.find_all('h3', class_='post-title')
        links = [thumb.find('a') for thumb in thumbs]
        return [l['href'] for l in links][from_index:]

    def load_post(self, url):
        self.post_url = url
        self.soup = BeautifulSoup(urlopen(url))
        self.post = self.soup.find(class_='blog-posts')
        return True if self.post else False

    def get_title(self):
        return self.post.find('h3', class_='post-title').text.strip()

    def get_date(self):
        date = self.post.find('h2', class_='date-header')
        return self.parse_date(date.text.strip()) if date else ''

    def get_author(self):
        author = self.post.find(class_='post-author')
        return author.find('span', itemprop='name').text.strip() if author else ''

    def get_category(self):
        cat_container = self.post.find(class_='post-labels')
        cats = [cat.text.strip() for cat in cat_container.find_all('a')] if cat_container else []
        return ', '.join(cats) if cats else ''

    def get_text(self):
        body = self.post.find(class_='post-body')
        return LINE_BREAK.sub(' ', body.text.strip()) if body else '' 
