from fastapi import HTTPException

from backend.app.api.repository.categories_repository import CategoriesRepository



class CategoriesService:

    @staticmethod
    def get_categories():
        try:
            categories = CategoriesRepository.get_categories()
            return  categories if categories else []
        except Exception as e:
            raise Exception(f"Error fetching categories: {str(e)}")

    @staticmethod
    def get_category_by_id(id:int):
        try:
            category = CategoriesRepository.get_category_by_id(id)
            if not category:
                raise HTTPException(status_code=404, detail="No found category")

            return category
        except Exception as e:
            raise Exception(f"Error fetching categories: {str(e)}")

    @staticmethod
    def create_category(category):
        category_new = CategoriesRepository.insert_category(category)
        if not category_new:
            HTTPException(status_code=404, detail="Failed insert new category")

        return category_new

    @staticmethod
    def update_category(category, id:int):
        update_data = CategoriesRepository.update_category(category, id)

        if not update_data:
            HTTPException(status_code=404, detail="Failed update category")

        return update_data

    @staticmethod
    def delete_category(id:int):

      delete_category = CategoriesRepository.delete_category(id)

      if not delete_category:
          raise HTTPException(status_code=404, detail="Category not found")

      return delete_category

