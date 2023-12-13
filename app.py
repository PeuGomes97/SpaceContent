from flask import Flask, render_template, redirect, session, jsonify, request, url_for, flash
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Bcrypt, SQLAlchemy, Favorite
from forms import RegisterForm, LoginForm, SearchAPODForm, MarsRoverForm
import requests
import datetime
from keys import API_KEY
from dotenv import load_dotenv, find_dotenv
import os

APOD_API_URL = "https://api.nasa.gov/planetary/apod"
MARSROVER_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

app = Flask(__name__)

load_dotenv(find_dotenv())
print(os.getenv('SECRET_KEY'))

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///nasausers"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route("/")
def homepage():
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")
    else:
        return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")
    else:
        form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        session['user_id'] = user.id

        return redirect(f"/users/{user.id}")
    
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(f"/users/{session['user_id']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(f"/users/{user.id}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/login")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    else:
        user = User.query.get(user_id)
        return render_template("/users/show.html", user=user)


@app.route("/users/<int:user_id>/result/apod", methods=['GET', 'POST'])
def result_for_apod(user_id):
    if "username" not in session or user_id != session['user_id']:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    
    form = SearchAPODForm()
    message = None
    images_info = []
    
    if form.validate_on_submit():
        params = {'api_key': API_KEY} 

        params['date'] = form.date.data if form.date.data else None
        params['start_date'] = form.start_date.data if form.start_date.data else None
        params['end_date'] = form.end_date.data if form.end_date.data else None
        params['count'] = form.count.data if form.count.data else None

        params = {k: v for k, v in params.items() if v is not None}
        res = requests.get(APOD_API_URL, params=params)

        data = res.json() if res.status_code == 200 else None
        if data is None:
            message = "No data found for that date!"
        else:
            if not isinstance(data, list):
                data = [data]
                
            images_info = [{'title': entry['title'], 'explanation': entry['explanation'], 'date': entry['date'], 'url': entry['url']} for entry in data]
    
            if not images_info:
                message = "Error fetching data for APOD"
    
        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        favorited_images = [fav.image_url for fav in user_favorites]
    
        return render_template("/users/result.html", form=form, images_info=images_info, message=message, favorited_images=favorited_images, user_id=user_id)
    
    res = requests.get(APOD_API_URL, params={'api_key': API_KEY})
    data = res.json()
    
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorited_images = [fav.image_url for fav in user_favorites]

    return render_template("/users/result.html", form=form, data=data, favorited_images=favorited_images, user_id=user_id)


@app.route("/users/<int:user_id>/mars_photos", methods=['GET', 'POST'])
def mars_photos(user_id):
    if "username" not in session or user_id != session['user_id']:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    
    form = MarsRoverForm()
    message = None
    default_date = "2023-12-01"

    if request.method == 'POST' and form.validate_on_submit():
        camera = form.cameras.data
        date = form.date.data

        params = {
            'api_key': API_KEY,
            'earth_date': date,
            'camera': camera
        }

        params = {k: v for k, v in params.items() if v is not None}
 
        res = requests.get(MARSROVER_API_URL, params=params)

        data = res.json() if res.status_code == 200 else None
        if data is None:
            message = "No data found for that date!"
        else:    
            photos = data['photos']
            photos = photos[:10]
            images_info = [{'img_src': photo['img_src'], 'rover_name': photo['rover']['name'], 'camera': photo['camera']['name'], 'date': photo['earth_date']} for photo in photos]

            if not images_info:
                message = "No data found for that date!"
        
        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        favorited_images = [fav.image_url for fav in user_favorites]

        return render_template("/users/marsrover.html", form=form, images_info=images_info, message=message, favorited_images=favorited_images)
    
    if request.method == 'GET':
        params = {
            'api_key': API_KEY,
            'earth_date': default_date,
            'camera': 'FHAZ'
        }
        res = requests.get(MARSROVER_API_URL, params=params)

        data = res.json() if res.status_code == 200 else None
        date = data['photos'][0]['earth_date']
        image = data['photos'][0]['img_src']
        rover = data['photos'][0]['rover']['name']
        camera = data['photos'][0]['camera']['name']

        user_favorites = Favorite.query.filter_by(user_id=user_id).all()
        favorited_images = [fav.image_url for fav in user_favorites]

        return render_template("/users/marsrover.html", form=form, camera=camera, rover=rover, date=date, image=image, favorited_images=favorited_images)

    return render_template("/users/marsrover.html")



@app.route("/users/<int:user_id>/favorites", methods=['GET'])
def list_favorites(user_id):
    """List user's favorite images"""

    if "user_id" not in session or user_id != session['user_id']:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    
    # Query DB based on user's id to see list about favorited images

    user = User.query.get_or_404(user_id)
    favorite_images = []
    favorite_ids = []  # Lista para armazenar os IDs dos favoritos
    if user.favorites:
        favorite_images = [fav.image_url for fav in user.favorites]
        favorite_ids = [fav.id for fav in user.favorites]  # Recupera os IDs dos favoritos
    else:
        flash("No Favorites added yet!")

    return render_template("favorites.html", favorite_images=favorite_images, favorite_ids=favorite_ids)





@app.route("/users/<int:user_id>/favorites/<int:favorite_id>", methods=['DELETE'])
def delete_favorite(user_id, favorite_id):
    if "user_id" not in session or user_id != session['user_id']:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    
    favorite_to_delete = Favorite.query.filter_by(id=favorite_id, user_id=user_id).first_or_404()

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({"message": "Favorito removido com sucesso!"}), 200



@app.route("/users/<int:user_id>/add_to_favorites", methods=['POST'])
def add_to_favorites(user_id):
    if "username" not in session or user_id != session['user_id']:
        flash("Unauthorized. Please log in.")
        return redirect("/login")
    
    image_url = request.form.get('image_url')

    existing_favorite = Favorite.query.filter_by(user_id=user_id, image_url=image_url).first()
    if existing_favorite:
        flash('Photo already added')
    else:
        favorite = Favorite(image_url=image_url, user_id=user_id)
        db.session.add(favorite)
        db.session.commit()

    return jsonify({"message": "Image added to favorites successfully!"}), 200

