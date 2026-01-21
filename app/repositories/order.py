from sqlalchemy.orm import Session
from app import models, schemas


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: schemas.OrderCreate):
        db_order = models.Order(**order.model_dump())
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get_all(self):
        return self.db.query(models.Order).order_by(models.Order.created_at.desc()).all()

    def get_by_id(self, order_id: int):
        return self.db.query(models.Order).filter(models.Order.id == order_id).first()

    def update_status(self, order_id: int, new_status: str):
        order = self.get_by_id(order_id)
        if order:
            order.status = new_status
            self.db.commit()
            self.db.refresh(order)
        return order