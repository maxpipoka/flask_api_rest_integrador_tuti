from datetime import datetime

from flask import Response, Blueprint, request, jsonify

from ..models.models import Attendance, db

bp= Blueprint('asistencias', __name__)

# Definicion endpoint 