from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User
from wtforms import ValidationError
 
 
 
class CategoryForm(FlaskForm):
   name = StringField('Category Name', validators=[Required(), Length(1, 64)])
   submit = SubmitField('Submit')
 
class PostForm(FlaskForm):
   title = StringField('Title', validators=[Required(), Length(1, 64)])
   content = TextAreaField('Body', validators=[Required()])
   submit = SubmitField('Submit')