# Reverse Proxy
An implementation of a HTTP reverse proxy which features:
* round-robin load balancing strategy
* in-memory caching
* multiple domains and hosts support

## Requirements
The following libraries are required to run the application:
* YAML
* requests

They can be installed from the command line by running the following command inside the reverse_proxy directory:
```
cd reverse_proxy
pip install -r requirements.txt
```
## Execution
```
cd reverse_proxy
python reverse_proxy.py
```
## Sample requests
The requests can follow the format:
```
curl --header "Host:<service_domain>" http://<proxy_address>:<proxy_port>
```
* <service_domain>: name of the domain of one of the downstream services
* <proxy_address>: address where the reverse proxy listens for HTTP traffic
* <proxy_port>: port where the reverse proxy listens for HTTP traffic

An example of request:
```
curl --header "Host:my-service.my-company.com" http://127.0.0.1:8080
```