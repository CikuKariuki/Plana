from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class ReviewForm(FlaskForm):
    review = TextAreaField('Service Review',validators=[Required()])
    submit = SubmitField('submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class ProviderForm(FlaskForm):
    location = StringField("Location", validators = [Required()])
    content = TextAreaField('Why choose you?')
    submit = SubmitField('Submit')