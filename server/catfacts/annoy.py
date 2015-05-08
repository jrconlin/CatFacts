# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from catfacts.store import Store
from catfacts.push import push
from twisted.internet import reactor


class Annoy(object):
    """ Send a notification full of kitty facts to the customer.

    This is called Annoy purely for historical reasons and not because
    it sends a notification every 10 seconds.
    """

    def __init__(self, config):
        self.ap_settings = config
        self.log = config.log
        self.period = config.period

    def _success(self, msg=None):
        self.log.msg(".")

    def _error(self, err=None):
        self.log.err("Annoy: %s" % err)

    def ping(self, url, info):
        """ Send out the notification via the Push service. """
        d = push(
            url.encode('ascii', 'ignore'),
            info['version'],
            info['data'])
        d.addCallback(self._success)
        d.addErrback(self._error)

    def bother(self):
        """ Iterate through known customers and send the next fact.

        Note, there's no customer clean up being done here. If this
        is a real app, you'd want to do that, possibly by having your
        app 'check in' or by monitoring when your customer responds
        to a ping.
        """
        customers = Store(self.ap_settings).getCustomerFacts()
        for url, info in customers.iteritems():
            self.ping(url, info)
        reactor.callLater(self.period, self.bother)
