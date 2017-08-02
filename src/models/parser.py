#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" instagram parser
"""

from lxml import etree
import requests

def parse(instagram_url):
    """ parse resource url
    """
    content = _fetch_content(instagram_url)
    resource_url = _parse(content)
    return resource_url

def _fetch_content(instagram_url, timeout_s=1):
    resp = requests.get(instagram_url, timeout=timeout_s)
    assert resp.status_code == 200
    return resp.text

def empty(obj):
    if obj in (None, '', [], '[]'):
        return True

def _parse(content):
    tree = etree.HTML(content)
    img = tree.xpath('//meta[@property="og:image"]')
    video = tree.xpath('//meta[@property="og:video"]')
    img_url = None if empty(img) else img[0].get('content')
    video_url = None if empty(video) else video[0].get('content')
    return dict(image=img_url, video=video_url)

if __name__ == '__main__':
    url = 'https://www.instagram.com/p/BW05Dfagjkg/?taken-by=realdonaldtrump&hl=en'
    url = 'https://www.instagram.com/p/BWxz68BFzVr/?taken-by=therock&hl=en'
    print parse(url)
