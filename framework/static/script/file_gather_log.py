#!/usr/bin/env python
# -*- coding: utf8 -*-
import json


def process_log_content():
    result_dict = dict()
    with open("./hxj_log") as f:
        line = f.readline()
        while line:
            index = line.find('[main]')
            start = index + 6
            if -1 == index:
                index = line.find('[Thread-2]')
                if -1 == index:
                    return None
                start = index + 10
            data = line[start:].split(':')
            rs = result_dict.get(data[0].strip())
            if None is not rs:
                if isinstance(rs, str):
                    result_dict[data[0].strip()] = list()
                result_dict[data[0].strip()].append(data[1].strip())
            else:
                result_dict[data[0].strip()] = data[1].strip()
            line = f.readline()
    print json.dumps(result_dict)


if __name__ == '__main__':
    process_log_content()
