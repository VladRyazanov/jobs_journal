from flask import jsonify, request
import flask
from data import db_session
from data.jobs import Jobs


blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route("/api/jobs")
def get_jobs():
    db_sess = db_session.create_session()
    all_jobs = db_sess.query(Jobs).all()
    return jsonify({"jobs": [item.to_dict() for item in all_jobs]})


@blueprint.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id)
    if job:
        return jsonify({"job": job.to_dict()})
    return jsonify({'error': 'Not found'})


@blueprint.route("/api/jobs", methods=["POST"])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'collaborators', 'end_date', 'start_date', 'is_finished', "work_size", "team_leader_id",
                  "team_leader"]):
        return jsonify({'error': 'Bad request'})
    json_response = request.json
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).filter(Jobs.id == json_response["id"]).first():
        return jsonify({"error": "Id already exists"})
    job = Jobs()
    job.id = json_response["id"]
    job.job = json_response["job"]
    job.collaborators = json_response["collaborators"]
    job.end_date = json_response["end_date"]
    job.start_date = json_response["start_date"]
    job.is_finished = json_response["is_finished"]
    job.work_size = json_response["work_size"]
    job.team_leader_id = json_response["team_leader_id"]
    job.team_leader = json_response["team_leader"]
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})



