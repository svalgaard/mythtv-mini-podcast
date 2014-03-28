#! /usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Must be run on the MythTV backend
# Requries HandBrakeCLI
#
# (c) 2014, Jens Svalgaard Kohrt
#

import MythTV
import os
import ConfigParser
import sys
import re
import email.utils
import time
import datetime
import xml.sax.saxutils

CONFIG_FN = '~/.mythpodcast.cfg'

CONV_CMD = ('HandBrakeCLI '
            '-f mp4 -m -O '
            '-v 1 '
            '-e x264 --x264-preset medium --x264-profile high '
            '-q 22.0 -r 25 -X 768 --custom-anamorphic --keep-display-aspect '
            '-E faac -B 128 -mixdown stereo -R Auto -D 1.1 '
            '--input "%(src)s" --output "%(dst)s"')


def setupConfig(config_fn=None):
    global config
    if not config_fn:
        config_fn = CONFIG_FN

    config = ConfigParser.ConfigParser({'convcmd': CONV_CMD})
    config.read(os.path.expanduser(config_fn))

    return [c for c in config.sections() if c != 'default']


def readValue(section, key, default=None):
    if config.has_option(section, key):
        return config.get(section, key).decode('utf-8')
    if section != 'default' and config.has_option('default', key):
        return config.get('default', key).decode('utf-8')
    if default is not None:
        return default
    print 'Cannot find required option key:'
    print '[%s]' % section
    print '%s=???' % key
    sys.exit(1)


def dateAsRFC2822(dt):
    return email.utils.formatdate(time.mktime(dt.timetuple()))


def xmlEscape(d):
    r = {}
    for k, v in d.items():
        if type(v) in (str, unicode):
            v = xml.sax.saxutils.escape(v)
        r[k] = v
    return r


class Podcast:
    'A collection of several recordings'
    def __init__(self, sec):
        self.sec = sec

        self.title = readValue(sec, 'title', sec.title())
        self.summary = readValue(sec, 'summary', '')
        self.search = readValue(sec, 'search')  # required

        # directory structure
        suf = readValue(sec, 'suffix', sec)
        self.root = os.path.join(readValue(self.sec, 'root'), suf)
        self.urlroot = os.path.join(readValue(self.sec, 'urlroot'), suf)

        if not os.path.isdir(self.root):
            print 'mkdir -p', self.root
            os.makedirs(self.root)

        # recordings
        self.recordings = None

    def getRecordings(self):
        if self.recordings is None:
            be = MythTV.MythBE()
            title = re.compile(self.search, re.IGNORECASE)

            self.recordings = []
            for rec in be.getRecordings():
                mfn = be.getCheckfile(rec)
                if title.search(rec.title) and os.path.isfile(mfn):
                    self.recordings.append(Recording(self, rec))
            self.recordings.sort()
        return self.recordings

    def convert(self):
        for rec in self.getRecordings():
            rec.convert()

    def writePodcast(self):
        xml = self.asXML().encode('utf-8')
        xfn = os.path.join(self.root, 'podcast.xml')
        if os.path.isfile(xfn) and open(xfn).read() == xml:
            print xfn, 'No changes. Podcast not updated'
        else:
            print xfn, 'updating podcast'
            open(xfn, 'w').write(xml)

    def asXML(self):
        d = dict()
        d['title'] = self.title
        d['summary'] = self.summary

        # do we have a cover?
        d['cover'] = ''
        for fn in ['cover.jpg', 'cover.png',
                   readValue(self.sec, 'cover', 'cover.png')]:
            lfn = os.path.join(self.root, fn)
            if os.path.isfile(lfn):
                d['cover'] = os.path.join(self.urlroot, fn)

        xml = u'''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <itunes:explicit>no</itunes:explicit>
    <title>%(title)s</title>
    <itunes:summary>%(summary)s</itunes:summary>
    <description>%(summary)s</description>
    <itunes:image href="%(cover)s" />
''' % xmlEscape(d)

        xml += u''.join(x.asXML() for x in self.getRecordings())
        xml += u'  </channel>\n</rss>\n'

        return xml


class Recording:
    def __init__(self, podcast, rec):
        be = MythTV.MythBE()
        self.podcast = podcast
        self.rec = rec
        self.mythlfn = be.getCheckfile(self.rec)
        self.mp4fn = os.path.splitext(os.path.basename(rec.filename))[0]+'.mp4'

    def __cmp__(self, other):
        return cmp((self.rec.starttime, self.rec),
                   (other.rec.starttime, other.rec))

    def convert(self):
        tmplfn = os.path.join(self.podcast.root, '.tmp.' + self.mp4fn)
        mp4lfn = os.path.join(self.podcast.root, self.mp4fn)

        if os.path.isfile(mp4lfn):
            print mp4lfn, 'already there'
            return

        cmd = CONV_CMD % {'src': self.mythlfn, 'dst': tmplfn}
        print cmd
        print
        r = os.system(cmd)
        if r or not os.path.isfile(tmplfn):
            print 'ERROR', r
            if os.path.isfile(tmplfn):
                os.unlink(tmplfn)
            sys.exit(1)
        else:
            print 'OK'
            os.rename(tmplfn, mp4lfn)

    def asXML(self):
        mp4lfn = os.path.join(self.podcast.root, self.mp4fn)
        if not os.path.isfile(mp4lfn):
            return ''

        d = dict(self.rec.items())
        d['url'] = os.path.join(self.podcast.urlroot, self.mp4fn)
        d['duration'] = '%s' % (self.rec.recendts-self.rec.recstartts).seconds
        d['pubdate'] = dateAsRFC2822(self.rec.recendts)
        d['guid'] = self.mythlfn

        return u'''  <item>
    <title>%(title)s</title>
    <description>%(description)s</description>
    <link>%(url)s</link>
    <itunes:duration>%(duration)s</itunes:duration>
    <itunes:summary>%(description)s</itunes:summary>
    <itunes:subtitle>%(subtitle)s</itunes:subtitle>
    <itunes:explicit>no</itunes:explicit>
    <pubDate>%(pubdate)s</pubDate>
    <enclosure url="%(url)s" length="%(duration)s" type="video/mp4" />
    <guid>%(guid)s</guid>
  </item>

''' % xmlEscape(d)

onlySecs = sys.argv[1:]
secs = setupConfig()
print 'Sections', secs
if onlySecs:
    usecs = []
    for o in onlySecs:
        if o in secs:
            usecs.append(o)
        else:
            print o, 'unknown section'
    print 'Only looking at sections', usecs
else:
    usecs = secs

pods = [(sec, Podcast(sec)) for sec in usecs]

[p.writePodcast() for s, p in pods]
for s, p in pods:
    p.convert()
    p.writePodcast()
