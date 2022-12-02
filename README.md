# cam-image-blob-uploader
### Retrieve Images from Network Cameras and Upload them to Azure Blob Storage

The purpose of these scripts is to allow a system to connect to one or multiple cameras (or camera views) and pull a current still image and upload it to Azure Blob Storage.

## Pre-Requisites
- A Working Network Camera that has a URL to pull the current static image (Refer to manufacturers documentation to check capability and determine the specific URL).
- An active [Azure account](https://azure.microsoft.com/en-us/get-started) if you don't have one you can [create a free account](https://azure.microsoft.com/free/).
  - Setup an [Azure Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create).
- Python (Verified with 3.8.10, but other versions 3.7+ that support the Azure Python SDK should work as well.)
- PIP
- Azure Python SDK Storage Blob library
  ```
  pip install azure-storage-blob
  ```
  > ([Click Here for more information about the Microsoft Azure Python SDK](https://learn.microsoft.com/en-us/azure/developer/python/sdk/azure-sdk-overview))

## Usage
- Ensure all Pre-Requisites are met
- In your target storge account create a [blob container](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal#create-a-container).
- Either Retrieve one of your Storage Account's Access Key Connection String or Generate a scoped SAS token and retrieve it's connection string. See: [Manage storage account access keys](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal).
- Configure an environment variable to pass the SAS URL to the script (Recommended: name the variable: `AZURE_STORAGE_CONNECTION_STRING` if you use a different environment variable name be sure to update the config.yaml.  
  Linux/Mac Example:
  ```
  export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=<storage-account-name>;AccountKey=<key>;EndpointSuffix=core.windows.net"
  ```
  Windows Example:
  ```
  set AZURE_STORAGE_CONNECTION_STRING "DefaultEndpointsProtocol=https;AccountName=<storage-account-name>;AccountKey=<key>;EndpointSuffix=core.windows.net"
  ```
- Configure an connection string environment variable for each camera. Be sure to set the URL to match with your specific Camera's static image URL.  
  Example Linux/Mac:
  ```
  export CAMERA1_CONNECTION_STRING="https://<username>:<password>@10.20.30.101/tmpfs/auto.jpg"
  export CAMERA2_CONNECTION_STRING="https://<username>:<password>@10.20.30.102/tmpfs/auto.jpg"
  export CAMERA3_CONNECTION_STRING="https://<username>:<password>@10.20.30.103/tmpfs/auto.jpg"
  ```
  Example Windows:
  ```
  set CAMERA1_CONNECTION_STRING "https://<username>:<password>@10.20.30.101/tmpfs/auto.jpg"
  set CAMERA2_CONNECTION_STRING "https://<username>:<password>@10.20.30.102/tmpfs/auto.jpg"
  set CAMERA3_CONNECTION_STRING "https://<username>:<password>@10.20.30.103/tmpfs/auto.jpg"
  ```
- If you have not alread done so, download and place all script and config files in a working directory
- Update the config.yaml:
  - Set the container name to match the Storage Account Blob Container you have setup
  - Define your Cameras/Views (Note: for multiple views camera must support a unique URL for each view).
    - Each camera in the `cameras` list should have both a defined **name** (this will be used as the prefix of the uploaded camera file) and a **connection_str_env_var** (referencing the appropriate environment variable you setup for each camera).  
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
  - (Optional) You can configure a timeout value (in seconds) in the config.yaml - this value determines how long the script waits to receive the image from a camera before giving up and moving onto the next camera (default is 10 seconds).
  - Here is an example `config.yaml` file:
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
## Notes
- The current version uses SAS tokens, use care as anyone with access to the SAS token can access your storage with whatever level of permissions you have set for the token.
### Current Known Limitations
- The current version does not clean up the cached images which over time could fill up your local storage, so be sure to occasionally remove old images from the `img_cache` directory - you could setup this up as a simple cron job.



> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
