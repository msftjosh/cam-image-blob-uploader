import os, yaml
from get_cam_img import get_jpg
from put_file_blob import put_file

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

blob_container_name = config['blob_container']
storage_conn_str = os.getenv(config['blob_connection_str_env_var'])

if config['blob_connection_str_env_var'] not in os.environ:
  print("Missing Storage Account Connection String Environment Variable (" + config['blob_connection_str_env_var'] + ")")
  exit()

for i in config['cameras']:
  cam_name = config.get('cameras').get(i).get('name')
  cam_conn_str = os.getenv(config.get('cameras').get(i).get('connection_str_env_var'))
  if config.get('cameras').get(i).get('connection_str_env_var') not in os.environ:
    print("Missing Connection String Environment Variable (" + config.get('cameras').get(i).get('connection_str_env_var') + ") for " + cam_name)
    continue
  local_file=(get_jpg(cam_conn_str, cam_name, config['timeout']))
  if(local_file is not None):
    put_file(blob_container_name, local_file, storage_conn_str)
    print("Uploaded " + str(local_file.name) + " to Blob Container: " + blob_container_name)