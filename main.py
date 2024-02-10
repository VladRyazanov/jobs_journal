from data import db_session
from data.jobs import Jobs
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
@app.route("/index")
def index():
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False

    db_sess.add(job)
    db_sess.commit()
    all_jobs = db_sess.query(Jobs).all()
    return render_template("index.html", all_jobs=all_jobs)


if __name__ == "__main__":
    app.run()