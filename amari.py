#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def parse_access_log(filepath):
    def create_dict(elem):
        kv = elem.split(':')
        return dict([(kv[0], kv[1])])

    lst=[]
    with open(filepath) as tsvfile:
        import csv
        reader=csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            r = {}
            for pair in row:
                r.update(create_dict(pair))
            lst.append(r)
    return lst




def filter_access(logmap):
    def filter_access_to_not_textual_contents(logmap):
        return [x for x in logmap if not re.search('(^/fonts)|((ico|js|css|png|jpeg|jpg)$)', x['request_uri'])]

    def filter_bot_access(logmap):
        return [x for x in logmap if not re.search('.*(bot|Bot|BOT).*', x['http_user_agent'])]

    def filter_by_status_code(logmap):
        return [x for x in logmap if re.search('^2\d\d', x['status'])]
    return filter_bot_access(
      filter_access_to_not_textual_contents(
        filter_by_status_code(logmap)))

from datetime import datetime as dt
def create_accesscount_by_time_map(logmaps):
    d = {}
    for logmap in logmaps:
        key = dt.strptime(logmap['time_local'], "%d/%b/%Y").date()
        d[key]=d.get(key, 0) + 1
    return sorted(d.items(),key=lambda e:e[0])


def create_request_uri_count(logmaps):
    d = {}
    for logmap in logmaps:
        key = logmap['request_uri']
        d[key] = d.get(key, 0) + 1
    return sorted(d.items(), key=lambda e:e[1], reverse=True)

logmaps=filter_access(parse_access_log('access.log'))
date_accesscount_map = create_accesscount_by_time_map(logmaps)

print('date\tclose')
for date_count in date_accesscount_map:
    print(date_count[0].strftime('%d-%b-%y') + '\t' + str(date_count[1]))

print('\n')

print(create_request_uri_count(logmaps))
