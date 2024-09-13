from flask import Blueprint,url_for,redirect,render_template,request
from models import Article

blog = Blueprint("blog", __name__)

@blog.route("/")
def home():
    return render_template("blog/home.html")


@blog.route("/about")
def about():    
    return render_template("blog/about.html")

@blog.route("/portfolio")
def portfolio():    
    return render_template("blog/portfolio.html")

@blog.route("/contact", methods = ["POST", "GET"])
def contact():    
    return render_template("blog/contact.html")

@blog.route("/publications")
def publications():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of articles per page
    
    # Use paginate method with keyword arguments
    pagination = Article.query.order_by(Article.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template("blog/publications.html", articles=pagination.items, pagination=pagination)

@blog.route("/article/<int:aid>")
def article(aid):
    article = Article.query.get_or_404(aid)
    return render_template("blog/article.html", article=article)

