from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,ProviderForm
from .. models import Reviews,User,Cars,Providers,Grounds,Caterers
from .. models import Photography,Tents,Songs
from flask import jsonify
from flask_login import login_required,UserMixin,current_user
from app import db

# import markdown2

@main.route('/')
def index():
    '''
    view root page function that returns the index page and its data
    '''
    # return redirect(url_for('main.cars'))

    title = "Plan your event without hustle"
    return render_template('index.html')

@main.route("/review/<int:id>",methods=['GET','POST'])
@login_required
def review(id):
    form = ReviewForm()
    song = Songs.query.get_or_404(id)
    if form.validate_on_submit():
        review = form.review.data

        new_review = Reviews()
        new_review.review= review

        new_review.save_review()

        new_review = Reviews(review = review)

        return redirect(url_for('main.details', id = song.id))

    title="Post your review"
    return render_template('new_review.html',review_form=form, song = song)

@main.route("/review/<int:id>",methods=['GET','POST'])
@login_required
def caterers_review(id):
    form = ReviewForm()
    caterer = Caterers.query.get_or_404(id)
    if form.validate_on_submit():
        review = form.review.data

        new_review = Reviews()
        new_review.review= review

        new_review.save_review()

        new_review = Reviews(review = review)

        return redirect(url_for('main.details', id = song.id))

    title="Post your review"
    return render_template('new_review.html',review_form=form, song = song)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/review/<int:id>')
def single_review(id):
    review=Reviews.query.get(id)
    if review is None:
        abort(403)
    # format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review)

@main.route('/cars')
def cars():
    cars = Cars.query.all()
    title="car service providers"
    return render_template('cars.html',title=title, cars = cars)

@main.route("/post_cars",methods=['GET','POST'])
@login_required
def post_cars():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_cars = Cars()
        new_post_cars.location = location
        new_post_cars.company= company
        new_post_cars.service = service

        new_post_cars.save_car()

        new_car = Cars(location = location, company = company, service = service)
        reviews = Reviews.query.all()

        return redirect(url_for('main.cars'))

    title="Car service providers"
    return render_template('post.html',title = title,provider_form=form)

@main.route("/post_cars/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_cars(id):
    car = Cars.query.get_or_404(id)
   
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('main.cars')) 

@main.route('/caterers')
def caterers():
    caterers = Caterers.query.all()
    title="Catering services you can hire"
    return render_template('catering.html',title=title, caterers = caterers)
   
@main.route("/post_caterers",methods=['GET','POST'])
@login_required
def post_caterers():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_caterers = Caterers()
        new_post_caterers.location = location
        new_post_caterers.company = company
        new_post_caterers.service = service

        new_post_caterers.save_caterer()

        new_caterer = Caterers(title=title,content = content)
        reviews = Reviews.query.all()

        return redirect(url_for('main.catering'))

    title="Catering services you can hire"
    return render_template('post.html',title=title,provider_form=form)

@main.route("/post_caterers/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_caterers(id):
    caterer = Caterers.query.get_or_404(id)
   
    db.session.delete(caterer)
    db.session.commit()
    return redirect(url_for('main.caterers')) 


@main.route('/grounds')
def grounds():
    grounds = Grounds.query.all()
    title = "grounds/venues you can hire"

    return render_template('grounds.html',grounds=grounds, title=title)

@main.route("/post_grounds",methods=['GET','POST'])
@login_required
def post_grounds():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_grounds = Grounds()
        new_post_grounds.location = location
        new_post_grounds.company= company
        new_post_grounds.service = service

        new_post_grounds.save_ground()

        new_car = Grounds(location = location, company = company, service = service)
        reviews = Reviews.query.all()

        return redirect(url_for('main.grounds'))

    title="Car service providers"
    return render_template('post.html',title = title,provider_form=form)

@main.route("/post_grounds/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_grounds(id):
    ground = Grounds.query.get_or_404(id)
   
    db.session.delete(ground)
    db.session.commit()
    return redirect(url_for('main.grounds')) 

@main.route('/photography', methods=['GET','POST'])
def photography():
   photography = Photography.query.all()

   title = "Photography services"
   return render_template('photography.html', photography= photography, title=title)

@main.route("/post_photography",methods=['GET','POST'])
@login_required
def post_photography():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_photography = Photography()
        new_post_photography.location = location
        new_post_photography.company= company
        new_post_photography.service = service

        new_post_photography.save_photograph()

        new_car = Photography(location = location, company = company, service = service)
        reviews = Reviews.query.all()

        return redirect(url_for('main.photography'))

    title = "Photography services"
    return render_template('post.html',title = title,provider_form=form)

@main.route("/post_photography/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_photography(id):
    photograph = Photography.query.get_or_404(id)
   
    db.session.delete(photograph)
    db.session.commit()
    return redirect(url_for('main.photography')) 

@main.route('/tents', methods=['GET','POST'])
def tents():
    tents = Tents.query.all()

    title = "Tent providers"
    return render_template('tents.html', tents = tents,title=title)

@main.route("/post_tents",methods=['GET','POST'])
@login_required
def post_tents():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_tents = Tents()
        new_post_tents.location = location
        new_post_tents.company= company
        new_post_tents.service = service

        new_post_tents.save_tent()

        new_car = Tents(location = location, company = company, service = service)
        reviews = Reviews.query.all()

        return redirect(url_for('main.tents'))

    title = "Tents providers"
    return render_template('post.html',title = title,provider_form=form)

@main.route("/post_tents/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_tents(id):
    tent = Tents.query.get_or_404(id)
   
    db.session.delete(tent)
    db.session.commit()
    return redirect(url_for('main.tents')) 

@main.route('/details/<int:id>', methods = ['GET','POST'])
@login_required
def details(id):
    reviews = Reviews.query.all()
    song = Songs.query.get_or_404(id)
    
    return render_template('song_review.html',song = song, reviews = reviews)

@main.route('/songs')
def songs():
    songs = Songs.query.all()

    title = "Where to get Music"
    return render_template('music.html',title = title, songs = songs)

@main.route("/post_songs/",methods=['GET','POST'])
@login_required
def post_songs():
    form = ProviderForm()
    if form.validate_on_submit():
        location = form.location.data
        company = form.company.data
        service = form.service.data

        new_post_songs = Songs()
        new_post_songs.location = location
        new_post_songs.company= company
        new_post_songs.service = service

        new_post_songs.save_song()

        new_car = Songs(location = location, company = company, service = service)
        reviews = Reviews.query.all()

        return redirect(url_for('main.songs'))

    title = "Where to get Music"
    return render_template('post.html',title = title,provider_form=form)

@main.route("/post_songs/<int:id>/delete",methods=['GET','POST'])
@login_required
def delete_songs(id):
    song = Songs.query.get_or_404(id)
   
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('main.songs')) 
