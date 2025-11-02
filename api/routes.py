
from flask import Blueprint, request, jsonify, abort
from extensions import db
from models.workflow import Workflow           
from datetime import datetime
import json
from utils.parser import parse_prompt_to_workflow

api_bp = Blueprint("api", __name__)

@api_bp.route('/workflows/from-prompt', methods=['POST'])
def create_from_prompt():
    data = request.get_json(force=True) or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        abort(400, "Prompt is required")

    workflow = parse_prompt_to_workflow(prompt)
    row = Workflow(
        id=workflow['workflow_id'],
        title=workflow['title'],
        version=workflow['version'],
        json=json.dumps(workflow),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(row)
    db.session.commit()
    return jsonify(workflow), 201

@api_bp.route('/workflows/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    row = Workflow.query.filter_by(id=workflow_id).first()
    if not row:
        abort(404, "Workflow not found")
    return jsonify(json.loads(row.json))

@api_bp.route('/workflows/<workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    payload = request.get_json(force=True)
    row = Workflow.query.filter_by(id=workflow_id).first()
    if not row:
        abort(404, "Workflow not found")
    row.json = json.dumps(payload)
    row.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(payload)
