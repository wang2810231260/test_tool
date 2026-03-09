from flask import Blueprint, json
from common.id_utils import CBUUtil, CUITUtil

data_bp = Blueprint('data', __name__)

@data_bp.route('/generate_cuit', methods=['GET'])
def generate_cuit():
    cuit = CUITUtil.generate_cuit()
    return json.dumps({"cuit": cuit})

@data_bp.route('/generate_cbu', methods=['GET'])
def generate_cbu():
    cbu = CBUUtil.generate_cbu()
    return json.dumps({"cbu": cbu})
