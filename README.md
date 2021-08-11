## Simple File Transfer Server over HTTP

A simple file server with both upload and download capability

once the server starts, devices on the network can access the server on HOST:PORT

people can view, search, download and upload files under the root directory

### Instructions

* install python3.X [once]
* install all the packages specified in 'requirements.txt' [once]
* run 'reset_settings.py' and change 'shared_direcory' to your likings in 'server_settings.json' file [optional]
* run 'run_server.py'

#### Notes
* run 'reset_settings.py' to reset settings to defualt
* edit the 'server_settings.json' file to change settings [after it has benn created]

* default host is "0.0.0.0" and port is 9921
* running server on the default host and port might not be allowed in all devices, then take steps accordingly
* if host and port are set to default, you can visit http://<yourdeviceip>:9921 from any connected devices to reash the file server