from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import UploadedFile
from app.utils import allowed_file, process_file, generate_dashboard_data
import os

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard_home():
    """Dashboard home page - shows user's uploaded files"""
    files = UploadedFile.query.filter_by(user_id=current_user.id).order_by(UploadedFile.upload_date.desc()).all()
    return render_template('dashboard.html', files=files)

@dashboard_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """File upload page and handler"""
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure the filename
            original_filename = file.filename
            filename = secure_filename(file.filename)
            
            # Add timestamp to avoid conflicts
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
            
            # Save file
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Determine file type
            file_type = 'excel' if ext.lower() in ['.xlsx', '.xls'] else 'csv'
            
            # Save to database
            uploaded_file = UploadedFile(
                filename=filename,
                original_filename=original_filename,
                file_path=file_path,
                file_type=file_type,
                user_id=current_user.id
            )
            db.session.add(uploaded_file)
            db.session.commit()
            
            flash(f'File "{original_filename}" uploaded successfully!', 'success')
            return redirect(url_for('dashboard.view_dashboard', file_id=uploaded_file.id))
        else:
            flash('Invalid file type. Please upload CSV or Excel files only.', 'danger')
            return redirect(request.url)
    
    return render_template('upload.html')

@dashboard_bp.route('/view/<int:file_id>')
@login_required
def view_dashboard(file_id):
    """View dashboard for a specific uploaded file"""
    file = UploadedFile.query.get_or_404(file_id)
    
    # Check if file belongs to current user
    if file.user_id != current_user.id:
        flash('You do not have permission to view this file.', 'danger')
        return redirect(url_for('dashboard.dashboard_home'))
    
    # Process file and generate dashboard data
    try:
        data_summary, charts = generate_dashboard_data(file.file_path, file.file_type)
        return render_template('view_dashboard.html', 
                             file=file, 
                             data_summary=data_summary, 
                             charts=charts)
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'danger')
        return redirect(url_for('dashboard.dashboard_home'))

@dashboard_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    """Delete an uploaded file"""
    file = UploadedFile.query.get_or_404(file_id)
    
    # Check if file belongs to current user
    if file.user_id != current_user.id:
        flash('You do not have permission to delete this file.', 'danger')
        return redirect(url_for('dashboard.dashboard_home'))
    
    # Delete physical file
    try:
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'warning')
    
    # Delete from database
    db.session.delete(file)
    db.session.commit()
    
    flash(f'File "{file.original_filename}" deleted successfully.', 'success')
    return redirect(url_for('dashboard.dashboard_home'))
