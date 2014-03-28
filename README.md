mythtv-mini-podcast
===================

Converts MythTV recordings into podcasts for viewing on a tablet etc.

Requirements
------------

* MythTV setup
* HandBrakeCLI
* Webserver to serve the files

This has only been tested with a setup with one mythtv backend server, and mythpodcast.py running on that server.

HOWTO
-----

Edit sample.mythpodcast.cfg and copy it to ~/.mythpodcast.cfg
Run mythpodcast.py
With the provided sample.mythpodcast.cfg file, you get a file structure similar to the following

<pre>
/share/mythtv/podcast/barbapapa/1028_20130304113800.mp4
/share/mythtv/podcast/barbapapa/1028_20130305113800.mp4
...
/share/mythtv/podcast/barbapapa/1028_20130415104300.mp4
/share/mythtv/podcast/barbapapa/cover.png
/share/mythtv/podcast/barbapapa/podcast.xml
/share/mythtv/podcast/disney_sjov
/share/mythtv/podcast/disney_sjov/1001_20130222175800.mp4
/share/mythtv/podcast/disney_sjov/cover.jpg
/share/mythtv/podcast/disney_sjov/podcast.xml
/share/mythtv/podcast/skaeg
/share/mythtv/podcast/skaeg/1001_20130123163300.mp4
/share/mythtv/podcast/skaeg/1001_20130130153300.mp4
/share/mythtv/podcast/skaeg/1001_20130213153300.mp4
/share/mythtv/podcast/skaeg/1001_20130222060000.mp4
/share/mythtv/podcast/skaeg/1001_20130227153300.mp4
/share/mythtv/podcast/skaeg/cover.jpg
/share/mythtv/podcast/skaeg/podcast.xml
</pre>

To use this on your iPad, locate the podcast.xml files inside safari, and the podcast will be added.

See also
========

* https://code.google.com/p/mythpodcaster/

Who
===

Jens Svalgaard kohrt - http://svalgaard.net/jens/ - github AT svalgaard.net
