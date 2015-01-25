#!/usr/bin/python3

from html.parser import HTMLParser
import urllib.request
import webbrowser
import datetime

LANG = 'en'
TMPFILE = '/tmp/watdo.html'

class Parser(HTMLParser):
    def __init__(self):
        super(Parser, self).__init__()
        self.handle_next_h2 = False
        self.handle_until_h2 = False
        self.result = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if self.handle_until_h2:
            if tag == 'h2':
                self.handle_until_h2 = False
            else:
                astr = ' '.join(map(lambda k: '%s=%r' % (k, attrs[k]), attrs))
                self.result += '<%s %s>' % (tag, astr) if astr else '<%s>' % tag
        else:
            if 'id' in attrs and attrs['id'] == 'Holidays_and_observances':
                self.handle_next_h2 = True

    def handle_endtag(self, tag):
        if self.handle_until_h2:
            self.result += '</%s>' % tag
        elif self.handle_next_h2 and tag == 'h2':
            self.handle_next_h2 = False
            self.handle_until_h2 = True

    def handle_data(self, data):
        if self.handle_until_h2:
            self.result += data.replace('\\n', '\n')

parser = Parser()
today = datetime.date.today().strftime('%B_%d')
parser.feed(str(urllib.request.urlopen('http://%s.wikipedia.org/wiki/%s' % (LANG,today)).read()))
with open(TMPFILE, 'w') as f:
    print('''<html lang='%s'>
        <head>
            <title>watdo</title>
            <meta charset='utf-8' />
            <base href='http://%s.wikipedia.org/' />
            <style>
                html { font-family: sans-serif; }
                h1 { margin: 0px; font-size: 1.5em; }
            </style>
        </head>
        <body>
            <h1>wat do?</h1>
            %s
        </body>
    </html>''' % (LANG, LANG, parser.result), file=f)
webbrowser.open(TMPFILE)
