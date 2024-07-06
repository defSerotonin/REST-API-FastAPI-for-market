from fastapi import FastAPI, Response, status
from pydantic import BaseModel, parse_file_as
import os
import json
import glob
import datetime

app = FastAPI()



activities_folder = "activities"


class Activity(BaseModel):
    id: int
    name: str
    date: datetime.datetime

def find_activity(activity_id=0):
    return glob.glob(os.path.join(activities_folder, f'*{activity_id if activity_id else ""}.json'))


@app.get('/activity/get/all')
def get_activity():
    res = []
    files = find_activity()
    if files:
        for file in files:
            res.append(parse_file_as(Activity, file))
    return res


@app.get('/activity/add/{activity_id}')
def get_activity(activity_id:int, response:Response):
    files = find_activity(activity_id)
    if files:
        return parse_file_as(Activity, files[0])
    response.status_code = status.HTTP_404_NOT_FOUND
    return {}



@app.post('/activity/add/{activity_id}')
def add_activity(activity_id:int, activity:Activity, response:Response):
    file = find_activity(activity_id)
    if file:
        response.status_code = status.HTTP_302_FOUND
        return False
    else:
        with open(os.path.join(activities_folder, f'activity_{activity_id}.json'), 'w') as f:
            f.write(activity.json())
    return activity_id

@app.put('/activity/update/{activity_id}')
def update_activity(activity_id:int, activity:Activity, response:Response):
    file = find_activity(activity_id)
    if file:
        act = parse_file_as(Activity, file[0])
        act.name = activity.name
        act.date = activity.date
        with open(os.path.join(activities_folder, f'activity_{activity_id}.json'), 'w') as f:
            f.write(activity.json())
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False


@app.delete('/activity/delete/{activity_id}')
def delete_activity(activity_id:int, response:Response):
    file = find_activity(activity_id)
    if file:
        os.remove(file[0])
        return True
    response.status_code = status.HTTP_404_NOT_FOUND
    return False
