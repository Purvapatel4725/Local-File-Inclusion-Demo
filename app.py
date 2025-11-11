#!/usr/bin/env python3
"""
Intentionally Vulnerable IDOR Demo - Flask Application

WARNING: This application contains intentional security vulnerabilities
for educational purposes only. DO NOT deploy to production or expose to public networks.

The vulnerability: The /profile/<id> endpoint does not verify that the
authenticated user owns the requested profile ID, allowing unauthorized access.
"""

import json
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load demo user data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def load_users():
    """Load users from JSON file."""
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_user_by_username(username):
    """Find user by username."""
    users = load_users()
    for user in users.values():
        if user.get("username") == username:
            return user
    return None

def get_user_by_id(user_id):
    """Find user by ID."""
    users = load_users()
    return users.get(str(user_id))

def get_authenticated_user():
    """Extract authenticated user from request headers.
    
    In this demo, we use a simple token scheme: X-Demo-Auth header
    contains the username. In production, this would be a proper JWT or session.
    """
    auth_header = request.headers.get("X-Demo-Auth")
    if not auth_header:
        return None
    return get_user_by_username(auth_header)

@app.route("/")
def index():
    """Home page with login form and profile links."""
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """Unauthenticated login endpoint.
    
    Accepts JSON: {"username": "...", "password": "..."}
    Returns: {"success": true, "token": "username"} or error.
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    
    user = get_user_by_username(username)
    if not user or user.get("password") != password:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Return a simple token (in production, this would be a secure JWT)
    # The token is just the username for demo purposes
    return jsonify({
        "success": True,
        "token": username,
        "message": f"Logged in as {username}"
    }), 200

@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    """
    INTENTIONALLY VULNERABLE PROFILE ENDPOINT
    
    This endpoint demonstrates IDOR (Insecure Direct Object Reference):
    - It checks if the user is authenticated (has a valid token)
    - BUT it does NOT verify that the authenticated user owns the requested profile ID
    - This allows any authenticated user to access any other user's profile
    
    VULNERABILITY: Missing authorization check
    Should verify: if current_user_id != user_id: return 403
    """
    # Check authentication
    authenticated_user = get_authenticated_user()
    if not authenticated_user:
        return jsonify({"error": "Authentication required. Send X-Demo-Auth header with your username."}), 401
    
    # Load the requested user profile
    requested_user = get_user_by_id(user_id)
    if not requested_user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404
    
    # VULNERABILITY: We return the profile without checking if authenticated_user.id == user_id
    # This is the intentional bug - any authenticated user can access any profile!
    
    # Return profile data (excluding password)
    profile_data = {
        "id": requested_user["id"],
        "name": requested_user["name"],
        "email": requested_user["email"],
        "department": requested_user["department"],
        "notes": requested_user["notes"]
    }
    
    return jsonify(profile_data), 200

@app.route("/profile/<int:user_id>/html", methods=["GET"])
def get_profile_html(user_id):
    """HTML view of profile (for browser-based demo).
    
    This page will fetch profile data via JavaScript from the /profile/<id> API endpoint.
    The user_id is passed to the template so it knows which profile to fetch.
    """
    return render_template("profile.html", user_id=user_id)

if __name__ == "__main__":
    # Ensure users.json exists
    if not os.path.exists(USERS_FILE):
        print("Warning: users.json not found. Run init_db.py first.")
    
    # Bind to 127.0.0.1 (localhost only) for safety
    app.run(host="127.0.0.1", port=5000, debug=True)

