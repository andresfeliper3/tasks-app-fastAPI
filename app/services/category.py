from models.task import Category as CategoryModel
from schemas.category import Category


class CategoryService:

    def __init__(self, db):
        self.db = db

    def get_categories(self):
        result = self.db.query(CategoryModel).all()
        return result

    def get_category_by_id(self, id):
        result = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        return result

    def get_category_by_title(self, title):
        result = self.db.query(CategoryModel).filter(CategoryModel.title == title).first()
        return result

    def create_category(self, category: Category):
        new_category = CategoryModel(**category.dict())
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def update_category(self, id: int, updated_category: Category):
        old_category = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        if old_category:
            data = updated_category.dict()
            data['id'] = id
            for key, value in data.items():
                setattr(old_category, key, value)
            self.db.commit()
            return old_category

    def delete_category(self, id):
        deleted_category = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        if deleted_category:
            self.db.delete(deleted_category)
            self.db.commit()
        return deleted_category

    def delete_all_categories(self):
        deleted_count = self.db.query(CategoryModel).delete()
        self.db.commit()
        return deleted_count
