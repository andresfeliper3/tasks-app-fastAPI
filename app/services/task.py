from models.task import Task as TaskModel
from schemas.task import Task


class TaskService():

    def __init__(self, db) -> None:
        self.db = db

    def get_tasks(self):
        result = self.db.query(TaskModel).all()
        return result

    def get_task_by_id(self, id):
        result = self.db.query(TaskModel).filter(TaskModel.id == id).first()
        return result

    def get_tasks_by_category(self, category):
        result = self.db.query(TaskModel).filter(
            TaskModel.category == category).all()
        return result

    def add_task(self, task: Task):
        new_task = TaskModel(**task.dict())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)  # Actualizar el objeto cargado desde la base de datos
        return new_task 

    def update_task(self, id: int, updated_task: Task):
        old_task =  self.db.query(TaskModel).filter(TaskModel.id == id)

        if old_task.scalar():
            data = updated_task.dict()
            data['id'] = id
            old_task.update(data)
            self.db.commit()
            return

    def delete_task(self, id):
        self.db.query(TaskModel).filter(TaskModel.id == id).delete()
        self.db.commit()
        return
