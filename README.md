mythtv-mini-podcast
===================

Converts MythTV recordings into podcasts for viewing on a tablet etc.

Requirements
------------

* Standard MythTV setup
* Webserver to serve the files

This has only been tested with a setup with one mythtv backend server, and mythpodcast.py running on that server.

HOWTO
-----

Edit <pre>sample.mythpodcast.cfg</pre> and copy it to <pre>~/.mythpodcast.cfg</pre>.
Running <pre>mythpodcast.py</pre> with the provided sample.mythpodcast.cfg file, you get a file structure similar to what is shown below.
The files can then subsequently be served using e.g. an apache webserver.

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
