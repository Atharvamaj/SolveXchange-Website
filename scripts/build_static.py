#!/usr/bin/env python3
"""makes the pages work without running flask"""
from pathlib import Path
import re
import shutil
import json
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
IMAGE_MANIFEST = ROOT / 'static' / 'images' / 'optimized' / 'manifest.json'
IMAGES = json.loads(IMAGE_MANIFEST.read_text()) if IMAGE_MANIFEST.exists() else {}
PAGES = ('index', 'aboutus', 'resources', 'faq', 'getinvolved', 'forum')
BLOCK = re.compile(r'{%\s*block\s+(\w+)\s*%}(.*?){%\s*endblock\s*%}', re.S)

def render(name):
    text = (ROOT / 'templates' / (name + '.html')).read_text()
    parent = re.search(r"{%\s*extends\s+['\"]([^'\"]+)['\"]\s*%}", text)
    if parent:
        blocks = dict(BLOCK.findall(text))
        text = BLOCK.sub(lambda m: blocks.get(m[1], m[2]),
                         (ROOT / 'templates' / parent[1]).read_text())
    return text.replace('<body>', f'<body data-page="{name}">')

def convert(text, prefix):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r"{{\s*url_for\(['\"]static['\"],\s*filename=['\"]([^'\"]+)['\"]\)\s*}}",
                  lambda m: prefix + 'static/' + m[1], text)
    # keep links working on the domain and github pages
    def link(m):
        attr, quote, value = m.groups()
        parsed = urlsplit(value)
        if parsed.netloc in ('127.0.0.1:5000', 'solvexchange.org', 'www.solvexchange.org') or (value.startswith('/') and not value.startswith('//')):
            route = parsed.path.strip('/')
            if route in ('login', 'register', 'register-verified'):
                route = 'forum'
            value = prefix + (route + '/' if route else '')
            if parsed.query:
                value += '?' + parsed.query
            if parsed.fragment:
                value += '#' + parsed.fragment
        return attr + '=' + quote + value + quote
    text = re.sub(r'(href|src|action)\s*=\s*([\'\"])(.*?)\2', link, text)
    text = re.sub(r'<script\b[^>]*src=[\'\"]https://code.jquery.com/[^>]*></script>', '', text)
    text = text.replace('share your ideas on a nationwide forum!', 'connect through our community channels!')
    text = text.replace('>Forum</a>', '>Community</a>').replace('See the Forum', 'Join the Community')
    # send people to the community links now
    text = text.replace('contribute your thoughts to a live forum.', 'connect through our community channels.')
    text = text.replace('Share your ideas through a Canada-wide forum to hear the opinions of others, and further expand your plan. See what others have to share and collaborate with your peers!', 'Connect through our community channels to share ideas, hear from others, and collaborate with your peers!')
    text = text.replace('Feel Free to reply to the comments of others.', 'Connect with others through our community channels.')
    text = text.replace('Our forum, social media', 'Our community channels, social media').replace('Our forum serves', 'Our community serves')
    def image_tag(m):
        tag = m[0]
        source = re.search(r'src=[\'\"]([^\'\"]+)[\'\"]', tag)
        if not source:
            return tag
        filename = source[1].split('/images/')[-1]
        entry = IMAGES.get(filename)
        if entry:
            tag = tag.replace(source[1], source[1].rsplit('/images/', 1)[0] + '/images/' + entry['file'])
            # leave room for the image before it loads
            tag = re.sub(r'\s+(?:width|height)=[\'\"][^\'\"]*[\'\"]', '', tag)
            tag = tag[:-1] + f' width="{entry["width"]}" height="{entry["height"]}">'
        if 'id="earth"' in tag or 'id="top-logo"' in tag:
            tag = tag[:-1] + ' fetchpriority="high" decoding="async">'
        else:
            tag = tag[:-1] + ' loading="lazy" decoding="async">'
        return tag
    text = re.sub(r'<img\b[^>]*>', image_tag, text)
    text = text.replace('</head>', '<link rel="stylesheet" href="' + prefix + 'static/css/static.css">\n</head>')
    if '{{' in text or '{%' in text:
        raise ValueError('Unresolved template expression')
    return text

def build():
    if OUT.exists():
        for child in OUT.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    OUT.mkdir(exist_ok=True)
    # only copy the public files. leave the server stuff out
    for folder in ('images', 'fonts', 'Files'):
        shutil.copytree(ROOT / 'static' / folder, OUT / 'static' / folder,
                        ignore=shutil.ignore_patterns('.DS_Store'), dirs_exist_ok=True)
    for category, names in {
        'css': ('main', 'global', 'index', 'aboutus', 'resources', 'faq', 'getinvolved', 'static'),
        'js': ('global', 'index', 'aboutus', 'resources', 'faq', 'getinvolved'),
    }.items():
        dest = OUT / 'static' / category
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            shutil.copyfile(ROOT / 'static' / category / f'{name}.{category}', dest / f'{name}.{category}')
    for original in IMAGES:
        if original == 'logo.png':  # keep the png for the tab icon
            continue
        (OUT / 'static' / 'images' / original).unlink(missing_ok=True)
    for page in PAGES:
        dest = OUT if page == 'index' else OUT / page
        dest.mkdir(exist_ok=True)
        (dest / 'index.html').write_text(convert(render(page), './' if page == 'index' else '../'))
        if page != 'index':
            (OUT / (page + '.html')).write_text(convert(render(page), './'))
    # old account links go to the community page
    for old in ('login', 'register', 'register-verified'):
        dest = OUT / old
        dest.mkdir()
        (dest / 'index.html').write_text(convert(render('forum'), '../'))
        (OUT / (old + '.html')).write_text(convert(render('forum'), './'))
    (OUT / '.nojekyll').touch()
    (OUT / 'CNAME').write_text('solvexchange.org\n')
    (OUT / '404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | SolveXchange</title><main><h1>Page not found</h1><p><a href="https://solvexchange.org/">Return to SolveXchange</a></p></main></html>')
    for file in ROOT.glob('google*.html'):
        shutil.copyfile(file, OUT / file.name)
    validate()

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        self.urls.extend(value for key, value in attrs if key in ('href', 'src') and value)
        if tag == 'form':
            raise ValueError('Backend form in static output')

def validate():
    errors = []
    for file in OUT.rglob('*.html'):
        parser = Links(); parser.feed(file.read_text())
        for value in parser.urls:
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (file.parent / unquote(parsed.path)).resolve()
            if not path.is_relative_to(OUT.resolve()) or not path.exists():
                errors.append(f'{file.relative_to(OUT)}: missing {value}')
        if re.search(r'127\.0\.0\.1|{%|{{', file.read_text()):
            errors.append(f'{file}: unresolved server reference')
    for file in (OUT / 'static' / 'js').glob('*.js'):
        if re.search(r'fetch\s*\(|XMLHttpRequest|\$\.ajax|127\.0\.0\.1', file.read_text()):
            errors.append(f'{file}: backend dependency')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Built {len(list(OUT.rglob("*.html")))} HTML files; all local links and assets resolve; no backend calls.')

if __name__ == '__main__':
    build()
