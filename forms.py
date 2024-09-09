from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import fields, widgets

class DropzoneForm(FlaskForm):
    upload = FileField(validators=[FileRequired()])

# Custom widget and field for CKEditor
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()

# If you have any other custom forms, add them here
