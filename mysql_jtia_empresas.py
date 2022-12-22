#!/usr/bin/python3

import time
import pymysql
import xmlrpc.client
from datetime import date, datetime
import ipdb

# Open database connection with JTIA


# data for connection with Odoo

# url = "http://localhost:1469"
# user = "admin"
# passw = "admin"
# dbname = "maga_jtia"

url = "https://jtia.odoo.com"
user = "admin"
# passw = "EjiM3quae9Oh"
passw = "admin"
dbname = "maga-systems-jtia-prod-1-1752958"


panameno_id = 4
professional_id = 1

# Open connection with Odoo for JTIA company

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

uid = common.authenticate(dbname, user, passw, {})

# prepare a cursor object using cursor() method
db = pymysql.connect(host="137.184.12.140", port=3306, user="jcmderhmzq", password="9cwdC2CpED", db="jcmderhmzq", connect_timeout=6)
cursor = db.cursor()

#primro saco el nombre de odoo luego hago la query a la tabla empresas
#me quedo con el ID de la tabla empresas
#luego consulto la tabla empresas_responsables para la empresa_id del ID de arriba y ahi me van aparecer los ID de los profesionales
#hacere un select a la tabla profesionales para el id_profesional que me de la tabla de arriba

all_companies = models.execute_kw(dbname, uid, passw, 'res.partner', 'search_read', [[('is_company', '=', True)]], {'fields': ['name']})
companies_names = [x['name'] for x in all_companies]
ipdb.set_trace()
for company in companies_names:
    print(company)
    cursor.execute(f"select id from empresas where empresa ='{company}'")
    old_company = cursor.fetchone()
    if not old_company:
        continue
    print(f'este es el resultado de la query que se queda con el id de empresa segun el nombre {old_company}')
    id_empresa = old_company[0]
    cursor.execute(f"select id_profesional from empresas_responsables where id_empresa ={id_empresa}")
    old_professionals = cursor.fetchall()
    if not old_professionals:
        continue
    print(f'f este es el resultado de hacer la consulta a la tabla empresas_responables para el id de empresa {id_empresa} --> {old_professionals} (largo {len(old_professionals)})')
    if len(old_professionals) > 1:
        ipdb.set_trace()
    for old_professional in old_professionals:
        id_professional = old_professional[0]
        cursor.execute(f"select id, cedula from profesionales where id ='{id_professional}'")
        result_ci = cursor.fetchone()
        if not result_ci:
            print('no tiene cedula deberiamos hacer para otra cosa')
        ci_professional = result_ci[0]
        partner_professional = models.execute_kw(dbname, uid, passw, 'res.partner', 'search_read', [[('cedula', '=', ci_professional)]], {'fields': ['id']})
        #esto es el profesional
        #ahora necesito buscar el certificado
        # id = models.execute_kw(dbname, uid, passw, 'jtia.certificate', 'write', [[certificate_ids[0]], {'caca': partner_professional}])




db.close()
