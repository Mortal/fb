import sys
from http.client import *
import json
import urllib
import re

connection = HTTPSConnection('graph.facebook.com')
connection.connect()

def get_fb(method, token, relative_url, data={}):
    data['access_token'] = token
    url = '/'+relative_url
    purl = url
    if len(purl) > 50:
        purl = purl[0:47]+'...'
    print('//',method, purl)
    body = None
    if method == 'GET':
        url += '?'+urllib.parse.urlencode(data)
    else:
        body = urllib.parse.urlencode(data).encode('utf-8')
    connection.request(method, url, body)
    res = connection.getresponse()
    print('//',res.status, res.reason)
    if res.status != 200:
        print('//',res.read())
        sys.exit()

    return json.loads(res.read().decode('utf-8'))

def get_fb_batch(token, reqs):
    j = [{"method": "GET", "relative_url": url} for url in reqs]
    while len(j) > 0:
        batch = json.dumps(j[0:50])
        j = j[50:]
        res = get_fb('POST', token, '', {"batch": batch})
        def reduce_response(res):
            print('//',res['code'], '(batch)')
            if res['code'] != 200:
                print('//',res['body'])
                sys.exit()
            return json.loads(res['body'])
        for r in res:
            yield reduce_response(r)

if __name__ == "__main__":
    token = sys.argv[1]
    friends = get_fb('GET', token, 'me/friends')
    friends = friends['data']
    print('graph {')
    print('outputorder=edgesfirst;')
    print('node [style=filled];')
    for f in friends:
        print('"'+f['id']+'" [label="'+f['name']+'"];')
    print()
    reqs = ['me/mutualfriends?user='+f['id'] for f in friends]
    regex = re.compile(r'user=(\d+)')
    for res in get_fb_batch(token, reqs):
        mutuals = res['data']
        if not 'paging' in res:
            print("// No paging data")
            continue
        o = regex.search(res['paging']['next'])
        if not o:
            print("// Couldn't get user")
            sys.exit()
        user = o.group(1)
        for mutual in mutuals:
            if user < mutual['id']:
                print('"'+user+'" -- "'+mutual['id']+'";')
    print('}')
