import os
from flask import Blueprint, url_for, redirect,render_template,request,session, flash,current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import bcrypt,db,login_manager
from models import User,Article



admin = Blueprint('admin', __name__)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/images'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Register Admin Route
@admin.route("/admin_register", methods = ["GET", "POST"])
def admin_register():
    if request.method=="GET":
        return render_template("admin/register.html")
    elif request.method == "POST":        
        username = request.form['username']
        password = request.form['password']
        password_hash =bcrypt.generate_password_hash(password).decode('utf-8')
        
        admin = User(username =username, password= password_hash)
        db.session.add(admin)
        db.session.commit()
        
        return redirect(url_for("admin.login"))

    
# Admin Login
@admin.route("/login", methods = ["GET", "POST"])
@admin.route("/", methods = ["GET", "POST"])
def login(): 
    if request.method=="GET":
        return render_template("admin/login.html")
    elif request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()     
        
        if user and bcrypt.check_password_hash(user.password, password):
            flash("Login Successful")
            session["uid"] = user.uid
            return redirect(url_for("admin.dashboard"))
        else:
            flash('Wrong Username or Password. Please, try again....')
            return render_template("admin/login.html")
  
      
# Article Creation Route
@admin.route("/create_article", methods = ["GET", "POST"])
def create_article():
    if request.method == "GET":
        return render_template("admin/create_article.html")
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # Handle image upload
        image_file = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
                image_file = image_filename

        article = Article(title=title, content=content, image_file=image_file)
        db.session.add(article)
        db.session.commit()
        flash('Article created successfully!', 'success')
        return redirect(url_for("admin.dashboard"))


#Article Editing Route
@admin.route("/edit_article/<int:aid>", methods=['GET', 'POST'])
def edit_article(aid):
    article = Article.query.get_or_404(aid)
    
    if request.method == "POST":
        # Update the title and content
        title = request.form['title']
        content = request.form['content']
        
        article.title = title
        article.content = content
        
        # Handle image upload if a new image is provided
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '' and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
                article.image_file = image_filename  # Update image in the article

        # Save the changes to the database
        db.session.commit()
        flash('Article updated successfully', 'success')
        return redirect(url_for('admin.dashboard'))

    # Render the edit article page
    return render_template('admin/edit_article.html', article=article)

# View Article
@admin.route("/view_article/<int:aid>")
def view_article(aid):
    if "uid" not in session:
        flash("You need to log in first.")
        return redirect(url_for("admin.login"))
    
    article = Article.query.get_or_404(aid)
    return render_template('admin/view_article.html', article=article)

# Delete an article
@admin.route("/delete_article/<int:aid>", methods=["POST"])
def delete_article(aid):
    if "uid" not in session:
        flash("You need to log in first.")
        return redirect(url_for("admin.login"))

    article = Article.query.get_or_404(aid)  # Get the article or return 404 if not found
    
    db.session.delete(article)  # Delete the article from the database
    db.session.commit()  # Save changes to the database

    flash('Article deleted successfully', 'success')
    return redirect(url_for("admin.dashboard"))



# dashbord route
@admin.route("/dashboard")
def dashboard():
    if "uid" not in session:
        flash("You need to log in first.")
        return redirect(url_for("admin.login"))
    
    articles = Article.query.order_by(Article.aid.desc()).all()
    return render_template("admin/dashboard.html", articles = articles,)

@login_manager.user_loader
def load_user(uid):
        return User.get(uid)
# Logout
@admin.route("/logout", methods=["POST"])
def logout():
    session.pop('uid',None)
    return redirect(url_for("admin.login"))
     