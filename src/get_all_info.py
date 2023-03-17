from arcgis.gis import GIS
import pprint

from src import cfg
from src.log import set_logger


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
    services = servers[0].services.list(folder="novatek")
    for service in services:
        ii = service.iteminformation
        # manifest = ii.manifest
        # pprint.pprint(manifest)
        # log.info(manifest)

        properties = ii.properties
        pprint.pprint(properties)
        log.info(properties)


if __name__ == "__main__":
    get_all_layers_info()
