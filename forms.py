from wtforms import SelectMultipleField, StringField, PasswordField, SelectField, IntegerField, DateField
from wtforms.validators import NumberRange, InputRequired, DataRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField(
        "Username",
        validators = [InputRequired(), Length(min = 1, max=20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

class RegisterForm(FlaskForm):
    """Registration Form"""    

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )



class MarsRoverForm(FlaskForm):
    """Choose a camera type to filter images for Mars Rover feature"""
    
    cameras = SelectMultipleField('Choose Cameras',
                                  choices=[('FHAZ', 'Front Hazard Avoidance Camera'),
                                           ('RHAZ', 'Rear Hazard Avoidance Camera'),
                                           ('MAST', 'Mast Camera'),
                                           ('CHEMCAM', 'Chemistry and Camera Complex'),
                                           ('MAHLI', 'Mars Hand Lens Imager'),
                                           ('MARDI', 'Mars Descent Imager'),
                                           ('NAVCAM', 'Navigation Camera'),
                                           ('PANCAM', 'Panoramic Camera'),
                                           ('MINITES', 'Miniature Thermal Emission Spectrometer (Mini-TES)')],
                                  validators=[Optional()])
    
    date = DateField(
        'Earth Date', validators=[Optional()]
        
        )
    
    



class SearchAPODForm(FlaskForm):
    """Params(filter) for APOD request"""
    
    date = DateField(
        'Date', validators=[Optional()]
        
        )
    
    start_date = DateField(
        'Start Date', validators=[Optional()]
        
        )
    
    end_date = DateField(
        'End Date', validators=[Optional()]
        
        )
    
    count = IntegerField(
        'Count', validators=[Optional(),NumberRange(max=20)]
        
        )


