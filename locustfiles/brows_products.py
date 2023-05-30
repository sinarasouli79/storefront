from random import randint

from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

    @task(2)
    def view_products(self):
        collection_id = randint(3, 6)
        self.client.get(f'/store/products/?collection={collection_id}', name='/store/products/')

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f'/store/products/{product_id}', name='/store/products/:id/')

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(f'/store/carts/{self.cart_id}/items/', name='/store/carts/items/',
                         json={"product": product_id, "quantity": 1})
