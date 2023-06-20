import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers.task import task_router  # Importa el enrutador task_router

app = FastAPI()
app.include_router(task_router)  # Incluye el enrutador task_router en la aplicación

client = TestClient(app)


class TestTaskRouter(unittest.TestCase):

    def setUp(self):
        # Insert an example category record before each test
        task_data = {
            "title": "Example task",
            "year": 2022,
            "content": "Example content",
            "category_id": 1
        }
        response = client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 201)
        self.task_id = response.json()["id"] # Get the ID of the inserted record

    def tearDown(self):
        # Delete the category record after each test
        response = client.delete(f"/task/{self.task_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_tasks(self):
        response = client.get("/task")
        self.assertEqual(response.status_code, 200)
 

    def test_get_task_by_id(self):
        response = client.get(f"/task/{self.task_id}")
        self.assertEqual(response.status_code, 200)
     

    def test_get_tasks_by_category(self):
        response = client.get("/task/?category=Default")
        self.assertEqual(response.status_code, 200)
      
    def test_add_task(self):
        task_data = {
            "title": "My task testing",
            "year": 2023,
            "content": "Content testing",
            "category_id": 1
        }
        response = client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 201)
        
    def test_update_task(self):
        task_data = {
            "category_id": 1,
            "title": "My testing updated task",
            "content": "Content of my testing updated task",
            "year": 2023
        }
        response = client.put(f"/task/{self.task_id}", json=task_data)
        self.assertEqual(response.status_code, 200)
      
    def test_add_task_no_title(self):
        task_data = {
            "year": 2023,
            "content": "Content testing",
            "category_id": 1
        }
        response = client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 422)

    def test_add_task_invalid_year(self):
        task_data = {
            "title": "My task testing",
            "year": "invalid_year",
            "content": "Content testing",
            "category_id": 1
        }
        response = client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 422)

    def test_add_task_invalid_category(self):
        task_data = {
            "title": "My task testing",
            "year": 2023,
            "content": "Content testing",
            "category_id": "category"
        }
        response = client.post("/task", json=task_data)
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
