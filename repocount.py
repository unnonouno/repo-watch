#!/usr/bin/env python

import argparse
import csv
import json
import sys
import urllib2


def download_json(url):
    f = urllib2.urlopen(url)
    js = json.loads(f.read())

    if f.getcode() != 200:
        print(js)
        sys.exit(1)

    return js


def get_count(owner, repo, keys):
    url = 'https://api.github.com/repos/{0}/{1}'.format(owner, repo)
    js = download_json(url)
    return {k: js[k] for k in keys}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', nargs='+')
    args = parser.parse_args()

    keys = [
        'open_issues',
        'forks',
        'watchers',
        'subscribers_count',
    ]

    repos = []
    for r in args.repo:
        org, repo = r.split('/')
        repos.append((org, repo))

    counts = {}
    for r in args.repo:
        org, repo = r.split('/')
        counts[r] = get_count(org, repo, keys)

    for key in keys:
        with open('{}.csv'.format(key), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(args.repo)
            writer.writerow([counts[r][key] for r in args.repo])
