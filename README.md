Marketing websites parser
===============

This is a parser for 3 marketing websites:

- digitalbuzzblog.com
- creativeguerrillamarketing.com
- creativecriminals.com

Parses all blog posts to a CSV file. Each record represents one blog post and has the following structure:

1. Date (yyyy-mm-dd)
2. Title
3. Author
4. Rating
5. Category
6. Has images / video (1 if true, 0 otherwise)
7. Comments count
8. Tweets count
9. Facebook likes count
10. Post text
11. Comments text (all comments joined together)


Installation
===============

Requires Python 2.7.x and additional libraries:

```
pip install lxml
pip install beautifulsoup4
```


Usage
===============

```
$ python parser.py -h
usage: parser.py [-h] [-f POST_FROM] [-c COUNT] sitename

positional arguments:
  sitename              name of the website to parse (digitalbuzzblog, creativecriminals, creativeguerrillamarketing)

optional arguments:
  -h, --help            show this help message and exit
  -f POST_FROM, --post_from POST_FROM
                        0-based index of the first post to parse
  -c COUNT, --count COUNT
                        number of posts to parse

```

Example #1: parse all content from Digital Buzz:

    python parser.py digitalbuzzblog
    
Example #2: parse 20 posts from Creative Criminals, starting from post # 300:

    python parser.py -f 300 -c 20 creativecriminals
    
    
All data is saved to the `data` subfolder (i.e., 'data/digitalbuzzblog.csv'). Pipe character `|` is used as a CSV separator.
