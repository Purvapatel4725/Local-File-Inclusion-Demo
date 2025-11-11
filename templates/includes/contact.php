<?php
// Demo file: Contact page
// This is a safe demo file included in the LFI demonstration
?>
<div>
    <h2>Contact Us</h2>
    <p>Fill out the form below to get in touch with us.</p>
    <hr>
    
    <form method="POST" action="#" style="margin-top: 20px;">
        <div style="margin-bottom: 15px;">
            <label for="name" style="display: block; margin-bottom: 5px; font-weight: 600;">Name:</label>
            <input type="text" id="name" name="name" style="width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid #bdc3c7; font-size: 14px;" placeholder="Enter your name">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="email" style="display: block; margin-bottom: 5px; font-weight: 600;">Email:</label>
            <input type="email" id="email" name="email" style="width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid #bdc3c7; font-size: 14px;" placeholder="Enter your email">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="subject" style="display: block; margin-bottom: 5px; font-weight: 600;">Subject:</label>
            <input type="text" id="subject" name="subject" style="width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid #bdc3c7; font-size: 14px;" placeholder="Enter subject">
        </div>
        
        <div style="margin-bottom: 15px;">
            <label for="message" style="display: block; margin-bottom: 5px; font-weight: 600;">Message:</label>
            <textarea id="message" name="message" rows="5" style="width: 100%; max-width: 400px; padding: 8px 12px; border: 1px solid #bdc3c7; font-size: 14px; font-family: inherit;" placeholder="Enter your message"></textarea>
        </div>
        
        <button type="submit" style="padding: 10px 20px; background: #27ae60; color: white; border: none; font-size: 14px; cursor: pointer;">Submit</button>
    </form>
    
    <p style="margin-top: 20px; font-size: 12px; color: #7f8c8d;"><em>Note: This is a demo contact form and does not actually submit data.</em></p>
</div>
