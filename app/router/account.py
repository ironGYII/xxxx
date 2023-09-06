# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask import request, jsonify
from app.controller.machines import mounted_machine, Machine
from app.lib.contract_lib import contract_helper

account_blueprint = Blueprint(name="account", import_name=__name__, url_prefix="/apus/account/")


@account_blueprint.route("/info", methods=['GET'])
def mount_client():
    user_address = request.args.get("address")
    try:
        info = contract_helper.get_account_info(pub_key=user_address)
    except Exception as e:
        return jsonify(dict(code=400, msg=str(e)))
    return jsonify(dict(code=200, data=info.info))




