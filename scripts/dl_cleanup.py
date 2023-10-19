#!/usr/bin/env python3
"""
OpenWrt download directory cleanup utility.
Delete all but the very last version of the program tarballs.

Copyright (C) 2010-2015 Michael Buesch <m@bues.ch>
Copyright (C) 2013-2015 OpenWrt.org
Copyright (C) 2023 CWD.SYSTEMS
"""

import sys
import os
import re
import getopt


# Command line options
class Options:
    def __init__(self):
        self.dry_run = False
        self.show_blacklist = False
        self.whitelist = None


def parse_version_1234(match, filepath):
    prog_name = match.group(1)
    prog_version = (
        (int(match.group(2)) << 64)
        | (int(match.group(3)) << 48)
        | (int(match.group(4)) << 32)
        | (int(match.group(5)) << 16)
    )
    return prog_name, prog_version


# Add other parse_version functions in a similar manner


def usage():
    print("OpenWrt download directory cleanup utility")
    print("Usage: {} [OPTIONS] <path/to/dl>".format(sys.argv[0]))
    print("\nOptions:")
    print("  -d, --dry-run         Do a dry-run. Don't delete any files")
    print("  -B, --show-blacklist  Show the blacklist and exit")
    print("  -w, --whitelist ITEM  Remove ITEM from blacklist")


def main(argv):
    opts = Options()

    try:
        (options, args) = getopt.getopt(
            argv[1:],
            "hdBw:",
            ["help", "dry-run", "show-blacklist", "whitelist="],
        )
        if len(args) != 1:
            usage()
            return 1
    except getopt.GetoptError as e:
        usage()
        return 1

    directory = args[0]

    if not os.path.exists(directory):
        print("Can't find dl path", directory)
        return 1

    for (option, value) in options:
        if option in ("-h", "--help"):
            usage()
            return 0
        if option in ("-d", "--dry-run"):
            opts.dry_run = True
        if option in ("-w", "--whitelist"):
            for i, (name, regex) in enumerate(blacklist):
                if name == value:
                    del blacklist[i]
                    break
            else:
                print("Whitelist error: Item", value, "is not in blacklist")
                return 1
        if option in ("-B", "--show-blacklist"):
            for (name, regex) in blacklist:
                sep = "\t\t" if len(name) >= 8 else "\t"
                print(f"{name}{sep}({regex.pattern})")
            return 0

    entries = []
    for filename in os.listdir(directory):
        if filename in (".", ".."):
            continue
        for (name, regex) in blacklist:
            if regex.match(filename):
                if opts.dry_run:
                    print(filename, "is blacklisted")
                break
        else:
            try:
                entries.append(Entry(directory, filename))
            except EntryParseError as e:
                pass

    prog_map = {}
    for entry in entries:
        if entry.prog_name in prog_map:
            prog_map[entry.prog_name].append(entry)
        else:
            prog_map[entry.prog_name] = [entry, ]

    for prog in prog_map:
        last_version = max(prog_map[prog])
        for version in prog_map[prog]:
            if version != last_version:
                version.delete_file()
        if opts.dry_run:
            print("Keeping", last_version.get_path())

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
