def get_jpg(url,file_prefix,timeout):
  import requests, time
  from pathlib import Path

  timestamp = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())

  Path('./img_cache/').mkdir(parents=True, exist_ok=True)

  filename = Path('./img_cache/' + file_prefix + '_'  + timestamp + '.jpg')
  
  try:
    response = requests.get(url, allow_redirects=True, timeout=timeout)

    filename.write_bytes(response.content)

    return filename

  except ConnectionError:
    print('Unable to connect to ' + file_prefix)

  except requests.exceptions.ConnectTimeout:
    print('Connection timeout to ' + file_prefix)

  except requests.exceptions.MissingSchema:
    print('No URL string passed for ' + file_prefix)

  except requests.exceptions.ConnectionError:
    print('Connection error to ' + file_prefix)

  except Exception as e:
    print("An exception has occured for " + file_prefix + ":",e)