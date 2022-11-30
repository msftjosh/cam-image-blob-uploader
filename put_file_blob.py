def put_file(container_name, local_file_name, connect_str):
  from azure.storage.blob import BlobServiceClient

  try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    with open(file=local_file_name, mode="rb") as data:
      blob_client.upload_blob(data)

  except Exception as e:
    print("An exception has occured while trying to upload: " + local_file_name + ":", e)