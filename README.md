# CUCM Export command line utility

This tool was created in an effort to make exporting information from Cisco Unified Communications Manager (CUCM) easy. Some example use cases might include regularly exporting a user and phone number list to csv on a recurring schedule.

## Usage

This tool will be packaged as a standalone executable file that can be used with syntax as seen below:

```
usage: main.py [-h] -a CUCM_ADDRESS [-v {11.0,11.5,12.0,12.5}] -u
               CUCM_USERNAME -p CUCM_PASSWORD [-o FILENAME] [-t]

optional arguments:
  -h, --help            show this help message and exit

cucm connection:
  -a CUCM_ADDRESS, --address CUCM_ADDRESS
                        specify cucm address
  -v {11.0,11.5,12.0,12.5}, --version {11.0,11.5,12.0,12.5}
                        specify cucm AXL version
  -u CUCM_USERNAME      specify ucm account username with AXL permissions
  -p CUCM_PASSWORD      specify ucm account password

output file:
  -o FILENAME, --out FILENAME
                        filename of export file (.csv format) -
                        default="userlist.csv"
  -t                    append filename with timestamp
```

EXAMPLE 1 - running the executable (download coming soon...)

```
cucm-exporter -a 10.129.225.201 -o "my file.csv" -u axlusername -p axlpassword -v 11.0 -t
```

EXAMPLE 2 - the raw python code can be run after installing dependencies

```
python main.py -a 10.129.225.201 -o "my file.csv" -u axlusername -p axlpassword -v 11.0 -t
```
