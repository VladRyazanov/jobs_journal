from data import db_session
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template, redirect, request, abort
from forms.user import RegisterForm, LoginForm
from forms.job import AddJobForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import user_resource
from data import jobs_api
from flask_restful import Api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/data.db")
api = Api(app)
api.add_resource(user_resource.UserListResource, '/api/v2/users')
api.add_resource(user_resource.UserResource, '/api/v2/news/<int:users_id>')


app.register_blueprint(jobs_api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    all_jobs = db_sess.query(Jobs).all()
    return render_template("index.html", all_jobs=all_jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/add_job", methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
                   job=form.job.data,
                   work_size=form.work_size.data,
                   collaborators=form.collaborators.data,
                   start_date=form.start_date.data,
                   end_date=form.end_date.data,
                   is_finished=form.is_finished.data
                   )
        job.team_leader = db_sess.query(User).filter(User.id == form.team_leader.data).first()
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template("add_job.html", form=form)


@app.route("/edit_job/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job and (job.team_leader == current_user or current_user.id == 1):
            form.team_leader.data = job.team_leader.id
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.start_date.data = job.start_date
            form.end_date.data = job.end_date
            form.is_finished.data = job.is_finished
            return render_template("add_job.html", form=form)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job is not None and job.team_leader == current_user or current_user.id == 1:
            job.team_leader = db_sess.query(User).filter(User.id == form.team_leader.data).first()
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect("/")

    abort(404)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run()