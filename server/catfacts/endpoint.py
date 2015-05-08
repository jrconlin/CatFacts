# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
import urlparse

import cyclone.web

from catfacts.store import Store
from catfacts.push import push


class EndpointHandler(cyclone.web.RequestHandler):
    """ Handle the one and only endpoint for this server. """

    def _addCors(self):
        """ Add the CORS callbacks to allow XMLHTTPRequests """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "GET, POST, PUT, DELETE")

    def _getArgs(self):
        reply = {}
        if len(self.request.body) > 0:
            bodyArgs = urlparse.parse_qs(self.request.body,
                                         keep_blank_values=True)
            reply['push'] = bodyArgs.get("push")
            reply['customer'] = bodyArgs.get("customerid")
            reply['version'] = bodyArgs.get("version")
        else:
            reply['push'] = self.request.arguments.get("push")
            reply['customer'] = self.request.arguments.get("customerid")
            reply['version'] = self.request.arguments.get("version")
        return reply

    def options(self, *args):
        """ Handles OPTIONS calls, used by CORS """
        self._addCors()

    def head(self, *args):
        """ Handles HEAD calls, used by CORS """
        self._addCors()

    def _success(self, *msg):
        """ Generic Success callback """
        self.log.msg("Ok...")
        self.set_status(200)
        for m in msg:
            # Don't send empty objects. Another option would be to
            # combine 'msg' objects into one outbound string.
            # An empty object could be created by an empty return from
            # a differed funciton.
            if m != '{}':
                self.log.msg("     %s" % m)
                self.write(m)
        self.finish()

    def _error(self, error):
        """ Generic Error callback """
        self.log.err("ERROR: %s" % error)
        self.set_status(500)
        self.finish()

    @cyclone.web.asynchronous
    def put(self, path_info):
        """ Registration function. Responds to PUT requests. """
        self._addCors()
        args = self._getArgs()
        # SQLite storage is not thread safe, and must be isolated to a thread.
        store = Store(self.ap_settings)
        try:
            # IMPORTANT:
            # This is the call that the client makes to "register" the push
            # URL with you. There's no official protocol for doing this, and
            # in this case, I'm just taking it as a Form field entry.
            #
            # The Endpoint URL is sensitive info, you should treat it as
            # you would the customer's phone number. If the endpoint url
            # falls into "the wrong hands" a malicious party could use it
            # to trigger your app needlessly.
            endpoint = args['push'][0]
            customerId = store.register(endpoint)
            # Send back the customer ID (just used by the app).
            self._process_registration(
                endpoint,
                json.dumps({"customerId": customerId}))
        except Exception, e:
            self._error(e)

    def _process_registration(self, endpoint, msg):
        """ Callback to complete registration """
        # Cheat like heck by appending the "fact" to the version.
        # Obviously, this is a horrible thing to do, and you really
        # ought to be using the customer ID
        version = int(time.time()) * 100
        d = push(
            endpoint,
            version,
            Store.firstFact)
        d.addCallback(self._success, msg)
        d.addErrback(self._error)

    @cyclone.web.asynchronous
    def get(self, path_info):
        """ Get the next fact for the user"""
        self._addCors()
        store = Store(self.ap_settings)
        args = self._getArgs()
        # The correct way, by using the customerID.
        # This could be loaded as a POST argument, or via cookies
        # or any number of ways. I'm doing the very insecure, horribly
        # lazy way of passing it in the request. This is because this is
        # a demo app.
        if args['customer']:
            id = args['customer'][0]
            try:
                fact = store.getFactForCustomer(id)
                self._success(fact)
                return
            except Exception, e:
                pass
        # Fail over to sneaky version trick.
        if not args['version']:
            return
        ver = args['version'][0][-2:]
        try:
            # SQLite3 isn't thread safe, so we can't defer.
            fact = store.getFact(ver)
            self._success(fact)
        except Exception, e:
            self._error(e)

    @cyclone.web.asynchronous
    def delete(self, path_info):
        """ The following is left as an exercise to the reader."""
        #TODO: delete
        # because it wouldn't be cat facts if it could go away.
        pass
