__author__ = 'sanyi'

import re
from .wrapper import *


# tested against ipset v6.20.1, protocol version: 6
IPSET_RE_LIST_TERSE = re.compile("Name:\s(.*?)\sType:\s(.*?)\sRevision:\s(.*?)\sHeader:\s(.*?)\sSize in memory:\s(.*?)"
                                 "\sReferences:\s(.*?)\s", re.DOTALL)

IPSET_LIST_HEADER = re.compile("hashsize (\d*) maxelem (\d*)")


def ipset_get_set_names():
    return ipset_list(name=True).split()


def ipset_list_ext():

    mode_new_entry = 0
    mode_headers = 1
    mode_members = 2

    result = dict()

    mode = mode_new_entry

    for line in ipset_list(generator=True):
        print(line)

        if mode == mode_new_entry:
            if line.startswith('Name: '):
                entry_name = line[6:]
                mode = mode_headers
                current_entry = dict()
                result[entry_name] = current_entry
                current_entry["name"] = entry_name

        elif mode == mode_headers:
            if line == '':
                mode = mode_new_entry
            elif line.startswith('Type: '):
                current_entry["type"] = line[6:]
            elif line.startswith('Revision: '):
                current_entry["revision"] = int(line[10:])
            elif line.startswith('Header: '):
                header = line[8:]

                match = IPSET_LIST_HEADER.search(header)

                if match:
                    current_entry['hashsize'] = match.group(1)
                    current_entry['maxelem'] = match.group(2)

                current_entry['header'] = header

            elif line.startswith('Size in memory: '):
                current_entry["memory"] = int(line[16:])
            elif line.startswith('References: '):
                current_entry["references"] = line[12:]

            elif line.startswith('Members:'):
                current_entry["members"] = []
                mode = mode_members

        elif mode == mode_members:
            if line == '':
                mode = mode_new_entry
            else:
                current_entry["members"].append(line)

    return result


def ipset_add_entries(set_name, entries, exist=False):
    def command_list_generator():
        for entry in entries:
            yield "add %s %s%s\n" % (set_name, entry, "-exist" if exist else "")

    return ipset_restore_from_command_list(command_list_generator())