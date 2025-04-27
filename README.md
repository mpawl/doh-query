# doh-query
Easily query a DoH responder at the command line.

doh-query is developed with the lowest common demoninator in mind. Basic output will be printed to stdout. 

doh-query has been tested against many popular DoH responders including:
* Cloudflare
* OpenDNS
* Google
* Quad-9's

doh-query was created to test resoluting against Apple's DoH responder: `doh.dns.apple.com`. doh-query can be used to test hostname resolution against this DoH responder. [Details in this blog post](https://medium.com/@mpawl/whats-up-with-doh-dns-apple-com-investigating-apple-s-doh-responder-fce376a19052).

# Installation and Setup

It is recommended to use a Python Virtual Environment (venv) for running doh-query. Create and activate the venv as outlined below. 

```
python3 -m venv <virtual_environment_name>
source <path_to_venv>/bin/activate
```
Once the Python venv is installed and activated, install Python library dependencies. Pythong library dependencies are provided in a `requirements.txt` file. 
```
python3 -m pip install -r requirements.txt
```

# Usage

```
usage: doh_query.py [-h] -n NAME [-r RESPONDER] [-t TYPE] [-s]

Perform DoH query via Apple DNS

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Hostname to resolve
  -r RESPONDER, --responder RESPONDER
                        Responder to use (default: cloudflare-dns.com)
  -t TYPE, --type TYPE  DNS record type (default: A)
  -s, --short           Mimic dig +short output
```
