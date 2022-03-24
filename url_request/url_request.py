import pathlib

import utils
import pandas as pd
import requests

url = 'https://glusfqycvwrucp9-db202202211424.adb.eu-zurich-1.oraclecloudapps.com/ords/sensor_datalake1/sens/insert/'

page_result = utils.get_all_pages(url)

df = utils.to_data_frame(page_result)

df.to_excel('db_data.xlsx', index=False)