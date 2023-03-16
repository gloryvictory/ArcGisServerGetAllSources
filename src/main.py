import os
import csv
import json

from arcgis.gis import GIS
import pprint

from src import cfg
from src.log import set_logger


def csv_file_out_create_with_headers():
    csv_dict = cfg.CSV_DICT
    file_csv = str(os.path.join(os.getcwd(), cfg.CSV_FOLDER_OUT, cfg.CSV_FILE))  # from cfg.file
    # Если выходной CSV файл существует - удаляем его
    if os.path.isfile(file_csv):
        os.remove(file_csv)
    with open(file_csv, 'w', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.CSV_DELIMITER)
        csv_file_open.writeheader()


def get_all_layers_info():
    log = set_logger(cfg.FILE_LOG)
    # gis = GIS(cfg.PORTAL_URL)
    csv_dict = cfg.CSV_DICT
    file_csv = cfg.CSV_FILE
    for key in csv_dict:
        csv_dict[key] = ''

    gis = GIS(cfg.PORTAL_URL, cfg.PORTAL_USER, cfg.PORTAL_PASS, verify_cert=False)
    print(f"Connected to {gis.properties.portalHostname} as {gis.users.me.username}")

    # layer_items = gis.content.get(layer_guid)  # <Item title:"Title_layer" type:Feature Layer Collection owner:user>
    servers = gis.admin.servers.list()
    for folder in cfg.SERVER_FOLDERS:
        print(servers)
        server1 = servers[0]
        services = server1.services.list(folder=folder)

        service = services[1]
        ii = service.iteminformation
        manifest = dict(ii.manifest)

        if "status" in manifest:
            if str(manifest['status']).lower() == 'error'.lower():
                pprint.pprint(manifest)
        else:
            if "databases" in manifest:
                # manifest_str = str(manifest).replace("\'", "\"")
                # db_info = json.loads(manifest_str)
                # layer_name = db_info['databases'][0]['datasets'][0]['onServerName']
                try:
                    layer_name = manifest['databases'][0]['datasets'][0]['onServerName']
                    sde_server_name = manifest['databases'][0]['onServerName']
                    sde_server_connection = manifest['databases'][0]['onServerConnectionString']
                    print(layer_name)
                    print(sde_server_name)
                    print(sde_server_connection)

                    csv_dict['LAYER'] = layer_name
                    csv_dict['ONSERVERNAME'] = sde_server_name
                    csv_dict['CONN'] = sde_server_connection


                except Exception as e:
                    str_err = f"Exception occurred: {str(e)}.  Portal:  {gis.properties.portalHostname} as {gis.users.me.username}"
                    print(str_err)
                    log.error(str_err)



        # for service in services:
        #     ii = service.iteminformation
        #     manifest = ii.manifest
        #     pprint.pprint(manifest)
        #     log.info(manifest)
        #     # properties = ii.properties
        # pprint.pprint(properties)
        # log.info(properties)

    # services = server1.services.list(folder="novatek")
    # for service in services:
    #     ii = service.iteminformation
    #     manifest = ii.manifest
    #     pprint.pprint(manifest)
    #     properties = ii.properties
    #     pprint.pprint(properties)
    #     log.info(manifest)

    # csv_dict['EMAIL'] = str_email
    # csv_dict['TEL'] = str_tel
    # csv_dict['PRIORITY'] = str_priority
    # csv_dict['CITY'] = str_city
    # csv_dict['GENDER'] = str_gender
    # csv_dict['AGE'] = str_age
    # csv_dict['GR'] = str_gr
    # csv_dict['ZAN'] = str_zan
    # csv_dict['OBR'] = str_obr
    # csv_dict['NAVIK'] = str_nav
    #
    # with open(file_csv, 'a', newline='\n', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
    #     csv_file_open = csv.DictWriter(csv_file, csv_dict.keys(), delimiter=cfg.CSV_DELIMITER)
    #     try:
    #         # print(csv_dict['FULLNAME'])
    #         csv_file_open.writerow(csv_dict)
    #     except Exception as e:
    #         print("Exception occurred " + str(e))  # , exc_info=True
    #     csv_file.close()
    #


if __name__ == "__main__":
    get_all_layers_info()
