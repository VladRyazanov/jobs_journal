from requests import get, post


print(get('http://localhost:5000/api/jobs').json())
print(post("http://localhost:5000/api/jobs", json={'id': 1, 'job': "some_job", 'collaborators': "", 'end_date': '',
                                                   'start_date': '', 'is_finished': '', "work_size": '',
                                                   "team_leader_id": 1
                              }).json())

