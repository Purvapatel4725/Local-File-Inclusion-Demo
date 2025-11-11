#!/usr/bin/env python3
"""
Simple script to initialize or recreate users.json with demo data.
Run this if users.json is missing or corrupted.
"""

import json
import os

def init_users():
    """Create users.json with demo user data."""
    users = {
        "1": {
            "id": 1,
            "username": "alice",
            "password": "demo123",
            "name": "Alice Johnson",
            "email": "alice.johnson@demo.local",
            "department": "Engineering",
            "notes": "Lead developer on Project Alpha. Prefers morning standups."
        },
        "2": {
            "id": 2,
            "username": "bob",
            "password": "demo123",
            "name": "Bob Smith",
            "email": "bob.smith@demo.local",
            "department": "Marketing",
            "notes": "Working on Q4 campaign. Available for client meetings."
        },
        "3": {
            "id": 3,
            "username": "charlie",
            "password": "demo123",
            "name": "Charlie Brown",
            "email": "charlie.brown@demo.local",
            "department": "Sales",
            "notes": "Top performer this quarter. Specializes in enterprise accounts."
        }
    }
    
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    users_file = os.path.join(data_dir, "users.json")
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)
    
    print(f"✓ Created {users_file} with {len(users)} demo users")
    print("  Users: alice, bob, charlie (all passwords: demo123)")

if __name__ == "__main__":
    init_users()

