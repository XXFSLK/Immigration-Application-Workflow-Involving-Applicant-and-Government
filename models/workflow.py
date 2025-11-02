from extensions import db
import uuid
from sqlalchemy.dialects.mysql import JSON
from datetime import datetime

class Workflow(db.Model):
    __tablename__ = 'workflows'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255))
    version = db.Column(db.Integer, default=1)
    json = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    steps = db.relationship('Step', backref='workflow', lazy=True)

class Step(db.Model):
    __tablename__ = 'workflow_steps'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = db.Column(db.String(36), db.ForeignKey('workflows.id'), nullable=False)
    name = db.Column(db.String(255))
    order = db.Column(db.Integer)
    role = db.Column(db.String(100))
    inputs = db.Column(JSON)
    actions = db.Column(JSON)
