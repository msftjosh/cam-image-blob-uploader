# cam-image-blob-uploader
### Retrieve Images from Network Cameras and Upload them to Azure Blob

The purpose of these scripts is to allow a system to connect to one or multiple cameras (or camera views) and pull a current still image and upload it to Azure Blob.

## Pre-Requisites
- A Working Network Camera that has a URL to pull the current static image (Refer to manufacturers documentation to check capability and determine the specific URL).
- An active [Azure account](https://azure.microsoft.com/en-us/get-started) if you don't have one you can [create a free account](https://azure.microsoft.com/free/).
  - Setup an [Azure Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create)
- Python (Verified with3.8.10, but other versions 3.7+ that support Azure Python SDK should work as well)
- PIP
- Azure Python SDK Storage Blob library
```
pip install azure-storage-blob
```
>([Click Here for more info about the Microsoft Azure Python SDK](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview))

## Usage
- Ensure all Pre-Requisites are met
- In your target storge account create a [blob container](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal#create-a-container)
- Create a [SAS token for your blob container](https://learn.microsoft.com/en-us/rest/api/storageservices/create-account-sas) it will be used in the next step.
- Configure an environment Variable to pass the SAS URL to the script (Recommended: Call the variable: `AZURE_STORAGE_CONNECTION_STRING` if you use a different environment variable name then be sure to update the config.yaml.  
  Example:
  ```
  export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=<storage-account-name>;AccountKey=<key>;EndpointSuffix=core.windows.net"
  ```
- Like you did with the Storage Account connection string configure an environment variable for each camera ensuring the variable name matches what you defined in the config.yaml for each camera
  Example (be sure to set the URL to match with your specific Camera's image URL):
  ```
  export CAMERA1_CONNECTION_STRING="https://<username>:<password>@10.20.30.101/tmpfs/auto.jpg"
  export CAMERA2_CONNECTION_STRING="https://<username>:<password>@10.20.30.102/tmpfs/auto.jpg"
  export CAMERA3_CONNECTION_STRING="https://<username>:<password>@10.20.30.103/tmpfs/auto.jpg"
  ```
- In the working directory update the config.yaml
  - Update the container name to match the Storage Account Blob Container you have setup
  - Define your Cameras in the config.yaml
    - Each camera in the `cameras` list should define both a **name** (this will be used as the prefix of the uploaded camera file) and a **connection_str_env_var** (referencing the appropriate environment variable you setup for each camera).  
      Example config.yaml:
      ```
      cameras:
        cam1:
          name: Cam01
          connection_str_env_var: CAMERA1_CONNECTION_STRING
        cam2:
          name: Cam02
          connection_str_env_var: CAMERA2_CONNECTION_STRING
        cam3:
          name: Cam03
          connection_str_env_var: CAMERA3_CONNECTION_STRING
      ```
  - (Optional) If you did not use `AZURE_STORAGE_CONNECTION_STRING` to define your SAS token update `blob_connection_str_env_var` in the config.yaml to the appropriate environment variable name.
  - (Optional) You can configure the timeout value (in seconds) in the config.yaml - this value determines how long the script waits to receive the image from a camera before giving up and moving onto the next camera (default is 10 seconds).
  - Put it all together here is an example `config.yaml`:
    ```
      blob_container: exampleblobcontainer
      blob_connection_str_env_var: AZURE_STORAGE_CONNECTION_STRING
      timeout: 10
      cameras:
        cam1:
          name: Cam01
          connection_str_env_var: CAMERA1_CONNECTION_STRING
        cam2:
          name: Cam02
          connection_str_env_var: CAMERA2_CONNECTION_STRING
        cam3:
          name: Cam03
          connection_str_env_var: CAMERA3_CONNECTION_STRING
      ```
- Finally run the `main.py` script to kick off the image retrieval and upload (this can be configured to be triggered on a schedule using something like [cron](https://en.wikipedia.org/wiki/Cron)):
  ```
  python main.py
  ```
