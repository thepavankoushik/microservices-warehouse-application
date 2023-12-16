from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host='redis-17480.c323.us-east-1-2.ec2.cloud.redislabs.com',
    port=17480,
    password='VUHh2X27vfwnr3acMRKgL5iAsQb95W79',
    decode_responses=True,
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    class Meta:
        database = redis

@app.post('/product')
def create(product: Product):
    return product.save()


@app.get('/product/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.get('/products')
def all():
    return [
        format(pk)
        for pk in Product.all_pks()
    ]

def format(pk: str):
    product = Product.get(pk)
    return {
        'id': pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }

@app.delete('/product/{pk}')
def delete(pk: str):
    return Product.delete(pk)

