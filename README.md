# Dashboard Generator

A full-stack web application that dynamically generates interactive dashboards from uploaded Excel or CSV files.

## Features

- **User Authentication**: Secure sign-up and login system with session management
- **File Upload**: Upload CSV and Excel files (up to 16MB)
- **Dynamic Dashboard Generation**: Automatically generates interactive visualizations using Plotly
- **Data Analysis**: View summary statistics, data previews, and multiple chart types
- **User-Friendly Interface**: Modern, responsive UI built with Bootstrap 5
- **File Management**: View, manage, and delete uploaded files

## Technologies Used

### Backend
- **Flask**: Web framework
- **Flask-Login**: User session management
- **Flask-SQLAlchemy**: Database ORM
- **SQLite**: Database for user and file storage
- **Pandas**: Data processing and analysis
- **Plotly**: Interactive data visualizations

### Frontend
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 5**: Responsive UI framework
- **Bootstrap Icons**: Icon library
- **JavaScript**: Client-side interactivity

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DHARSAN09/dashboard-generator.git
   cd dashboard-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your web browser and navigate to: `http://localhost:5000`

## Usage

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Upload File**: Navigate to the Upload page and select a CSV or Excel file
4. **View Dashboard**: After upload, you'll be redirected to an interactive dashboard showing:
   - Data summary (rows, columns)
   - Data preview table
   - Multiple visualizations:
     - Summary statistics table
     - Distribution histograms
     - Bar charts for categorical data
     - Correlation heatmaps
     - Scatter plots
     - Box plots
5. **Manage Files**: View all your uploaded files from the dashboard home and delete files as needed

## Project Structure

```
dashboard-generator/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models (User, UploadedFile)
│   ├── auth.py              # Authentication routes
│   ├── dashboard.py         # Dashboard and file upload routes
│   ├── utils.py             # Data processing utilities
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   └── view_dashboard.html
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   └── uploads/             # Uploaded files directory
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Features in Detail

### Authentication
- Secure password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Password validation (minimum 6 characters)
- Username and email uniqueness checks

### Dashboard Visualizations
The application automatically generates the following visualizations based on your data:
- **Summary Statistics**: Statistical overview of numeric columns
- **Distribution Plots**: Histograms showing data distribution
- **Categorical Analysis**: Bar charts for top values in categorical columns
- **Correlation Analysis**: Heatmaps showing relationships between numeric variables
- **Scatter Plots**: Relationships between pairs of numeric variables
- **Box Plots**: Distribution and outlier detection for numeric columns

### Data Support
- **CSV files**: Comma-separated values
- **Excel files**: .xlsx and .xls formats
- Automatic data type detection
- Handles missing values
- Supports various data types (numeric, categorical, datetime)

## Security Considerations

- Passwords are hashed using Werkzeug's security module
- File uploads are validated and sanitized
- User authentication required for all dashboard operations
- Session-based authentication with secure cookies
- File size limits to prevent abuse (16MB max)

## Future Enhancements

- Export dashboards as PDF or images
- Advanced filtering and data manipulation
- Custom visualization builder
- Sharing dashboards with other users
- API endpoints for programmatic access
- Support for more file formats (JSON, Parquet)
- Real-time data updates
- Collaborative features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

DHARSAN09

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
