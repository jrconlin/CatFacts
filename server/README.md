# Cat Facts

A sample app to demonstrate using AutoPush services.

This is a demo app that sends fun, possibly true cat facts to your
"customers" every period. The default is 10 seconds. Sadly, the
"unsubscribe" feature is incomplete.

## About the server:

The server is also a bit of an experiment for me to learn python's
Twisted framework. Your suggestions/patches/comments happily accepted
because that's how people learn things.

You'll note a sad lack of unit tests at the moment. Those are coming,
but for now, it's a demo app and you get to live on the edge.

## Installing:

To install the server, I suggest running it in a virtualenv:

    $ virtualenv .
    $ bin/python setup.py install develop

This will set up the server in "developmental" mode. This will make
changing the server easier.

You'll probably also want to make sure that sqlite3 is installed. The
app uses it for the catfacts.db.

## Running:

Configuration can be by command line or by config file. Configuration
isn't required, and you can just run the server as is:

    $ bin/catfacts

This will start a server listening on port 8082. You can get help with

    $ bin/catfact -h

## Resetting:

The easiest way to "reset" this app would be to just delete
"catfacts.db". The app will recreate the facts and start accepting new
customers. Obviously, all old customers are lost.
