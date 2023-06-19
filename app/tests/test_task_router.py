import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers.task import task_router  # Importa el enrutador task_router


app = FastAPI()
# Incluye el enrutador task_router en la aplicación
app.include_router(task_router)

client = TestClient(app)


class TestTaskRouter(unittest.TestCase):
    
    def setUp(self):
        # Insertar un registro de tarea de ejemplo antes de cada prueba
        task_data = {
            "title": "Example task",
            "year": 2022,
            "content": "Example content",
            "category": "Default"
        }
        response = client.post("/tasks", json=task_data)
        self.assertEqual(response.status_code, 201)
        self.task_id = response.json()["id"]  # Obtener el ID del registro insertado

    def tearDown(self):
        # Eliminar el registro de tarea después de cada prueba
        response = client.delete(f"/tasks/{self.task_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_tasks(self):
        response = client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        # Aquí puedes verificar si el contenido de la respuesta es el esperado

    def test_get_task_by_id(self):
        response = client.get(f"/tasks/{self.task_id}")
        self.assertEqual(response.status_code, 200)
        # Aquí puedes verificar si el contenido de la respuesta es el esperado

    def test_get_tasks_by_category(self):
        response = client.get("/tasks/?category=Default")
        self.assertEqual(response.status_code, 200)
        # Aquí puedes verificar si el contenido de la respuesta es el esperado

    def test_add_task(self):
        task_data = {
            "title": "My task testing",
            "year": 2023,
            "content": "Content testing",
            "category": "Default"
        }
        response = client.post("/tasks", json=task_data)
        self.assertEqual(response.status_code, 201)
        # Aquí puedes verificar si el contenido de la respuesta es el esperado

    def test_update_task(self):
        task_data = {
            "category": "New default",
            "title": "My testing updated task",
            "content": "Content of my testing updated task",
            "year": 2023
        }
        response = client.put(f"/tasks/{self.task_id}", json=task_data)
        self.assertEqual(response.status_code, 200)
        # Aquí puedes verificar si el contenido de la respuesta es el esperado
        
    def test_add_task_no_title(self):
        task_data = {
            "year": 2023,
            "content": "Content testing",
            "category": "Default"
        }
        response = client.post("/tasks", json=task_data)
        self.assertEqual(response.status_code, 422)
        
    def test_add_task_invalid_year(self):
        task_data = {
            "title": "My task testing",
            "year": "invalid_year",
            "content": "Content testing",
            "category": "Default"
        }
        response = client.post("/tasks", json=task_data)
        self.assertEqual(response.status_code, 422)
        
    # def test_add_task_invalid_category(self):
    #     task_data = {
    #         "title": "My task testing",
    #         "year": 2023,
    #         "content": "Content testing",
    #         "category": 123
    #     }
    #     response = client.post("/tasks", json=task_data)
    #     self.assertEqual(response.status_code, 422)




if __name__ == "__main__":
    unittest.main()
