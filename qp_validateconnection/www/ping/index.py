import frappe
import socket
import json
from datetime import datetime
from qp_validateconnection.services.validate_status import ping
def get_context(context):

    context.server_list = frappe.get_list("qp_vc_Server", filters = {"status": "ON"},fields = ["*"])

    context.setup = frappe.get_doc("qp_vc_Setup")

    context.list_valid = len(context.server_list)
    

@frappe.whitelist()
def search_ping(server_list = []):

    UP = "UP"
    DOWN = "DOWN"

    server_list = frappe.get_list("qp_vc_Server", filters = {"status": "ON"},fields = ["name", "url"])


    for server in server_list:
        
        respuesta = UP if ping(server.get("url")) == 200 else DOWN
        
        server.update({"ping": respuesta})

        server.update({"ping_refresh": datetime.now().strftime('%d-%m-%Y %H:%M:%S') })

    return server_list
    