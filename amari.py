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

def filter_access_to_not_textual_contents(logmap):
    return [x for x in logmap if not re.search('(.ico|js|css)$', x['request_uri'])]

from datetime import datetime as dt
def create_accesscount_by_time_map(logmaps):
    d = {}
    for logmap in logmaps:
        key = dt.strptime(logmap['time_local'], "%d/%b/%Y").date()
        d[key]=d.get(key, 0) + 1
    return sorted(d.items(),key=lambda e:e[0])

logmaps = parse_access_log('access.log')

date_accesscount_map = create_accesscount_by_time_map(
  filter_access_to_not_textual_contents(logmaps))

print('date\tclose')
for date_count in date_accesscount_map:
    print(date_count[0].strftime('%d-%b-%y') + '\t' + str(date_count[1]))
