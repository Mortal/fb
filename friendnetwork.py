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

    jdata = res.read().decode('utf-8')
    res = json.loads(jdata)
    if None in res:
        print("Could not decode:")
        print(jdata)
    return res

def get_fb_batch(token, reqs):
    j = [{"method": "GET", "relative_url": url} for url in reqs]
    while len(j) > 0:
        batch = json.dumps(j[0:50])
        j = j[50:]
        res = get_fb('POST', token, '', {"batch": batch})
        def reduce_response(res):
            if res is None:
                print('// Response is None')
                sys.exit()
            print('//',res['code'], '(batch)')
            if res['code'] != 200:
                print('//',res['body'])
                sys.exit()
            return json.loads(res['body'])
        for r in res:
            yield reduce_response(r)

if __name__ == "__main__":
    token = sys.argv[1]
    label = sys.argv[2]
    labels = ['id', 'first_name', 'name', 'middle_name', 'last_name']
    clique = False
    names = {}
    if label == 'clique':
        clique = True
        label = 'first_name'
    if not label in labels:
        print("// Warning: Label '"+label+"' not in suggested label set "+' '.join(labels))
    friends = get_fb('GET', token, 'me/friends', {'fields':label})
    friends = friends['data']
    if clique:
        for f in friends:
            names[f['id']] = re.sub(r' ', '', f[label])+f['id'][-3:]
            print(names[f['id']])
    else:
        print('graph {')
        print('outputorder=edgesfirst;')
        print('node [style=filled];')
        for f in friends:
            print('"'+f['id']+'" [label="'+f[label]+'"];')
    print()
    reqs = [f['id']+'?fields=mutualfriends.user('+f['id']+')' for f in friends]
    regex = re.compile(r'user=(\d+)')
    for res in get_fb_batch(token, reqs):
        user = res['id']
        if not 'mutualfriends' in res:
            print("// Response for id "+user+" has no mutualfriends")
            continue
        mutuals = res['mutualfriends']['data']
        for mutual in mutuals:
            if user < mutual['id']:
                if clique:
                    print(names[user]+' '+names[mutual['id']])
                else:
                    print('"'+user+'" -- "'+mutual['id']+'";')
    if not clique:
        print('}')
