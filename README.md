# IDOR Vulnerability Demo

## ⚠️ SECURITY WARNING

**This application contains intentional security vulnerabilities for educational purposes only.**

- **DO NOT** deploy to production
- **DO NOT** expose to public networks
- **DO NOT** use with real user data
- Run **ONLY** in isolated lab environments (localhost)

---

## What is IDOR?

**Insecure Direct Object Reference (IDOR)** is a vulnerability that occurs when an application provides direct access to objects (like user profiles, files, or records) based on user-supplied input without proper authorization checks.

### The Vulnerability in This Demo

This Flask application demonstrates IDOR by implementing a profile endpoint (`/profile/<id>`) that:
- ✅ Checks if the user is **authenticated** (has a valid token)
- ❌ **Does NOT** verify that the authenticated user **owns** the requested profile ID

This allows any authenticated user to access any other user's profile by simply changing the ID in the URL.

---

## Project Structure

```
IDOR/
├── README.md              # This file
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
├── app.py                 # Flask application (contains the vulnerability)
├── init_db.py             # Script to initialize demo user data
├── demo_commands.txt      # Step-by-step curl commands for the demo
├── data/
│   └── users.json         # Demo user data (3 fake users)
└── templates/
    ├── index.html         # Login page
    └── profile.html       # Profile view page
```

---

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Terminal/command prompt access

### Startup Instructions

1. **Start the application:**
   ```bash
   docker compose up --build
   ```

2. **Wait for the startup message:**
   ```
   * Running on http://127.0.0.1:5000
   ```

3. **Access the web interface:**
   - Open browser: http://127.0.0.1:5000
   - Or use the curl commands in `demo_commands.txt`

4. **Stop the application:**
   - Press `Ctrl+C` in the terminal, or run:
   ```bash
   docker compose down
   ```

---

## Demo User Credentials

| Username | Password | User ID |
|----------|----------|---------|
| alice    | demo123  | 1       |
| bob      | demo123  | 2       |
| charlie  | demo123  | 3       |

---

## Demonstrating the Vulnerability

### Method 1: Using curl (Command Line)

See `demo_commands.txt` for complete step-by-step commands. Quick example:

```bash
# 1. Login as alice
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "demo123"}'
# Response: {"success":true,"token":"alice",...}

# 2. Access alice's own profile (legitimate)
curl -X GET http://127.0.0.1:5000/profile/1 \
  -H "X-Demo-Auth: alice"
# Response: Alice's profile data

# 3. IDOR EXPLOIT: Access bob's profile as alice (unauthorized!)
curl -X GET http://127.0.0.1:5000/profile/2 \
  -H "X-Demo-Auth: alice"
# Response: Bob's profile data (SHOULD NOT BE ALLOWED!)
```

### Method 2: Using the Web Interface

1. Open http://127.0.0.1:5000 in your browser
2. Login as `alice` with password `demo123`
3. Click "Profile 2 (Bob)" link
4. Observe that you can view Bob's profile even though you're logged in as Alice
5. Try accessing Profile 3 (Charlie) as well

---

## Expected Demo Output

### Login Success
```json
{
  "success": true,
  "token": "alice",
  "message": "Logged in as alice"
}
```

### Legitimate Profile Access (Own Profile)
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice.johnson@demo.local",
  "department": "Engineering",
  "notes": "Lead developer on Project Alpha. Prefers morning standups."
}
```

### IDOR Exploit (Unauthorized Access)
```json
{
  "id": 2,
  "name": "Bob Smith",
  "email": "bob.smith@demo.local",
  "department": "Marketing",
  "notes": "Working on Q4 campaign. Available for client meetings."
}
```
**Note:** This response should return a 403 Forbidden error, but it doesn't due to the vulnerability.

---

## Root Cause

The vulnerability exists in `app.py`, function `get_profile()`:

```python
@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    authenticated_user = get_authenticated_user()
    if not authenticated_user:
        return jsonify({"error": "Authentication required"}), 401
    
    requested_user = get_user_by_id(user_id)
    if not requested_user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404
    
    # VULNERABILITY: Missing authorization check!
    # Should verify: if authenticated_user["id"] != user_id: return 403
    
    return jsonify(profile_data), 200  # Returns any profile if authenticated
```

**The bug:** The code checks authentication but never verifies that `authenticated_user["id"] == user_id`.

---

## Mitigations

### 1. **Server-Side Authorization Check** (Recommended)

Add an ownership verification before returning the profile:

```python
@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    authenticated_user = get_authenticated_user()
    if not authenticated_user:
        return jsonify({"error": "Authentication required"}), 401
    
    # FIX: Verify ownership
    if authenticated_user["id"] != user_id:
        return jsonify({"error": "Forbidden: You can only access your own profile"}), 403
    
    requested_user = get_user_by_id(user_id)
    if not requested_user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404
    
    return jsonify(profile_data), 200
```

### 2. **Use Indirect Object References**

Instead of exposing sequential IDs (1, 2, 3), use unguessable UUIDs or hashed tokens:

```python
# Instead of: /profile/1
# Use: /profile/a3f8b9c2-d4e5-4f6a-8b9c-0d1e2f3a4b5c
```

### 3. **Role-Based Access Control (RBAC)**

Implement role-based permissions where users can only access resources they're authorized for:

```python
def can_access_profile(authenticated_user, requested_user_id):
    # Admin can access all profiles
    if authenticated_user.get("role") == "admin":
        return True
    # Users can only access their own
    return authenticated_user["id"] == requested_user_id
```

---

## Suggested Screenshots for Course Report

1. **Login page** (http://127.0.0.1:5000)
2. **Login success response** (JSON token returned)
3. **Accessing own profile** (Profile 1 as alice - legitimate)
4. **IDOR exploit** (Profile 2 as alice - unauthorized access)
5. **IDOR exploit** (Profile 3 as alice - another unauthorized access)
6. **Browser view of unauthorized profile** (showing the vulnerability warning)
7. **curl command demonstrating the exploit**
8. **Server logs** (if applicable)
9. **Code snippet showing the vulnerable endpoint**
10. **Code snippet showing the fix** (authorization check)

**Keep total screenshots ≤ 15 for the course report.**

---

## Technical Details

- **Framework:** Flask 3.0.0
- **Python Version:** 3.11
- **Authentication:** Simple token scheme (X-Demo-Auth header with username)
- **Port Binding:** 127.0.0.1:5000 (localhost only)
- **Data Storage:** JSON file (`data/users.json`)

---

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "127.0.0.1:5001:5000"  # Use port 5001 instead
```

### Users.json Missing
Run the initialization script:
```bash
python init_db.py
```

### Container Won't Start
Check Docker logs:
```bash
docker compose logs idor-demo
```

---

## License & Disclaimer

This code is provided for educational purposes only. The authors are not responsible for any misuse of this code. Always follow responsible disclosure practices when testing security vulnerabilities.

---

## References

- [OWASP: Insecure Direct Object Reference](https://owasp.org/www-community/vulnerabilities/Insecure_Direct_Object_Reference)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)

