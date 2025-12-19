#!/usr/bin/env python3
"""
Dashboard Generator Application
Main entry point for the Flask application
"""

import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Use environment variable to control debug mode (default to False for safety)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
