# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask import request, jsonify
from app.lib.config import contract_address, helper_abi, public_to_private_keys, url
from app.controller.machines import mounted_machine, Machine
config_blueprint = Blueprint(name="config_blueprint", import_name=__name__, url_prefix="/apus_network/config/")


@config_blueprint.route("/", methods=['GET'])
def mount_client():
    # dict(code=200, data=dict(contract_address=contract_address, abi=helper_abi, public_to_private_keys=public_to_private_keys))
    return jsonify(dict(code=200, data=dict(contract_address=contract_address, abi=helper_abi, public_to_private_keys=public_to_private_keys, rpc_url=url)))