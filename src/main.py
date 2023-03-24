import os
import csv
import json
import re
import pandas as pd

from arcgis.gis import GIS
import pprint

from src import cfg
from src.log import set_logger


def csv2xlsx(file_csv: str):
    read_file = pd.read_csv(file_csv)
    xls_file = file_csv + '.xlsx'
    if os.path.isfile(xls_file):
        os.remove(xls_file)
    read_file.to_excel(xls_file, index=None, header=True)
    print(f"File Excel {xls_file} created !")


def csv_file_out_create_with_headers():
    csv_dict = cfg.CSV_DICT
    dir_csv = str(os.path.join(os.getcwd(), cfg.CSV_FOLDER_OUT))  # from cfg.file

    if not os.path.exists(dir_csv):
        os.makedirs(dir_csv)

    file_csv = str(os.path.join(os.getcwd(), cfg.CSV_FOLDER_OUT, cfg.CSV_FILE))  # from cfg.file
    # Если выходной CSV файл существует - удаляем его
    if os.path.isfile(file_csv):
        os.remove(file_csv)
    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.CSV_DELIMITER)
        csv_file_open.writeheader()
    return file_csv


def csv_file_write_row_from_dict(file_csv: str, csv_dict: dict):
    with open(file_csv, 'a', newline='\n', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.CSV_DELIMITER)
        try:
            csv_file_open.writerow(csv_dict)
        except Exception as e:
            print("Exception occurred " + str(e))  # , exc_info=True
        csv_file.close()


def get_all_layers_info():
    log = set_logger(cfg.FILE_LOG)
    # gis = GIS(cfg.PORTAL_URL)
    csv_dict = cfg.CSV_DICT
    file_csv = cfg.CSV_FILE
    for key in csv_dict:
        csv_dict[key] = ''

    gis = GIS(cfg.PORTAL_URL, cfg.PORTAL_USER, cfg.PORTAL_PASS, verify_cert=False)
    print(f"Connected to {gis.properties.portalHostname} as {gis.users.me.username}")

    file_csv = csv_file_out_create_with_headers()

    # layer_items = gis.content.get(layer_guid)  # <Item title:"Title_layer" type:Feature Layer Collection owner:user>
    servers = gis.admin.servers.list()
    print(servers)

    # for folder in cfg.SERVER_FOLDERS: # если надо только конкретные
    for folder in servers[0].services.folders:
        print(folder)
        server1 = servers[0]
        # SERVER_FOLDERS = server1.services.folders
        services = server1.services.list(folder=folder)

        # service = services[1]

        for service in services:
            for key in csv_dict:
                csv_dict[key] = ''
            ii = service.iteminformation
            manifest = dict(ii.manifest)
            properties = dict(ii.properties)

            if "status" in manifest:
                if str(manifest['status']).lower() == 'error'.lower():
                    print(f"Ошибка в этом манифесте!!!")
                    pprint.pprint(manifest)
            else:
                if "databases" in manifest:
                    server_re_str = r'SERVER=(.*?);'
                    instance_re_str = r'INSTANCE=(.*?);'
                    user_re_str = r'USER=(.*?);'
                    dbconn_re_str = r'DB_CONNECTION_PROPERTIES=(.*?);'

                    try:
                        layer_name = manifest['databases'][0]['datasets'][0]['onServerName']
                        print(layer_name)
                        csv_dict['FOLDER'] = folder
                        csv_dict['LAYER'] = manifest['databases'][0]['datasets'][0]['onServerName']
                        csv_dict['CLIENT'] = manifest['resources'][0]['clientName']
                        csv_dict['PRJPATH'] = manifest['resources'][0]['onPremisePath']

                        if "name" in properties:
                            csv_dict['ONSERVERNAME'] = properties['name']
                            csv_dict['TITLE'] = properties['title']
                            csv_dict['GUID'] = properties['guid']
                            csv_dict['SUMMARY'] = properties['summary']
                            csv_dict['TYPE'] = properties['type']
                            csv_dict['SR'] = properties['spatialReference']

                        by_ref = str(manifest['databases'][0]['byReference']).lower()
                        if by_ref == 'true'.lower():
                            csv_dict['LOCAL'] = "DATABASE"
                            sde_server_connection = manifest['databases'][0]['onServerConnectionString']
                            csv_dict['SERVER'] = re.findall(server_re_str, sde_server_connection)[
                                0]  # SERVER=[A-Za-z0-9]+ matching
                            csv_dict['INSTANCE'] = re.findall(instance_re_str, sde_server_connection)[
                                0]  # INSTANCE=(.*?); matching
                            csv_dict['USER'] = re.findall(user_re_str, sde_server_connection)[0]  # USER=(.*?); matching
                            csv_dict['DBCONPROP'] = re.findall(dbconn_re_str, sde_server_connection)[0]  # USER=(.*?); matching
                            csv_dict['CONN'] = str(sde_server_connection).replace(";", "#")
                        else:
                            print(f"Найден локальный источник")
                            pprint.pprint(manifest)
                            pprint.pprint(properties)
                            csv_dict['LOCAL'] = "LOCAL"
                            csv_dict['FOLDER'] = folder

                    except Exception as e:
                        str_err = f"Exception occurred: {str(e)}.  manifest: {str(manifest)}"
                        print(str_err)
                        log.error(str_err)
            if len(csv_dict['LAYER']):
                csv_file_write_row_from_dict(file_csv, csv_dict)
    csv2xlsx(file_csv)




if __name__ == "__main__":
    get_all_layers_info()
