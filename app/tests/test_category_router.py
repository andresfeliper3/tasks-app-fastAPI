import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers.category import category_router  # Import the category router

app = FastAPI()
app.include_router(category_router)  # Include the category router in the app

client = TestClient(app)


class TestCategoryRouter(unittest.TestCase):

    def setUp(self):
        # Insert an example category record before each test
        category_data = {
            "name": "Example category",
            "description": "Example description"
        }
        response = client.post("/category", json=category_data)
        self.assertEqual(response.status_code, 201)
        self.category_id = response.json()["id"]  # Get the ID of the inserted record

    def tearDown(self):
        # Delete the category record after each test
        response = client.delete(f"/category/{self.category_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        response = client.get("/category")
        self.assertEqual(response.status_code, 200)
    

    def test_get_category_by_id(self):
        response = client.get(f"/category/{self.category_id}")
        self.assertEqual(response.status_code, 200)
       

    def test_add_category(self):
        category_data = {
            "name": "My category",
            "description": "Category description"
        }
        response = client.post("/category", json=category_data)
        self.assertEqual(response.status_code, 201)
       
    def test_update_category(self):
        category_data = {
            "name": "Updated category",
            "description": "Updated description"
        }
        response = client.put(f"/category/{self.category_id}", json=category_data)
        self.assertEqual(response.status_code, 200)
       

    def test_add_category_no_name(self):
        category_data = {
            "description": "Category description"
        }
        response = client.post("/category", json=category_data)
        self.assertEqual(response.status_code, 422)

   


if __name__ == "__main__":
    unittest.main()
