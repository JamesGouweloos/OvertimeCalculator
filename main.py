"""
Firebase Cloud Functions entry point for Overtime Analysis Platform.
"""

from app import app

# Export the Flask app for Firebase Functions
# Firebase Functions expects the app to be accessible
def app_function(request):
    """Handle requests for Firebase Functions."""
    return app(request.environ, lambda status, headers: None)

# For App Hosting, we can also export directly
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

