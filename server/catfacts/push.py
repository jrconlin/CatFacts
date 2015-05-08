# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urllib import urlencode
from twisted.web import client
# from twisted.python import log


def push(url, version, fact):
    """ Send out a Push Notification. """
    # Send out the next fun cat fact!
    #
    # Important:
    # Push can take two fields, the "version" (which is an ever increasing
    # numeric value) and "data" (which is up to about 4K of whatever).
    # IN THE NEAR FUTURE, "data" will need to be encrypted using a spec that
    # has not finalized yet. Keep an eye out for details. For now, it's just
    # passed in whole.
    # Remember: data is highly volitile. Your app may not get it for a number
    # of reasons. That's why you also send a version which your app will get.
    # (See the docs for why data is volitile and version is not, but basically,
    # a number potentially exposes far less data to third parties (us), than
    # a data block does.)
    bjs = urlencode({"version": version, "data": fact})
    d = client.getPage(url, method='PUT', postdata=bjs)
    # uncomment this for a "curl" call you could make from the command line.
    # log.msg("""curl -X PUT "%s" -d '%s' """ % (url, bjs))
    return d
