from flask import render_template, request, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home(): 
    page = request.args.get('page', 1, type=int) #istenilen sayfayi almak...type page number oluy yani birisi int den baska birsey girerese error.1 = default first page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  #database den tum postlari al... page=page ile secilen page i query e  pass ediyoruk
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template("about.html", title="Hakkında")
