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
        result = self.db.query(TaskModel).filter(TaskModel.category == category).all()
        return result
    
    def add_task(self, task: Task):
        new_task = TaskModel(**task.dict())
        self.db.add(new_task)
        self.db.commit()