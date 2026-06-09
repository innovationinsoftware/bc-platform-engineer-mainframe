"""
JWT + API Key + Dynamic Resource CRUD + Jinja2 Dashboard - beginner version

This program combines:

1. System data collected with psutil
   - The application reads network interfaces from the local machine.
   - The data is stored in an in-memory dictionary called data.
   - The interfaces resource is read-only from the operating system snapshot.

2. JWT login
   - The user logs in with username and password.
   - The server creates a JWT token.
   - The JWT token is stored in an HttpOnly cookie.
   - Browser pages such as /dashboard use this cookie.

3. API keys
   - A logged-in user can create API keys.
   - API keys can be created from JSON endpoints or from the Jinja2 dashboard.
   - API keys are sent by scripts in the Authorization header:
     Authorization: Bearer <api_key>
   - This sample also expects the Username header for API-key requests.

4. Dynamic CRUD endpoints
   - GET /<resource> lists a resource.
   - POST /<resource> creates or replaces an entry inside a resource.
   - PUT /<resource>/<id> updates an entry.
   - DELETE /<resource>/<id> deletes an entry.
   - GET /search?q=... searches across all resources.

5. Jinja2 web interface
   - GET /login shows a login form.
   - POST /login logs the user in from the browser.
   - GET /dashboard shows API key metadata for the logged-in user.
   - POST /dashboard/api-keys creates a new API key from a web form.
   - POST /dashboard/api-keys/<key_id>/delete deletes / revokes an API key.


HOW TO TEST THIS PROGRAM
========================

1. Install required libraries:

   pip install flask psutil pyjwt

2. Create this folder structure:

   project/
   ├── 2.4-sample-solution-jinja.py
   └── templates/
       ├── layout.html
       ├── login.html
       └── dashboard.html

3. Run the application over HTTP:

   python 2.4-sample-solution-jinja.py

   The application listens on:

   http://localhost:5000

4. Open the web login page in your browser:

   http://localhost:5000/login

5. Login with one of these users:

   Username: alice
   Password: password1

   Username: bob
   Password: password2

6. After login, you should see the dashboard:

   http://localhost:5000/dashboard

7. From the dashboard:
   - create a new API key,
   - copy the generated API key value,
   - delete / revoke existing API keys.

8. Test JSON login with curl and save JWT cookie:

   curl -i -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"password1"}' \
     -c cookies.txt

9. Create a new API key using curl and JWT cookie:

   curl -i -X POST http://localhost:5000/api/newkey \
     -b cookies.txt

10. Use the returned API key with API endpoints:

   curl -i http://localhost:5000/interfaces \
     -H "Username: alice" \
     -H "Authorization: Bearer YOUR_API_KEY_HERE"

   curl -i -X POST http://localhost:5000/notes \
     -H "Content-Type: application/json" \
     -H "Username: alice" \
     -H "Authorization: Bearer YOUR_API_KEY_HERE" \
     -d '{"id":"note1","value":"hello"}'

11. You can also use the preloaded API keys:

   alice: secretapikey1
   bob:   abc123

12. Logout in browser:

   http://localhost:5000/logout


IMPORTANT:
This is a lab example.

In a real application:
- Passwords should be hashed with a password-hashing algorithm, not HMAC.
- API keys should be stored in a database, not in memory.
- API key values should usually be shown only once.
- Secrets should not be hardcoded in the source code.
- Web forms should use CSRF protection.
- HTTPS should be handled before using Secure cookies.

This specific file intentionally keeps HTTP enabled because it is the
Jinja2 variant of the 2.4 sample solution.
"""

from flask import Flask, request, jsonify, abort, current_app, g, make_response
from flask import redirect, url_for, render_template
import secrets
import psutil
import socket
import time
from functools import wraps
import hmac
import hashlib
from datetime import datetime, timedelta
import jwt


# -------------------------------------------------------------------
# LAB SECRETS
# -------------------------------------------------------------------
#
# In this lab the secrets are hardcoded so students can run the file
# without extra setup.
#
# In a real application both values should come from environment
# variables or a secret manager.
HASH_SECRET = b"dev-secret-change-me"
JWT_SECRET = b"dev-secret-change-me"


def hash_key(api_key: str) -> str:
    """
    Create a HMAC-SHA256 hash from a password or API key.

    The application does not store raw API keys.
    Instead, it stores only hashes and compares hashes later.

    Examples:

    hash_key('secretapikey1')
    'deda7fdcf493cae490ea6b7889bc032799d5c1459085cd59bcb6f38ff6f4045a'

    hash_key('abc123')
    '8e024929eb9be0f39c3fb4e0f58bb5f2e8c9ccf81d1723e4c78729d3d0b135f0'

    hash_key("password1")
    '6cbfeac955cd5296ec7394a3d845c0b2f53603fb6fd49629b2b6371bf39ab4f7'
    
    hash_key("password2")
    'a3a232a44f8017ae2d673ae57b5b132f5153d1f117e89008e2f6098f2880a2f2'
    """

    return hmac.new(HASH_SECRET, api_key.encode(), hashlib.sha256).hexdigest()


def keys_match(api_key: str, stored_hash: str) -> bool:
    """
    Check whether a raw API key matches a stored hash.

    compare_digest() is used instead of == because it is safer for
    comparing secret values.
    """

    return hmac.compare_digest(hash_key(api_key), stored_hash)


# Create the Flask application object.
app = Flask(__name__)

# -------------------------------------------------------------------
# IN-MEMORY DATA STORE
# -------------------------------------------------------------------
#
# This dictionary works like a tiny fake database.
#
# "interfaces" is filled from psutil when the application starts.
# "notes" is a writable resource used for CRUD practice.
data = {
    "interfaces": {},
    "notes": {}
}


# -------------------------------------------------------------------
# IN-MEMORY USER AND API KEY DATABASE
# -------------------------------------------------------------------
#
# Each user has:
# - api_key: list of API key hashes or API key metadata dictionaries,
# - role: simple role label displayed in the dashboard,
# - password: hashed password used during login.
#
# Preloaded credentials:
# - alice / password1 / secretapikey1
# - bob   / password2 / abc123
user_db = {
    "alice": {
        "api_key": ["deda7fdcf493cae490ea6b7889bc032799d5c1459085cd59bcb6f38ff6f4045a"],  # secretapikey1
        "role": "admin",
        "password" : "6cbfeac955cd5296ec7394a3d845c0b2f53603fb6fd49629b2b6371bf39ab4f7" # password1
    },
    "bob": {
        "api_key": ["8e024929eb9be0f39c3fb4e0f58bb5f2e8c9ccf81d1723e4c78729d3d0b135f0"],  # abc123
        "role": "user",
        "password" : "a3a232a44f8017ae2d673ae57b5b132f5153d1f117e89008e2f6098f2880a2f2" # password2
    }
}


def permissions_for_user(username: str) -> list[str]:
    """
    Return simple permission labels for the Jinja2 dashboard.

    The original API-key protection in this sample checks whether a key
    belongs to a user. For the dashboard we expose beginner-friendly labels
    that match the user's role.
    """

    # Read user metadata from the fake database.
    user = user_db.get(username, {})

    # Admin gets all example permissions.
    if user.get("role") == "admin":
        return ["read", "write", "delete"]

    # Regular users get read-only permission in this lab.
    return ["read"]


def get_api_keys_for_user(username: str) -> dict:
    """
    Return API key metadata safe to display in HTML.

    Real API key values are not stored. The dashboard therefore displays a
    short hash fingerprint instead of the raw key.

    dashboard.html expects a dictionary and uses:

        api_keys.items()

    That is why this helper returns:

        {
            key_id: {
                "label": "...",
                "permissions": [...],
                "created_at": "..."
            }
        }
    """

    # Find the logged-in user.
    user = user_db.get(username)

    if not user:
        return {}

    # This dictionary is passed directly to dashboard.html.
    result = {}

    # Existing preloaded API keys are stored as plain hash strings.
    # New API keys created from the dashboard are stored as dictionaries.
    #
    # The code below supports both formats so the old curl examples
    # and the new dashboard functionality can work together.
    for index, stored_key in enumerate(user.get("api_key", [])):
        if isinstance(stored_key, dict):
            result[index] = {
                "label": stored_key.get("label", "no label"),
                "permissions": stored_key.get("permissions", ["read"]),
                "created_at": stored_key.get("created_at", "unknown"),
            }
        else:
            result[index] = {
                "label": f"legacy key {index}",
                "permissions": permissions_for_user(username),
                "created_at": "preloaded",
            }

    return result


def get_stored_api_key_hash(stored_key) -> str:
    """
    Return the hash from either the old string format or the dashboard format.

    Old format:
        "abcdef..."

    New dashboard format:
        {
            "api_key_hash": "abcdef...",
            "label": "...",
            "permissions": [...],
            "created_at": "..."
        }
    """

    if isinstance(stored_key, dict):
        return stored_key["api_key_hash"]

    return stored_key


def create_jwt(username: str) -> str:
    """
    Create JWT for a logged-in user.

    The JWT is later stored in an HttpOnly cookie.
    Browser-only routes such as /dashboard use this cookie to identify
    the current user.
    """

    # Get user information from the fake database.
    user = user_db[username]

    # Payload is the data stored inside the token.
    payload = {
        "username": username,
        "role": user["role"],

        # After 5 minutes the token will expire.
        "exp": datetime.utcnow() + timedelta(minutes=5),
    }

    # Create and sign the token.
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def get_username_from_jwt():
    """
    Read and validate JWT from the HttpOnly cookie.

    Returns:
    - username, None when JWT is valid,
    - None, response tuple when JWT is missing or invalid.
    """

    # Read cookie named "jwt".
    token = request.cookies.get("jwt")

    # If there is no cookie, the browser/user is not logged in.
    if not token:
        return None, (jsonify({"error": "Missing JWT cookie"}), 401)

    try:
        # Decode and verify JWT signature and expiration.
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        # Read username from JWT payload.
        username = payload["username"]

        # Check if this user still exists in our fake database.
        if username not in user_db:
            return None, (jsonify({"error": "User from token does not exist"}), 401)

        # Store decoded payload for route handlers that need it.
        g.jwt_payload = payload
        return username, None

    except jwt.ExpiredSignatureError:
        return None, (jsonify({"error": "JWT expired"}), 401)

    except jwt.InvalidTokenError:
        return None, (jsonify({"error": "Invalid JWT"}), 401)


def jwt_protected(func):
    """
    Decorator for routes that require a valid JWT cookie.

    If the cookie is missing or invalid, the wrapped endpoint returns
    an error response.

    If the JWT is valid, g.current_user is set for the endpoint.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Validate JWT before running the protected route.
        """

        # Reuse the helper so all JWT errors are handled consistently.
        username, error = get_username_from_jwt()

        if error:
            return error

        # Flask's g object stores data for the current request only.
        g.current_user = username
        return func(*args, **kwargs)
    return wrapper


@app.errorhandler(401)
def unauthorized(e):
    """
    Return JSON for 401 Unauthorized errors.

    This keeps authentication failures readable for curl users.
    """

    return jsonify({
        "error": e.description
    }), 401


def api_protected(func):
    """
    Decorator for routes that require an API key.

    Expected request headers:

        Username: alice
        Authorization: Bearer <api_key>

    The Username header tells this beginner sample which user's API key
    list should be checked.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Validate API key before running the protected API route.
        """

        current_app.logger.info("api_protected running")

        # Read both headers used by this lab.
        auth = request.headers.get("Authorization", "")
        username = request.headers.get("Username", "")

        if not username:
            abort(401, description="Missing Username header")

        info = user_db.get(username)

        if not info:
            abort(401, description="Unknown user")

        if not auth.startswith("Bearer "):
            abort(401, description="Missing Authorization Bearer token")

        if auth.startswith("Bearer "):
            # "Bearer abc123" becomes "abc123".
            key = auth.split(" ", 1)[1]

            # Go through all API keys that belong to this user.
            for stored_key in info.get('api_key', []):

                # Compare raw key sent by the client with stored hash.
                if keys_match(key, get_stored_api_key_hash(stored_key)):

                    # Store authenticated API username for route handlers.
                    g.api_username = username
                    return func(*args, **kwargs)

        abort(401, description="Invalid or missing API key or username")

    return wrapper


def load_data():
    """
    Load local network interfaces into the in-memory data store.

    psutil.net_if_addrs() returns interfaces from the operating system.
    This function converts them into simple JSON-friendly dictionaries.
    """

    # Refresh the interfaces resource every time this function runs.
    data["interfaces"] = {}

    # Go through all network interfaces visible to the system.
    for iface, addrs in psutil.net_if_addrs().items():
        data["interfaces"][iface] = []

        # Each interface may have several addresses.
        for a in addrs:
            fam = "MAC"

            if a.family == socket.AF_INET:
                fam = "IPv4"
            elif a.family == socket.AF_INET6:
                fam = "IPv6"

            # Store only beginner-friendly fields.
            data["interfaces"][iface].append({
                "family": fam,
                "address": a.address
            })


# Load operating-system data once when the application starts.
load_data()


@app.after_request
def log_request(response):
    """
    Log each request after Flask creates a response.

    This is intentionally simple: method, path and status code.
    """

    print(request.method, request.path, response.status_code)
    return response


@app.route("/")
def index():
    """
    Browser entry point.

    Redirect users to the Jinja2 login page.
    """

    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route used by both browser users and curl.

    Browser:
    - GET /login shows Jinja2 login form.
    - POST /login receives form data and redirects to dashboard.

    Curl:
    curl -i -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"password1"}' \
     -c cookies.txt
    """

    error = None

    # Browser opens /login with GET, so Flask renders login.html.
    if request.method == "GET":
        return render_template("login.html", error=error)

    # JSON branch keeps the old curl-based API login working.
    if request.is_json:
        body = request.get_json(silent=True)

        if not body:
            return jsonify({"error": "Missing JSON body"}), 400

        username = body.get("username")
        password = body.get("password")

    else:
        # Form branch is used by the HTML login form.
        # The names come from input name="username" and name="password".
        username = request.form.get("username")
        password = request.form.get("password")

    # Try to find the user in the fake database.
    user = user_db.get(username)

    # Passwords in this lab are stored as HMAC hashes.
    # The incoming password is hashed and compared with the stored hash.
    if user and password and user["password"] == hash_key(password):
        token = create_jwt(username)

        if request.is_json:
            # JSON response for curl or API clients.
            resp = make_response(jsonify({
                "message": "Logged in",
                "username": username,
            }))
        else:
            # Browser response redirects to the dashboard.
            resp = make_response(redirect(url_for("dashboard")))

        # Store JWT in an HttpOnly cookie.
        # This file intentionally keeps HTTP, so the Secure cookie flag is not used here.
        resp.set_cookie('jwt', token, httponly=True, samesite='Lax')
        return resp

    # If login failed and request came from curl, return JSON.
    if request.is_json:
        return jsonify({"error": "Invalid credentials"}), 401

    # If login failed and request came from browser, show the form again.
    error = "Invalid credentials"
    return render_template("login.html", error=error), 401


@app.route("/dashboard")
@jwt_protected
def dashboard():
    """
    Jinja2 dashboard for logged-in users.

    The @jwt_protected decorator validates the JWT cookie first.
    This function then renders dashboard.html with metadata needed by
    the template.
    """

    username = g.current_user

    return render_template(
        "dashboard.html",
        username=username,
        role=user_db[username]["role"],
        api_keys=get_api_keys_for_user(username),
        resources=sorted(data.keys()),
    )


@app.route("/dashboard/api-keys", methods=["POST"])
@jwt_protected
def create_api_key_from_dashboard():
    """
    Create a new API key from the dashboard form.

    The real API key value is returned only once in the HTML response.
    The application stores only its hash plus metadata.
    """

    # Generate the secret API key value that the user will copy.
    api_key = secrets.token_urlsafe(32)

    # Store only a hash, not the real API key.
    api_hash = hash_key(api_key)

    # Read optional metadata from the HTML form.
    label = request.form.get("label") or "no label"
    permissions = request.form.getlist("permissions") or ["read"]

    # Dashboard-created API keys use the richer dictionary format.
    user_db[g.current_user]["api_key"].append({
        "api_key_hash": api_hash,
        "label": label,
        "permissions": permissions,
        "created_at": datetime.utcnow().isoformat() + "Z",
    })

    # Re-render dashboard and show the raw API key once.
    return render_template(
        "dashboard.html",
        username=g.current_user,
        role=user_db[g.current_user]["role"],
        api_keys=get_api_keys_for_user(g.current_user),
        resources=sorted(data.keys()),
        new_api_key=api_key,
        message="API key created. Copy it now; it will not be shown again.",
    ), 201


@app.route("/dashboard/api-keys/<int:key_id>/delete", methods=["POST"])
@jwt_protected
def delete_api_key_from_dashboard(key_id):
    """
    Delete an API key from the dashboard.

    Browser forms cannot send DELETE directly, so the dashboard uses
    a POST route for this delete/revoke action.
    """

    # Get the current user's API key list.
    keys = user_db[g.current_user].get("api_key", [])

    if key_id < 0 or key_id >= len(keys):
        return jsonify({"error": "API key not found"}), 404

    # Remove the key. After this, the raw API key no longer works.
    del keys[key_id]

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    """
    Clear JWT cookie and return to login page.
    """

    resp = make_response(redirect(url_for("login")))

    # Delete the browser cookie that stores JWT.
    resp.delete_cookie("jwt")
    return resp


@app.route("/chpasswd", methods=["POST"])
@jwt_protected
def chpasswd():
    """
    Change password for the currently logged-in user.

    This route requires JWT cookie and is meant for curl/API use.

    curl -i -X POST http://localhost:5000/chpasswd \
     -H "Content-Type: application/json" \
      -d '{"new_password":"newsecret123"}' \
      -b cookies.txt
    """

    # Read JSON body safely. If it is not valid JSON, return None.
    data = request.get_json(silent=True)

    if not data or not data.get('new_password'):
        return jsonify({"error": "new_password required"}), 400

    # Store a hash of the new password.
    new_password = hash_key(data.get('new_password'))

    # jwt_protected already set g.current_user.
    current_user = g.current_user

    user_db[current_user]["password"] = new_password
    return jsonify({"message": "Password updated"})

@app.route("/api/newkey", methods=["POST"])
@jwt_protected
def api_new_key():
    """
    Create a new API key using JSON/API flow.

    This route requires JWT cookie.
    It returns the raw API key once and stores only the hash.

    curl -i -X POST http://localhost:5000/api/newkey \
      -H "Content-Type: application/json" \
      -b cookies.txt
    """

    # Generate real API key value.
    api_key  = secrets.token_urlsafe(32)

    # Hash the key before storing it.
    api_hash = hash_key(api_key)

    current_user = g.current_user

    # API-created keys also use the richer metadata format.
    user_db[current_user]["api_key"].append({
        "api_key_hash": api_hash,
        "label": "created through API",
        "permissions": permissions_for_user(current_user),
        "created_at": datetime.utcnow().isoformat() + "Z",
    })

    # Return the real key once.
    return jsonify({"new_api_key": api_key})

@app.route("/<resource>", methods=["GET"])
@api_protected
def get_all(resource):
    """
    Get all entries for a resource.

    This endpoint is protected by API key.
    The resource name comes from the URL path.

    Example:
      curl -i \
        -H "Username: alice" \
        -H "Authorization: Bearer secretapikey1" \
        http://localhost:5000/interfaces
    """

    # Check if requested resource exists in the fake database.
    if resource not in data:
        return jsonify({"error": "not found"}), 404

    return jsonify(data[resource])


@app.route("/<resource>", methods=["POST"])
@api_protected
def create(resource):
    """
    Create a new entry in a resource (requires JSON body with 'id').

    This endpoint is protected by API key.
    If the resource does not exist yet, it is created in memory.

    Example:
      curl -i -X POST \
        -H "Content-Type: application/json" \
        -H "Username: alice" \
        -H "Authorization: Bearer secretapikey1" \
        -d '{"id":"test1","value":"hello"}' \
        http://localhost:5000/notes
    """

    # request.json reads JSON body sent by the client.
    body = request.json

    # Every stored entry needs an id so it can be updated or deleted later.
    if not body or "id" not in body:
        return jsonify({"error": "id required"}), 400

    # Create resource dictionary if it does not exist yet.
    data.setdefault(resource, {})

    # Store the whole JSON body under body["id"].
    data[resource][body["id"]] = body

    return jsonify(body), 201


@app.route("/<resource>/<id>", methods=["PUT"])
@api_protected
def update(resource, id):
    """
    Update an existing entry by id.

    This endpoint is protected by API key.
    It uses PUT because the sample treats the request as an update of
    an existing resource entry.

    Example:
      curl -i -X PUT \
        -H "Content-Type: application/json" \
        -H "Username: alice" \
        -H "Authorization: Bearer secretapikey1" \
        -d '{"value":"updated"}' \
        http://localhost:5000/notes/test1
    """

    # The resource and id must already exist.
    if resource not in data or id not in data[resource]:
        return jsonify({"error": "not found"}), 404

    # Merge incoming JSON fields into the existing dictionary.
    data[resource][id].update(request.json)

    return jsonify(data[resource][id])


@app.route("/<resource>/<id>", methods=["DELETE"])
@api_protected
def delete(resource, id):
    """
    Delete an entry by id.

    This endpoint is protected by API key.

    Example:
      curl -i -X DELETE \
        -H "Username: alice" \
        -H "Authorization: Bearer secretapikey1" \
        http://localhost:5000/notes/test1
    """

    # The resource and id must already exist.
    if resource not in data or id not in data[resource]:
        return jsonify({"error": "not found"}), 404

    # Delete entry from memory.
    del data[resource][id]

    # HTTP 204 means success with no response body.
    return "", 204


@app.route("/search")
@api_protected
def search():
    """
    Search across all resources for a term.

    This endpoint is protected by API key.
    It is intentionally simple: it converts keys and values to strings
    and checks whether the query appears inside them.

    Example:
      curl -i \
        -H "Username: alice" \
        -H "Authorization: Bearer secretapikey1" \
        "http://localhost:5000/search?q=ipv4"
    """

    # Read query parameter from URL, for example /search?q=ipv4.
    q = request.args.get("q", "").lower()
    results = []

    # Search each resource and each item inside that resource.
    for res, items in data.items():
        for k, v in items.items():

            # Convert both id and value to lowercase strings.
            blob = str(k).lower() + str(v).lower()

            if q in blob:
                results.append({res: {k: v}})

    return jsonify(results)


# Run Flask development server only when this file is run directly.
# This Jinja2 variant intentionally stays on HTTP port 5000.
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
