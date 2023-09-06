# -*- coding:utf-8 -*-

from flask import request, jsonify
from flask.blueprints import Blueprint
from app.lib.contract_lib import contract_helper
from app.controller.machines import mounted_machine, Machine
machine_blueprint = Blueprint(name="machine_blueprint", import_name=__name__, url_prefix="/apus_network/server/")


@machine_blueprint.route("/info", methods=['GET'])
def get_mount_server():
    machine_id = request.args.get("machine_id")
    address = request.args.get("address")
    try:
        machine = mounted_machine.get(address, machine_id)
    except Exception as e:
        return jsonify(dict(code=400, msg=str(e)))
    return jsonify(dict(code=200, data=dict(server_info=machine.contract_server_info)))


@machine_blueprint.route("/provider/list")
def list_server():
    # offset = int(request.args.get("offset"))
    # limit = int(request.args.get("limit"))
    address = request.args.get("address")
    d_machines = mounted_machine.list(address)

    try:
        c_machines = contract_helper.list_own_devices(type("owner", (), dict(public_key=address)), 100, 0)
        c_machines = {machine.machine_id: machine for machine in c_machines}
    except Exception as e:
        return jsonify(dict(code=400, msg="contract rpc:listOwnMachine err"))

    # merge online & created address
    result = []
    for machine_id, machine in d_machines.items():
        if machine_id not in c_machines:
            result.append(machine)

    for machine in c_machines.values():
        result.append(machine)

    result = [item.data for item in result]
    return jsonify(dict(code=200, data=result))


@machine_blueprint.route("/market/list")
def list_market_server():
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    try:
        c_machines = contract_helper.list_devices(limit, offset)
        result = [item.data for item in c_machines]
    except Exception as e:
        return jsonify(dict(code=400, msg="contract rpc:listMachine err"))
    return jsonify(dict(code=200, data=result))