from fastapi import FastAPI, Depends, HTTPException, status, Query  # Adicionei Query aqui
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, database

# Create database tables (isso roda ao importar, mas movi para uma função para controle)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Fake Store Backend API",
    description="API para gerenciar compras da Fake Store.",
    version="1.0.0"
)

# Configuração de CORS (corrigida e expandida para Docker/local)
origins = [
    "http://localhost",
    "http://localhost:80",      # Para acessar via browser (Docker)
    "http://frontend:80",       # Nome do serviço no Docker Compose (rede interna)
    "http://localhost:5173",    # Porta dev local (Vite)
    "http://localhost:3000",    # Porta alternativa para React/CRA
    "*"                         # Para testes rápidos (remova em produção por segurança)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Rotas REST ---

# 1. POST: Criar uma nova compra
@app.post("/purchases/", response_model=schemas.PurchaseSchema, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    if not purchase.items:
        raise HTTPException(status_code=400, detail="Purchase must contain at least one item.")

    total_amount = sum(item.product_price * item.quantity for item in purchase.items)

    db_purchase = models.Purchase(total_amount=total_amount)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    for item_data in purchase.items:
        db_item = models.PurchaseItem(
            purchase_id=db_purchase.id,
            product_id=item_data.product_id,
            product_name=item_data.product_name,
            product_price=item_data.product_price,
            quantity=item_data.quantity
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_purchase)  # Refresh to load the items relationship

    return db_purchase

# 2. GET: Listar todas as compras
@app.get("/purchases/", response_model=List[schemas.PurchaseSchema])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = db.query(models.Purchase).offset(skip).limit(limit).all()
    return purchases

# 3. GET: Obter detalhes de uma compra específica
@app.get("/purchases/{purchase_id}", response_model=schemas.PurchaseSchema)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

# 4. DELETE: Cancelar (excluir) uma compra
@app.delete("/purchases/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")

    # Delete associated items first
    db.query(models.PurchaseItem).filter(models.PurchaseItem.purchase_id == purchase_id).delete()
    db.delete(db_purchase)
    db.commit()
    # Não retorne body para 204 (FastAPI lida com isso)

# 5. PUT: Atualizar a quantidade de um item em uma compra
@app.put("/purchases/{purchase_id}/items/{item_id}", response_model=schemas.PurchaseSchema)
def update_purchase_item_quantity(
    purchase_id: int,
    item_id: int,
    new_quantity: int = Query(..., ge=1, description="Nova quantidade do item (deve ser >= 1)"),  # Lê do query param
    db: Session = Depends(get_db)
):
    # Validação já feita pelo Query (ge=1 para >=1)
    # Mas reforçando:
    if new_quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db_item = db.query(models.PurchaseItem).filter(
        models.PurchaseItem.id == item_id,
        models.PurchaseItem.purchase_id == purchase_id
    ).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Purchase item not found in this purchase")

    old_item_total = db_item.product_price * db_item.quantity
    new_item_total = db_item.product_price * new_quantity

    db_item.quantity = new_quantity
    db_purchase.total_amount = db_purchase.total_amount - old_item_total + new_item_total

    db.add(db_item)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_item)
    db.refresh(db_purchase)
    return db_purchase
