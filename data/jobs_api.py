from flask import jsonify, request
import flask
from data import db_session
from data.jobs import Jobs
from data.users import User

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route("/api/jobs")
def get_jobs():
    db_sess = db_session.create_session()
    all_jobs = db_sess.query(Jobs).all()
    return jsonify({"jobs": [item.to_dict(only=['job', 'collaborators', 'end_date', 'start_date',
                                                'is_finished', "work_size", "user_id"]) for item in all_jobs]})


@blueprint.route("/api/jobs/<int:job_id>", methods=["GET"])
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
                 ['job', 'collaborators', 'end_date', 'start_date', 'is_finished', "work_size", "user_id"]):
        return jsonify({'error': 'Bad request'})
    json_response = request.json
    db_sess = db_session.create_session()
    teamleader = db_sess.query(User).filter(User.id == json_response["teamleader_id"]).first()
    if not teamleader:
        return jsonify({'error': 'User not found'})
    job = Jobs()
    job.job = json_response["job"]
    job.collaborators = json_response["collaborators"]
    job.end_date = json_response["end_date"]
    job.start_date = json_response["start_date"]
    job.is_finished = json_response["is_finished"]
    job.work_size = json_response["work_size"]
    job.user_id = json_response["teamleader_id"]
    job.team_leader = teamleader
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Job not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    json_response = request.json
    if not json_response:
        return jsonify({'error': 'Empty request'})
    elif not all(map(lambda key: key in ['job', 'collaborators',
                                         'end_date', 'start_date',
                                         'is_finished', "work_size",
                                         "teamleader_id"], json_response)):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Job not found'})
    for key in json_response:
        if hasattr(jobs, key):
            setattr(jobs, key, json_response[key])
    db_sess.commit()
    return jsonify({'success': 'OK'})





