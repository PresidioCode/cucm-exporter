# CUCM Export command line utility

This tool was created in an effort to make exporting information from Cisco Unified Communications Manager (CUCM) easy. Some example use cases might include regularly exporting a user and phone number list to csv on a recurring schedule.

- download [cucm-exporter.exe](/releases/download/0.6/cucm-exporter.exe) for windows
- download `cucm-exporter` for mac (coming soon)

## Usage

This tool will be packaged as a standalone executable file that can be used with syntax as seen below:

```
cucm-exporter --help                                                                                                  status: starting 2020-03-23 20:07:33.256787
usage: cucm-exporter.exe [-h] --address CUCM_ADDRESS [--version {8.0,10.0,10.5,11.0,11.5,12.0,12.5}] --username
                         CUCM_USERNAME --password CUCM_PASSWORD [--out FILENAME] [--timestamp]
                         [--export {users,phones}] [--smtpserver SMTPSERVER] [--mailto MAILTO]

optional arguments:
  -h, --help            show this help message and exit

cucm connection:
  --address CUCM_ADDRESS, -a CUCM_ADDRESS
                        specify cucm address
  --version {8.0,10.0,10.5,11.0,11.5,12.0,12.5}, -v {8.0,10.0,10.5,11.0,11.5,12.0,12.5}
                        specify cucm AXL version
  --username CUCM_USERNAME, -u CUCM_USERNAME
                        specify ucm account username with AXL permissions
  --password CUCM_PASSWORD, -p CUCM_PASSWORD
                        specify ucm account password
  --export {users,phones}, -e {users,phones}
                        specify what you want to export

output file:
  --out FILENAME, -o FILENAME
                        filename of export file (.csv format) - default="export.csv"
  --timestamp, -t       append filename with timestamp

email options:
  --smtpserver SMTPSERVER, -s SMTPSERVER
                        smtp server name or ip address
  --mailto MAILTO, -m MAILTO
                        send output to mail recipient

```

EXAMPLE 1 - running the executable

```
cucm-exporter -a 10.129.225.201 -v 11.0 -o "my file.csv" -u axlusername -p axlpassword -t --export users
```

EXAMPLE 2 - the raw python code can be run from source after installing dependencies `pip install -r requirements.txt`

```
python cucm-exporter.py -a 10.129.225.201 -v 11.0 -o "my file.csv" -u axlusername -p axlpassword -t --export users
```
