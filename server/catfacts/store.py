# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sqlite3
import time
import uuid


class Store(object):
    """ Storage for catfacts """

    firstFact = "Welcome to Cat Facts! Your kitty canonical " + \
        "source of tabby trivia!"

    def __init__(self, config):
        create = False
        self.file = config.database
        if not os.access(self.file, os.W_OK):
            create = True
        self.db = sqlite3.connect(self.file)
        if create:
            self._create()
        self._getMaxFacts()

    def _create(self):
        cursor = self.db.cursor()
        cursor.execute('''
        create table if not exists
            facts(id integer primary key, fact text)
        ''')
        cursor.execute('''
        create table if not exists
            customers(id string primary key,
                push text unique,
                fact integer,
                unsubscribe text)
        ''')
        self._load()
        self.db.commit()

    def _load(self):
        cursor = self.db.cursor()
        f = open("catfacts.txt")

        def loader():
            for line in f.readlines():
                yield(line.strip(),)
        cursor.executemany('''insert into facts(fact) values (?)''',
                           loader())
        cursor.execute('''insert into facts(id,fact) values (0,:fact)''',
                       {"fact": self.firstFact})
        f.close()

    def _getMaxFacts(self):
        """ How many facts do we have? """
        cursor = self.db.cursor()
        cursor.execute('''select count(*) from facts;''')
        self.maxFacts = cursor.fetchone()[0]

    def getCustomerFacts(self):
        """ Get the next fact for each customer """
        reply = {}
        cursor = self.db.cursor()
        # update the cat fact, resetting to 1 on fact wrap.
        cursor.executescript('''
            update customers set fact = fact + 1;
            update customers set fact = 1 where fact = %d;
        ''' % self.maxFacts)
        self.db.commit()
        cursor = self.db.cursor()
        cursor.execute('''
            select a.push, a.fact, b.fact from customers as a, facts as b
            where a.fact = b.id;
            ''')
        for row in cursor.fetchall():
            reply[row[0]] = {"version": int(time.time()) * 100 + row[1],
                             "data": row[2]}
        return reply

    def getFactForCustomer(self, customerId):
        """ Get the current fact for the customer.

        This is probably going to be used by clients that don't support
        push data
        """
        cursor = self.db.cursor()
        cursor.execute('''
        select b.fact from
            customers as a, facts as b
            where a.fact = b.id and
            a.id = :id;
        ''', {"id": customerId})
        row = cursor.fetchone()
        cursor = self.db.cursor()

        # return push url, factid, fact
        return row[0]

    def getFact(self, id):
        """ Get an individual fact. """
        cursor = self.db.cursor()
        qq = "select fact from facts where id = :id"
        cursor.execute(qq, {"id": id})
        row = cursor.fetchone()
        return row[0]

    def register(self, push):
        """ Register a new endpoint (which is a new customer) """
        cursor = self.db.cursor()
        id = str(uuid.uuid4())
        cursor.execute('''
        insert into customers (id, push, fact) values (:id, :push, 0);
        ''', {"id": id, "push": push})
        self.db.commit()
        # Yes, a proper customer index system would assign something
        # like a guid for the customer id.
        # This is a demo app, so I'm cutting a corner.
        return id

    def unregister(self, push):
        """ Unregister a customer """
        cursor = self.db.cursor()
        cursor.execute('''
        delete from customers where push = :push
        ''', {"push": push})
        self.db.commit()
