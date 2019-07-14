from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

class ImageForm(FlaskForm):
    target_word = StringField("Target Word", validators=[DataRequired()])

    rotate_image = SelectField('Rotate Image?', choices=[(1, 'yes'), (0, 'no')])

    submit = SubmitField("Classify")