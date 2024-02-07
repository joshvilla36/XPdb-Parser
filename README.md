<!-- ABOUT THE PROJECT -->
## About The Project

This is a python parser for the OSX XProtect XPdb.

For more info: https://support.apple.com/guide/security/protecting-against-malware-sec469d47bd8/web

https://eclecticlight.co/2023/09/04/is-macoss-new-xprotect-behavioural-security-preparing-to-go-live/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

```
usage: parse_xpdb.py [-h] [--file FILE] [--output OUTPUT] [--hostname HOSTNAME]

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  input file (xpdb)
  --output OUTPUT, -o OUTPUT
                        output csv file
  --hostname HOSTNAME, -hn HOSTNAME
                        source hostname of the XPdb if parsing offline, if not provided it will use the hostname of the current system

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>