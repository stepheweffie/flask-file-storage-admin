from flask_admin import AdminIndexView, expose, form
from flask import request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from markupsafe import Markup
import shutil
from models import db, Upload
from forms import DropzoneForm
from flask_admin.contrib import sqla
from forms import CKTextAreaField
from flask_admin.form import rules
from plugins import Plugins 
    

class HomeView(AdminIndexView):    
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        uploads_dir = current_app.config['UPLOAD_PATH']
        saved_dir = current_app.config['FILE_PATH']
        dropzone = DropzoneForm()
        uploads = self.get_uploads(uploads_dir)
        username = current_app.config['APP_USERNAME']
        plugins = Plugins.render_plugins()
        if request.method == 'POST':
            uploaded_files = request.files.getlist("file")
            if uploaded_files:
                for file in uploaded_files:
                    if file:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
                        add_upload = self.handle_file_upload(filename, file, uploads_dir)
                        file.save(file_path)    
            
            else:
                clear = self.clear_uploads(uploads_dir)
                        
        return self.render('admin/index.html', form=dropzone, uploads=uploads, username=username, plugins=plugins)

    def get_uploads(self, uploads_dir):
        files = []
        if os.path.exists(uploads_dir):
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                file_type = self.get_file_type(filename)
                files.append({
                    'name': filename,
                    'path': file_path,
                    'type': file_type
                })
        return files
    
    def get_file_type(self, filename):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in ['.mp4', '.avi', '.mov']:
            return 'video'
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        else:
            return 'file'
        
    def handle_file_upload(self, filename, file_data, uploads_dir):
        try:
            if os.path.exists(uploads_dir):
                filename = secure_filename(filename)        
                file_path = os.path.join(uploads_dir, filename)

                with open(file_path, 'wb') as f:
                    f.write(file_data)
            
                file_type = self.get_file_type(filename)
            
                upload = Upload(name=filename, path=file_path, type=file_type)

                db.session.add(upload)
                db.session.commit()
                return True
            
        except Exception as e:
            return False, str(e)

    def save_uploads(self, uploads_dir, saved_dir):
        selected_files = os.listdir(uploads_dir)
        
        for filename in selected_files:
            filename = secure_filename(filename)
            source_path = os.path.join(uploads_dir, filename)

            dest = os.path.join(saved_dir, filename)
            if os.path.exists(source_path):
                shutil.move(source_path, dest)       

    @expose('/clear_uploads', methods=['POST'])
    def clear_uploads(self):
        uploads_dir = current_app.config['UPLOAD_PATH']
        saved_dir = current_app.config['FILE_PATH']
        self.save_uploads(uploads_dir, saved_dir)
        try:
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        except Exception as e:
            flash(f'Error clearing uploads: {str(e)}', 'error')
        return redirect(url_for('.index'))

    @expose('/files/<path:filename>')
    def download_file(self, filename):
        return send_from_directory(uploads_dir, filename, as_attachment=True)
