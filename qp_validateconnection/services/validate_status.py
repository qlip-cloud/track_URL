import frappe
import json
import os
import time
UP = "UP"
DOWN = "DOWN"
import  threading
import multiprocessing
from datetime import datetime
import socket
import requests
from frappe.database.mariadb.database import MariaDBDatabase as Database
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def ping(url):

    status_code = 200

    try:

        response = requests.request("GET", url, timeout=5, verify=False)

        status_code = response.status_code

    except Exception as error:

        status_code = 500
        

    return status_code

def setup_update(setup = None, method = None):

    cache = frappe.cache()

    status = update_status_cache(cache)

    if status:

        active_daemon(cache)

@frappe.whitelist()
def validate_daemon():

    current_process = multiprocessing.active_children()

    if not current_process:
        
        setup_update()

def server_update(server = None, method = None):

    cache = frappe.cache()

    update_cache_url(cache)

def update_cache_url(cache):

    urls  = frappe.db.get_list("qp_vc_Server", filters = {"status": "ON"}, fields = ["name", "url"])    
    
    cache.set("urls", json.dumps(urls))

def active_daemon(cache):
    
    update_cache_url(cache)
    
    database  = Database()
    
    t = multiprocessing.Process(daemon = True, name = "make_ping", target=execute_thread_2, args=(database,))

    t.start()

def update_status_cache(cache):

    setup = frappe.get_doc("qp_vc_Setup")

    status = setup.status == "Activo"

    is_status = is_status_true(cache)

    if status != is_status:

        cache.set("status",str(status))

    return status

def execute_thread_2(database):

    cache = frappe.cache()


    while is_status_true(cache):

        urls = json.loads(cache.get("urls"))

        cache.set("ping", "ON")

        for url in urls:
            
            response = ping(url.get("url"))

            if response == 500:

                sql = """
                    INSERT INTO tabqp_vc_ServerLog 
                        (name, server, status, server_url, creation, modified, modified_by, owner, docstatus) 
                    values 
                        ('{}','{}','{}', '{}','{}','{}','{}', '{}', '{}')""".format(
                            str(datetime.now()), 
                            url.get("name"),
                            DOWN,
                            #UP if int(respuesta) == 0 else DOWN,
                            url.get("url"),
                            datetime.now(),
                            datetime.now(),
                            "Administrator",
                            "Administrator",
                            0
                        )
            
                database.sql(sql,auto_commit=True)
            
def is_status_true(cache):

    cache_value = cache.get("status").decode('utf-8') if cache.get("status") else ""
    
    return True if cache_value == 'True' else False