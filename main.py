from fastapi import FastAPI, Response, status
from pydantic import BaseModel, parse_file_as
import os
import json
import glob
import datetime

app = FastAPI()

json_folder = "Json_f"

class UserRegister(BaseModel):
    user_id: int
    user_name: str
    user_surname: str
    user_city: str
    user_mail: str
    user_date: datetime.datetime

class UserBlog(BaseModel):
    user_message: str
    user_message_datetime: datetime.datetime

def find_json(json_user_id=0):
    return glob.glob(os.path.join(json_folder, f'*{json_user_id if json_user_id else ""}.json'))

@app.get('/users/get/all')
def get_users_list():
    res = []
    files = find_json()
    if files:
        for file in files:
            res.append(parse_file_as(UserRegister, file))
    return res

@app.get('/users/add/{json_user_id}')
def get_users_json(json_user_id:int, response:Response):
    files = find_json(json_user_id)
    if files:
        return parse_file_as(UserRegister, files[0])
    response.status_code = status.HTTP_404_NOT_FOUND
    return {}

@app.post('/users/post/{json_user_id}')
def add_user(json_user_id:int, user:UserRegister, response:Response):
    file = find_json(json_user_id)
    if file:
        response.status_code = status.HTTP_302_FOUND
        return False
    else:
        with open(os.path.join(json_folder, f'user_{json_user_id}.json'), 'w') as f:
            f.write(user.json())
    return json_user_id

@app.put('/users/update/{json_user_id}')
def update_user(json_user_id:int, user:UserRegister, response:Response):
    file = find_json(json_user_id)
    if file:
        act = parse_file_as(UserRegister, file[0])
        act.user_name = user.user_name
        act.user_surname = user.user_surname
        act.user_city = user.user_city
        act.user_mail = user.user_mail
        act.user_date = user.user_date
        with open(os.path.join(json_folder, f'user_{json_user_id}.json'), 'w') as f:
            f.write(user.json())
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False

@app.delete('/users/delete/{json_user_id}')
def delete_user_data(json_user_id:int, response:Response):
    file = find_json(json_user_id)
    if file:
        os.remove(file[0])
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False
