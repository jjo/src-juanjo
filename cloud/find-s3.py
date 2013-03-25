#!/usr/bin/python
#
# Author: JuanJo Ciarlante <jjo@canonical.com>
# License: GPlv3
# Copyright 2013, Canonical Ltd.
#
"""
find-s3.py: simple find like command for swift/s3 buckets
"""
# pylint: disable=C0103,W0142,E1101
import os
import sys
import argparse
import time
import fnmatch
import distutils.util
from signal import signal, SIGPIPE, SIG_DFL


UNITS_TO_EXP = {'B': 1, 'K': 10, 'M': 20, 'G': 30, 'T': 40}
EXP_TO_UNITS = dict([(v, k) for (k, v) in UNITS_TO_EXP.iteritems()])


class SStorageEntry():
    "Facility class to create a storage-type independent entry"
    def __init__(self, key, name, size, last_modified, **kwargs):
        self.key = key
        self.name = name
        self.size = size
        self.last_modified = last_modified
        for key in kwargs:
            self.key = kwargs[key]


class SStorage(object):
    "Parent class: provide generic generators for filter, print"
    def __init__(self, args):
        self._args = args

    def find_filter(self, entries):
        "Filter consumer entries by 'args' cmdline switches"
        args = self._args
        for entry in entries:
            if (args.name and not fnmatch.fnmatchcase(entry.key, args.name)):
                continue
            if (args.iname and not fnmatch.fnmatch(entry.key, args.iname)):
                continue
            #s3: 2013-03-14T08:34:08.937090Z
            #swift: 2013-03-14T08:34:08.937090Z
            if entry.last_modified[-1] == 'Z':
                entry.last_modified = entry.last_modified[0:-1]
            t = time.strptime(entry.last_modified, "%Y-%m-%dT%H:%M:%S.%f")
            if (args.mtime and not args.mmin):
                args.mmin = args.mtime * 1440
            if (args.mmin):
                ts = (time.time() - abs(args.mmin) * 60)
                if bool(args.mmin < 0) == bool(time.mktime(t) < ts):
                    continue
            if (args.size_less):
                args.size = '-' + args.size_less
            if (args.size):
                units = UNITS_TO_EXP.get(args.size[-1].upper())
                if units:
                    size = int(args.size[0:-1]) * 2 ** units
                else:
                    size = int(args.size)
                if bool(size < 0) == bool(entry.size > abs(size)):
                    continue
            yield entry

    def find_print(self, entries):
        "Print entries, including aggregation (-du) and deletion"
        args = self._args
        size_total = 0
        for entry in entries:
            if args.du:
                size_total = size_total + entry.size
            elif args.ls:
                print "  {name}\t{mtime}\t{size:>12s}\n".format(
                    name=entry.name,
                    mtime=entry.last_modified,
                    size=human_units(entry.size, args),
                ),
            else:
                print "  {}".format(entry.key)
            if (args.delete):
                if args.yes or yesno("Delete: {}/{} {}?".format(
                    entry.parent_name, entry.name,
                        args.dry_run * "(DRY-RUN)")):
                    if not args.dry_run:
                        self.delete_entry(entry)
        if args.du:
            print "  {}".format(human_units(size_total, args))

    def do_find(self):
        "Main entry point: Plug generators together"
        return self.find_print(
            self.find_filter(self.gen_entries(self.gen_buckets())))


class S3Storage(SStorage):
    "S3 specific storage implementation"
    def __init__(self, args):
        super(S3Storage, self).__init__(args)
        import boto
        import boto.s3.connection
        assert(not args.prefix)
        if args.s3_hostport:
            self._conn = boto.connect_s3(
                aws_access_key_id=args.ec2_access_key,
                aws_secret_access_key=args.ec2_secret_key,
                host=args.s3_hostport,
                is_secure=not args.ec2_insecure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat())
        else:
            self._conn = boto.connect_s3(
                aws_access_key_id=args.ec2_access_key,
                aws_secret_access_key=args.ec2_secret_key,
                is_secure=not args.ec2_insecure,
                calling_format=boto.s3.connection.OrdinaryCallingFormat())

    def gen_buckets(self):
        "S3: generate buckets, from passed args"
        if self._args.all:
            for bucket in self._conn.get_all_buckets():
                print "{name}/\tctime={created}".format(
                    name=bucket.name,
                    created=bucket.creation_date,
                )
                yield (bucket.name, bucket)
        for name in self._args.bucket:
            yield (name, self._conn.lookup(name))

    def gen_entries(self, buckets):
        "S3: for each consumed bucket, generate its entries"
        for (name, bucket) in buckets:
            for item in bucket.list():
                yield SStorageEntry(item.name, item.key, item.size,
                                    item.last_modified,
                                    parent_name=name, parent_ref=bucket)

    def delete_entry(self, entry):
        "S3: delete single entry"
        entry.parent_ref.delete_key(entry.key)


class SWStorage(SStorage):
    "Swift specific storage implementation"
    def __init__(self, args):
        super(SWStorage, self).__init__(args)
        import swiftclient
        os_options = {
            'tenant_name': args.os_tenant_name,
            'region_name': args.os_region_name,
        }
        self._conn = swiftclient.Connection(
            args.os_auth_url, args.os_username, args.os_password,
            auth_version='2.0', os_options=os_options
        )

    def gen_buckets(self):
        "Swift: generate containers, from passed args"
        if self._args.all:
            for bucket in self._conn.get_account()[1]:
                print "{name}/\tbytes={bytes} count={count}".format(
                    name=bucket['name'],
                    bytes=human_units(bucket['bytes'], self._args),
                    count=bucket['count'],
                )
                name = bucket['name']
                yield (name, self._conn.get_container(
                    name, prefix=self._args.prefix)[1])
        for name in self._args.bucket:
            yield (name, self._conn.get_container(
                name, prefix=self._args.prefix)[1])

    def gen_entries(self, containers):
        "Swift: for each consumed container, generate its entries"
        for (name, container) in containers:
            for item in container:
                yield SStorageEntry(item['name'], item['name'],
                                    item['bytes'], item['last_modified'],
                                    parent_name=name)

    def delete_entry(self, entry):
        "Swift: delete single entry"
        self._conn.delete_object(entry.parent_name, entry.name)


def yesno(msg, default='n'):
    "yesno prompt, using strtobool"
    prompt = raw_input('{} ({})'.format(msg, default))
    return distutils.util.strtobool({'': default}.get(prompt, prompt))


def human_units(size, args):
    "Convert to human units"
    if (not args.human):
        return str(size)
    for exp, unit in sorted(EXP_TO_UNITS.iteritems(), reverse=True):
        ## Only select this unit if at least 3 digits to show
        if size > 100 * (2 ** exp):
            return str(int(size / (2 ** exp))) + unit
    return str(size)


def main():
    "The main()"
    p = argparse.ArgumentParser(description='S3/Swift simple find')
    p.add_argument('bucket', type=str, nargs='*',
                   help='bucket names')
    p.add_argument('-prefix', '--prefix', type=str, action='store',
                   help='prefix, only valid for swift storage')
    p.add_argument('-stype', '--stype', type=str, action='store',
                   help='storage type: {s3, swift}')
    p.add_argument('-name', '--name', type=str, action='store',
                   help='name, with globbing wildcards')
    p.add_argument('-iname', '--iname', type=str, action='store',
                   help='iname, with globbing wildcards')
    p.add_argument('-mtime', '--mtime', type=float, action='store',
                   help='~similar to find cmd: positive for older, '
                   'negative for newer')
    p.add_argument('-mmin', '--mmin', type=float, action='store',
                   help='~similar to find cmd: positive for older, '
                   'negative for newer')
    p.add_argument('-size', '--size', type=str, action='store',
                   help='only objects larger than size[kmg] '
                   '(negative numbers work with no units postfix)')
    p.add_argument('-size-less', '--size-less', type=str, action='store',
                   help='only objects smaller than size (useful for units, '
                   'e.g. --size-less 1M)')
    p.add_argument('-dry-run', '--dry-run', action='store_true',
                   help="don't change/delete anything, only show")
    p.add_argument('-yes', '--yes', action='store_true',
                   help="don't ask, assume 'yes' to prompts")
    p.add_argument('-delete', '--delete', action='store_true',
                   help='DELETE listed objects, will prompt for yes/no')
    p.add_argument('-delet', '--delet', action='store_true',
                   help='bogus option just to avoid --delete short prefixing')
    p.add_argument('-ls', '--ls', action='store_true',
                   help='list object: name mtime size status')
    p.add_argument('-tar', '--tar', action='store_true',
                   help='create a tarfile stream to stdout, from found files')
    p.add_argument('-du', '--du', action='store_true',
                   help='only print a line with aggregated '
                   'disk-usage from matched objects')
    p.add_argument('-human', '--human', action='store_true',
                   help='show human units for size')
    p.add_argument('-all', '--all', action='store_true',
                   help='do it over all buckets')
    p.add_argument('--ec2-access-key', action='store',
                   default=os.environ.get('EC2_ACCESS_KEY'))
    p.add_argument('--ec2-secret-key', action='store',
                   default=os.environ.get('EC2_SECRET_KEY'))
    p.add_argument('--ec2-insecure', action='store_true',
                   default=os.environ.get('EC2_INSECURE'))
    p.add_argument('--s3-hostport', action='store',
                   default=os.environ.get('S3_HOSTPORT'))
    p.add_argument('--os-username', action='store',
                   default=os.environ.get('OS_USERNAME'))
    p.add_argument('--os-tenant-name', action='store',
                   default=os.environ.get('OS_TENANT_NAME'))
    p.add_argument('--os_password', action='store',
                   default=os.environ.get('OS_PASSWORD'))
    p.add_argument('--os_auth_url', action='store',
                   default=os.environ.get('OS_AUTH_URL'))
    p.add_argument('--os-region-name', action='store',
                   default=os.environ.get('OS_REGION_NAME'))
    args = p.parse_args()

    if args.delet:
        print >> sys.stderr, "ERROR: must pass full option: --delete\n"
        p.print_help()
        sys.exit(1)

    class_bytype = {'swift': SWStorage, 's3': S3Storage}
    if not args.stype:
        if args.os_username and args.os_password:
            args.stype = 'swift'
        elif args.ec2_access_key and args.ec2_secret_key:
            args.stype = 's3'
        else:
            print >> sys.stderr, "ERROR: can't guess stype = 's3' or 'swift'"
            sys.exit(1)
    class_bytype[args.stype](args).do_find()

if __name__ == '__main__':
    signal(SIGPIPE, SIG_DFL)
    try:
        main()
    except KeyboardInterrupt:
        pass
