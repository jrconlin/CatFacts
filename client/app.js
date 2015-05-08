/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

var endpoint;
var msgCount=0;
var customerId;

/** Very simplistic logging mechanism.
 */
function Log(s, cls="log") {
    // Write to the dev console.
    if (cls == "error") {
        console.error(s)
    } else {
        console.log(s);
    }
    // Optionally display via the app.
    // Display(s, cls);
}

function Display(s, cls="fact") {
    // Display the message on the app.
    var txt = document.createTextNode(s);
    var p = document.createElement("p");
    p.className=cls;
    p.appendChild(txt);
    var stat = document.getElementById("status");
    if (msgCount > 4) {
        stat.removeChild(stat.firstChild);
    }else {
        msgCount = msgCount + 1;
    }
    document.getElementById("status").appendChild(p);
}

function _getHost() {
    // Get the host from the app form field.
    // This would normally either be hardcoded or (preferably) pulled
    // from a config file.
    try {
        var host = document.getElementById("server").value;
        if (!host.startsWith('http')) {
           host = 'http://'+ host;
        }
        if (host != "") {
            return host
        }
        Log ("Host not specified","error")
    } catch(e) {
        console.error(e);
    }
    return undefined
}


function _isOk(stat) {
    // Is the returned status "OK" or a variant there of?
    return (stat >=200 && stat < 300)
}


function _register(endpoint) {
    // Registering as a new customer.
    try{
        var host = _getHost();
        if (host == undefined) {
            return false
        }

        // Registration is a PUT call to the remote server.
        var post = new XMLHttpRequest();
        post.open('PUT', host);
        post.setRequestHeader("Content-Type",
                "application/x-www-form-urlencoded");
        post.onload=function(e) {
            if (!_isOk(this.status)) {
                Log("Error " + JSON.stringify(e) + JSON.stringify(this), "error");
                return

            }
            info = JSON.parse(e.target.response);
            customerId=info.customerId;
            Log("Registered. " + e.target.response)
        }
        post.onerror=function(e) {
            Log("Error. Check server log.", "error")
        }
        post.send("push="+encodeURIComponent(endpoint));
        Log("Sending endpoint..." + endpoint)
        return true
    } catch(e) {
        console.error(e);
        return false;
    }
}

function _fetchFact(factid) {
    // if there is no Push Data, or if the data is empty, get the
    // next fact from the server.
    var host = _getHost();
    if (host == undefined) {
        return false
    }
    try {
        var post = new XMLHttpRequest();
        post.open('GET', host + "?version=" + factid +
                  "&customerid=" + customerId);
        post.onload = function (e) {
            if (!_isOk(this.status)) {
                Log("Error " + JSON.stringify(e) + JSON.stringify(this));
                return
            }
            Log("Got.. ", e.target.response);
            Display(e.target.response, "fact");
            notify(title="New Fact!", msg = e.target.response);
        }
        post.onerror = function(e) {
            Log("Error. Check server log.", "error");
            return;
        }
        Log("Getting fact...")
        post.send();
    } catch(e) {
        Log("Error " + JSON.stringify(e));
        return
    }

}

function setMessageHandler() {
    // Set the message handler for the push events
    // IMPORTANT::::
    // This is the key function for clients an push. This handles events
    // from push.
    navigator.mozSetMessageHandler('push', function(msg) {
        if (msg.data == undefined) {
            Log("Fetch the fact from the catfact server");
            _fetchFact(msg.version);
            return
        }
        notify("New Cat Fact!", msg.data);
    })

    // IMPORTANT::::
    // Push re-registration is possible, so handle it.
    // A push re-registration is when the server has stated that the
    // endpoint has changed. This doesn't happen very often. When it
    // does, it's important that your server start using the new endpoint
    // since notifications to the old endpoint will no longer be
    // received by this app.
    navigator.mozSetMessageHandler("push-register", function(e){
        Log("Recv'd re-registration "+JSON.stringify(e))
        _retister(endpoint, '/', 'DELETE')
        doRegister()
    })
    Log("Message Handler Set.")
}


function notify(title="Cat Fact!", msg=None){
    // Display the popup notification to the user.
    Log("New Notification " + msg)
    if (!("Notification" in window)) {
        console.error("Sad Cat: No notifications.");
        return;
    }
    if (Notification.permission === "granted") {
        var notification = new Notification(title, {
            "body": msg});
        }
    return;
}

function doRegister() {
    // Register the endpoint with the remote server
    Log("Registering...");
    var srv = document.getElementById("server");
    if (srv.value.length == 0) {
        alert("Server address missing.");
        if (!srv.classList.contains("error")) {
            srv.classList.add("error");
        }
        return;
    }
    srv.classList.remove("error");

    // IMPORTANT::::
    // Push.register is how your app gets a new endpoint. Each call to
    // register() results in a new endpoint to your app. Note that this
    // does not invalidate old endpoints, so it's possible for your app
    // to get multiple messages. Handy if you want endpoints for different
    // functions, not so handy if you're not careful.
    //
    // It's a good idea to store this endpoint in app storage after you
    // get it and before you send it off to your app server.
    var req = navigator.push.register();
    req.onsuccess = function(e) {
        endpoint = req.result;
        Log("Endpoint:" + endpoint)
        // Now would be a great time to save this endpoint to local storage.
        _register(endpoint)
    }
    req.onerror = function(e) {
          Log("Registration error: " + JSON.stringify(e), "error");
          return;
    }
}

// main
if (!navigator.push && !navigator.mozSetMessageHandler) {
    document.getElementById("config").style.display="none";
    Display("No push service available for this device.","sadcat")
} else {
    setMessageHandler();
    document.getElementById("go").addEventListener("click", doRegister, true)
}

