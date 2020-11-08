import uuid
from app import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.String, primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), nullable=True)
    description = db.Column(db.String(2048), nullable=True)
    amount = db.Column(db.Integer(), nullable=False)
    paid = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Payment {id}>'.format(id=self.id)
