from fastapi import FastAPI
from Order.apis import order_app
from Product.apis import product_app
from Warehouse.apis import warehouse_app
from Supplier.apis import supplier_app

app = FastAPI()

#Include all routers
app.include_router(warehouse_app, prefix="/warehouse")
app.include_router(supplier_app, prefix="/supplier")

app.include_router(order_app, prefix="/orders")
app.include_router(product_app, prefix="/product")
