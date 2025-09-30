from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.Record_model import Record_Model
from schemas.record_schema import Record_Schema
import time

record_bp = Blueprint('record_bp', __name__,url_prefix='/record')
record_schema = Record_Schema()

@record_bp.route('/create', methods=['POST'])
def create_record():
    try:
        record_data = record_schema.load(request.json)
    except ValidationError as err:
        return jsonify("error", err.messages), 400

    timestamp_ms = int(time.time() * 1000)
    record_data['timestamp'] = timestamp_ms

    Record_Model.create_record(record_data)
    return jsonify({"message": "Record created successfully", "timestamp": timestamp_ms}), 201


@record_bp.route('/latest', methods=['GET'])
def get_latest_data():
    """
    Endpoint สำหรับให้ React Dashboard ดึงข้อมูลล่าสุดและประวัติ
    """
    try:
        # --------------------------------------------------
        # *** แก้ไขแล้ว ***: เรียกใช้ Model เพื่อดึงข้อมูลย้อนหลัง 20 รายการ
        # --------------------------------------------------
        # ดึงข้อมูลย้อนหลัง 20 รายการจาก MongoDB
        history_data = Record_Model.get_history_data(limit=20)

        latest_data = history_data[-1] if history_data else None

        # ส่งข้อมูลล่าสุดและประวัติกลับไป
        return jsonify({
            "latestData": latest_data,
            "history": history_data
        }), 200

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch data from model/DB"}), 500


# Endpoint สุขภาพ (Health Check)
@record_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "OK", "service": "Flask IoT API"}), 200
