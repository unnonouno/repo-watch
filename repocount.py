#!/usr/bin/env python

import argparse
import csv
import sys

import requests


def download_json(url):
    r = requests.get(url)

    if r.status_code != 200:
        print(r.json())
        sys.exit(1)

    return r.json()


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
