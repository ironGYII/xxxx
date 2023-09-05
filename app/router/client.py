# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask import request, jsonify
from app.controller.machines import mounted_machine, Machine
client_blueprint = Blueprint(name="client_blueprint", import_name=__name__, url_prefix="/apus_network/client/")


@client_blueprint.route("/mount", methods=['POST'])
def mount_client():
    client_info = request.get_json()
    mounted_machine.add(Machine(pub_key=client_info.get("pub_key"), ip=client_info.get("ip"), container_name=client_info.get("container_name"), info=client_info.get("info")))
    return jsonify(pub_key=client_info.get("pub_key"), ip=client_info.get("ip"), container_name=client_info.get("container_name"), info=client_info.get("info"))

