<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LFI Demo - Home</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: #ecf0f1;
            padding: 20px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            border-top: 1px solid #bdc3c7;
            margin-top: 40px;
            font-size: 12px;
            color: #7f8c8d;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border: 1px solid #ddd;
        }
        h1 {
            font-size: 28px;
            margin-bottom: 20px;
            color: #34495e;
            font-weight: 400;
        }
        p {
            margin-bottom: 15px;
            color: #555;
        }
        .links {
            margin: 25px 0;
        }
        .links h3 {
            font-size: 18px;
            margin-bottom: 12px;
            font-weight: 400;
            color: #34495e;
        }
        .links a {
            display: inline-block;
            margin-right: 10px;
            margin-bottom: 8px;
            padding: 8px 16px;
            background: #3498db;
            color: white;
            text-decoration: none;
            font-size: 14px;
        }
        .links a:hover {
            background: #2980b9;
        }
        .form-section {
            margin-top: 30px;
            padding-top: 25px;
            border-top: 1px solid #e0e0e0;
        }
        .form-section h3 {
            font-size: 18px;
            margin-bottom: 12px;
            font-weight: 400;
            color: #34495e;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-size: 14px;
            color: #555;
        }
        input[type="text"] {
            width: 100%;
            max-width: 400px;
            padding: 8px 12px;
            border: 1px solid #bdc3c7;
            font-size: 14px;
            margin-bottom: 10px;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #3498db;
        }
        button {
            padding: 8px 20px;
            background: #27ae60;
            color: white;
            border: none;
            font-size: 14px;
            cursor: pointer;
        }
        button:hover {
            background: #229954;
        }
        small {
            display: block;
            margin-top: 8px;
            font-size: 12px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Local File Inclusion Demo</h1>

        <p>This demo application demonstrates a Local File Inclusion (LFI) vulnerability. Use the links below or the form to view different pages.</p>

        <div class="links">
            <h3>Quick Links:</h3>
            <a href="vulnerable.php?page=about.php">About</a>
            <a href="vulnerable.php?page=contact.php">Contact</a>
            <a href="vulnerable.php?page=help.php">Help</a>
        </div>

        <div class="form-section">
            <h3>Custom Page Loader:</h3>
            <form method="GET" action="vulnerable.php">
                <label for="page">Page to load:</label>
                <input type="text" name="page" id="page" placeholder="e.g., about.php" value="<?php echo htmlspecialchars($_GET['page'] ?? ''); ?>">
                <button type="submit">Load Page</button>
            </form>
            <small>Try entering different file names to see how the application handles file inclusion.</small>
        </div>
    </div>
    
    <div class="footer">
        Copyright 2025 by Purva Patel
    </div>
</body>
</html>
