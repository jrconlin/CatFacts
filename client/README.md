# Cat Facts

A sample app to demonstrate using AutoPush services.

This is a demo app that displays fun, possibly true cat facts every
period. The default is 10 seconds. Sadly, the "unsubscribe" feature is
incomplete.

## About the client:

This app is a FirefoxOS app.

If you want, you can grab Firefox Developer at
https://www.mozilla.org/en-US/firefox/channel/#developer

Once you have it, you can:
* start the WebIDE
* Install the simulator for Firefox OS 2.2
* Under Project, Open a Package Project
* Navigate the the "client" subdirectory
* Start the app by pressing the "Play" button.

If you wish, you can open up the developer tools by pressing the
"wrench" icon.

## Running:

Since I run the server in a local virtual machine, I've preset the app
to connect to it's address and port. You'll probably want to modify
that value (in index.html) to point to whatever address is correct for
you.

Once you register, you'll start getting cat facts! Sadly, since
there's no unsubscribe implemented, the only way you can stop getting
cat facts is to either stop the server, or to delete the app. Bear
that in mind when you're building your app. (HINT: You really want to
give users control over these sorts of things otherwise they're not
going to be terribly happy with you.)

You may notice that if you run this app more than once, you start
getting more and more duplicate messages. Why is that? Well, it's
because everytime you register, you're getting a new endpoint. The
server doesn't care, it just iterates through each known endpoint and
sends out a push.  Kinda handy if you want your app to have endpoints
for different things, not so handy if you're just going to pay
attention to whether or not you've already registered an endpoint for
that user + app + device.

You can solve that by doing things like keeping app state in local
storage, or by having the server be smarter about connections for a
user.

Or you can spam users with messages so they delete your app and give
you a one star rating. It's up to you.


