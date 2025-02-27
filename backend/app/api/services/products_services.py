from fastapi import HTTPException

from backend.app.api.repository.products_repository import ProductRepository



class ProductService:

    @staticmethod
    def get_products():
        return ProductRepository.get_products()

    @staticmethod
    def get_product_by_id(id):
        product = ProductRepository.get_product_by_id(id)
        if not product:
            raise  HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def create_product(product):
        new_product = ProductRepository.insert_product(product)
        if new_product:
            return new_product
        raise ValueError("Failed to insert product")

    @staticmethod
    def update_product(id: int, product):
        update_product = ProductRepository.update_product(id, product)

        if not update_product:
            raise HTTPException(status_code=404, detail="Product not found")

        return update_product

    @staticmethod
    def delete_product(id:int):
        delete_product = ProductRepository.delete_product(id)

        if not delete_product:
            raise HTTPException(status_code=404, detail="Product not found")

        return delete_product

