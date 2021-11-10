from wtforms import StringField,TextAreaField, SubmitField, SelectField
from wtforms.validators import Required, Length
from flask_wtf import FlaskForm


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post_title = StringField('Post title', validators=[Required()])
    content = TextAreaField('Body', validators=[Required()])
    category = SelectField('Post category',choices=[('Select a category','Select a category'),('Pickup lines', 'Pickup lines'),('Interview','Interview'),('Product','Product'),('Promotions','Promotions')], validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Body', validators=[Required()])
    submit = SubmitField('Submit')