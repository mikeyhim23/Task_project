from flask_restful import Resource
from flask import request
from models import db, UserTask

class UserTaskResource(Resource):
    def get(self, user_task_id=None):
        if user_task_id:
            user_task = UserTask.query.get(user_task_id)
            if user_task:
                return user_task.serialize(), 200
            return {'message': 'UserTask not found'}, 404
        user_tasks = UserTask.query.all()
        return [user_task.serialize() for user_task in user_tasks], 200

    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        project_id = data['project_id']
        role = data['role']
        
        new_user_task = UserTask(user_id=user_id, project_id=project_id, role=role)
        db.session.add(new_user_task)
        db.session.commit()
        return new_user_task.serialize(), 201

    def put(self, user_task_id):
        user_task = UserTask.query.get(user_task_id)
        if not user_task:
            return {'message': 'UserTask not found'}, 404
        
        data = request.get_json()
        user_task.user_id = data.get('user_id', user_task.user_id)
        user_task.project_id = data.get('project_id', user_task.project_id)
        user_task.role = data.get('role', user_task.role)

        db.session.commit()
        return user_task.serialize(), 200

    def delete(self, user_task_id):
        user_task = UserTask.query.get(user_task_id)
        if user_task:
            db.session.delete(user_task)
            db.session.commit()
            return {'message': 'UserTask deleted'}, 200
        return {'message': 'UserTask not found'}, 404
