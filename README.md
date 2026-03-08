# TinyURL – Django URL Shortener

A simple URL shortener built using Django, Tailwind CSS, and HTMX.

## Features
- User authentication (Signup, Login, OTP verification)
- Short URL creation
- Redirect with click analytics
- Dashboard for managing links

## Tech Stack
- Django
- Tailwind CSS
- HTMX
- SQLite (dev)

## Setup

```bash
git clone https://github.com/yourusername/tiny_url.git
cd tiny_url
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


### Current Features

1. **User Authentication**
   - User registration and login
   - Session management for anonymous users
   - OTP verification

2. **URL Shortening**
   - Convert long URLs to short codes
   - Support for both authenticated and anonymous users
   - Unique code generation
   - Redirection to original URLs

3. **Analytics**
   - Track click counts
   - Device type detection (mobile, tablet, desktop)
   - Browser and OS detection
   - IP address tracking
   - Timestamp tracking

4. **Dashboard**
   - List of user's shortened URLs
   - Click count per URL
   - Full short URLs with domain

5. **Security**
   - URL validation
   - Active/inactive URL status
   - Secure session handling

### Features to Add/Improve

1. **Enhanced Analytics**
   - Click heatmaps by time of day
   - Geographic location visualization
   - Referrer tracking
   - Click patterns over time (daily/weekly/monthly)
   - Custom date range filtering

2. **User Experience**
   - Custom alias/slug support
   - Link expiration dates
   - Password protection for links
   - Link scheduling (active between specific dates)
   - Bulk URL shortening

3. **Security**
   - Rate limiting
   - CAPTCHA for anonymous users
   - Malicious URL detection
   - Click fraud detection

4. **API**
   - RESTful API for URL shortening
   - API key authentication
   - Bulk operations
   - Webhook support for analytics

5. **Performance**
   - Caching for frequently accessed URLs
   - Database optimization for analytics
   - Asynchronous analytics processing

6. **User Management**
   - Profile management
   - API key management
   - Two-factor authentication
   - Team/Organization support

7. **UI/UX**
   - Responsive design improvements
   - Dark mode
   - Custom branding
   - QR code generation
   - Preview of destination page

8. **Advanced Features**
   - A/B testing for different URLs
   - UTM parameter support
   - Integration with analytics platforms
   - Custom domain support
   - Link retargeting

9. **Monitoring**
   - Uptime monitoring
   - Performance metrics
   - Error tracking
   - Usage analytics

10. **Documentation**
    - API documentation
    - User guides
    - Developer documentation
    - Analytics interpretation guide







Improvements (Fix/Enhance Existing)
High Priority
Email OTP sending — currently only prints to console; needs actual email sending via SMTP
OTP resend button — UI exists but functionality is not implemented
Copy-to-clipboard — no button to copy the generated short URL

Admin registration — models not registered in Django admin panel

Empty test files — both links/tests.py and accounts/tests.py are completely empty

Medium Priority


Pagination — dashboard and analytics have no pagination (will break with large data)

Delete/Deactivate URL — users can't delete or disable their short URLs
Analytics charts — currently just plain text counts; no visual charts
Click trends — daily/weekly/monthly breakdown instead of just total clicks
Environment variables — secret key, debug flag, DB settings exposed in settings.py
Low Priority
Error handling UX — better error messages across forms
ALLOWED_HOSTS — empty in settings (will fail in production)
Optimize analytics queries — raw queries not aggregated efficiently for scale
New Features to Add
Core URL Features
Custom alias — let users choose their own short code (e.g. /my-link)
URL expiration — set an expiry date after which link stops working
Password-protected links — require a password to access redirect
Link activation toggle — enable/disable a link without deleting it
Analytics Enhancements
Geographic tracking — country field exists but unused; integrate IP-to-country lookup
Referrer tracking — track where clicks are coming from (Google, Twitter, etc.)
Click timeline chart — bar/line chart of clicks over time
Unique vs. total clicks — distinguish repeat visits from unique visitors
User Experience
QR code generation — generate a QR code for each short URL
Bulk URL shortening — shorten multiple URLs at once
API endpoints — REST API so developers can integrate programmatically
Dark mode — UI toggle
Security
Rate limiting — prevent abuse on /create/ and redirect endpoints
Malicious URL detection — check URLs against a blocklist (Google Safe Browsing API)
CAPTCHA for anonymous users — prevent bot abuse