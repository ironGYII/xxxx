# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask import request, jsonify
from app.controller.machines import mounted_machine, Machine
from app.lib.contract_lib import contract_helper

account_blueprint = Blueprint(name="account", import_name=__name__, url_prefix="/apus/account/")



@account_blueprint.route("/info", methods=['GET'])
def mount_client():

    user_address = request.args.get("address")
    info = contract_helper.get_account_info(addr=user_address)

    return jsonify(dict(code=200, data=dict(address=user_address)))

