from requests import get, post, delete, put

# Корректный запрос, ответ сервера - {'success': 'OK'}
print(post('http://localhost:5000/api/jobs', json={
    'job': "Что-то сделать",
    'collaborators': "1, 2",
    'end_date': None,
    'start_date': None,
    'is_finished': False,
    "work_size": 150,
    "teamleader_id": 1
    }).json())

# Проверка, добавилась ли новая работа
print(get("http://localhost:5000/api/jobs").json())

# Запрос, не содержащий всех необходимых полей. Ответ сервера - {'error': 'Bad request'}
print(post('http://localhost:5000/api/jobs', json={"work_size": 1}).json())

# Запрос с несуществующим id пользователя (teamleader_id). Ответ сервера - {'error': 'User not found'}
print(post('http://localhost:5000/api/jobs', json={
    'job': "Что-то сделать",
    'collaborators': "1, 2",
    'end_date': None,
    'start_date': None,
    'is_finished': False,
    "work_size": 150,
    "teamleader_id": 999}).json())

# Получение всех работ
print(get("http://localhost:5000/api/jobs").json())

# Изменение работы - правильный запрос
print(put("http://localhost:5000/api/jobs/1", json={"job": "Измененная работа"}).json())

# Проверка
print(get("http://localhost:5000/api/jobs").json())

# Запрос с несуществующим id работы. Ответ - {'error': 'Job not found'}
print(put("http://localhost:5000/api/jobs/999", json={"job": "Измененная работа"}).json())

# Пустой запрос. Ответ сервера - {'error': 'Empty request'}
print(put('http://localhost:5000/api/jobs/999', json={}).json())

# Запрос с несуществующими ключами. Ответ сервера - {'error': 'Bad request'}
print(put("http://localhost:5000/api/jobs/999", json={"not_job": "Измененная работа"}).json())


