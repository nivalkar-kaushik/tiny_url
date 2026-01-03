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

