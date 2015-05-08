# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json

from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer
from zope.interface import implements


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducting(self):
        pass

    def stopProducing(self):
        pass


class JSONProducer(StringProducer):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = json.dumps(body)
        self.length = len(body)
