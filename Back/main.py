from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from clases.Item import Item

# Creacion de la API
app = FastAPI(
    title="Smart Trade",
    description="This is a web app made for PSW-DDS proyect on UPV."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Las URLs del frontend que necesitan acceso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creacion de un catalogo con 3 items
catalog = {
    0: Item(name='PlayStation 5', description="La mejor consola", price=599.99, provider_name="Sony"),
    1: Item(name="Harry Potter y la piedra filosofal", description="Libro bueno", price= 12.50, provider_name="Editorial 123"),
    2: Item(name="MANZANA", description="La mejor del mercado", price= 2.3, provider_name="De ecuador")
}

# Endpoints
@app.get("/")
def index():
    return "Hi, welcome to Smart Trade" 

@app.get("/items/all/")
def get_all_items():
    return catalog

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    if (item_id not in catalog):
        raise HTTPException(
            status_code=404, 
            detail=f"El id '{item_id}', no existe en la base de datos."
        )
    return catalog[item_id]

@app.post("/items/")
def post_item(item: Item = Body(...)):
    item_id = len(catalog)
    catalog[item_id] = item
    return catalog

@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int):
    if item_id not in catalog:
        raise HTTPException(status_code=404, detail="No existe un producto con ese nombre")
    del catalog[item_id]
    return catalog

@app.put("/items/{item_id}")
def update_item_by_id(item_id:int, item: Item = Body(...)):
    if item_id not in catalog:
        raise HTTPException(status_code=404, detail="No existe un producto con ese nombre")
    catalog[item_id] = item
    return catalog