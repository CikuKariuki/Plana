from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,ProviderForm
from .. models import Reviews,User,Providers
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

@main.route('/user/<int:user_id>')
def user(user_id):
    '''
    view function that returns the users details page and its data
    '''
    return render_template('providers.html', id = user_id)   

@main.route("/post",methods=['GET','POST'])
@login_required
def post():
    form = ProviderForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_post = Providers()
        new_post.title = title
        new_post.content= content

        new_post.save_provider()

        new_provider = Providers(title=title,content = content)
        reviews = Reviews.query.all()

        return redirect(url_for('main.index'))

    title="Post your provider"
    return render_template('post.html',title=title,provider_form=form)

@main.route("/review/<int:id>",methods=['GET','POST'])
@login_required
def review(id):
    form = ReviewForm()
    # provider = Provider.query.get_or_404(id)
    if form.validate_on_submit():
        review = form.review.data

        new_review = Reviews()
        new_review.review= review

        new_review.save_review()

        new_review = Reviews(review = review)

        return redirect(url_for('main.index',id = provider.id))

    title="Post your review"
    return render_template('new_review.html',review_form=form)


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
        abort(404)
    # format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review)

@main.route('/tents')
def tents():
    return render_template('tents.html')


@main.route('/grounds')
def grounds():
    return render_template('grounds.html')

@main.route('/cars')
def cars():
    return render_template('cars.html')

@main.route('/catering', methods=['GET','POST'])
def Catering(category = "Catering"):

   catering = Catering.query.all()

   title = "Catering"
   return render_template('catering.html', catering= catering, title=title)

@main.route('/photography', methods=['GET','POST'])
def photography(category = "Photography"):

   photography = Photography.query.all()

   title = "Photography"
   return render_template('photography.html', photography= photography, title=title)

@main.route('/music')
def music():
    return render_template('music.html')


