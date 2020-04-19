import csv, json, sys
from pathlib import Path
from datetime import datetime
from ciscoaxl import axl
from ciscoris import ris
import argparse
from email_util import send_email
from gooey import Gooey, GooeyParser
import cucm

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR.joinpath("img")

start_time = datetime.now()
print(f"status: starting {start_time}")

# GUI if no cli args, otherwise default to cli
if len(sys.argv) >= 2:
    if not "--ignore-gooey" in sys.argv:
        sys.argv.append("--ignore-gooey")


def output_filename(filename, results):
    """
    Construct the output filename
    """
    if results.timestamp:
        date_time = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")
        lname = filename.split(".")[0]
        rname = filename.split(".")[-1]
        new_filename = f"{lname}_{date_time}.{rname}"
    else:
        new_filename = filename

    return new_filename


def write_csv(filename, results, content):
    """
    write output to csv file
    """
    filename = output_filename(filename, results)
    with open(filename, "w", newline="") as csvfile:
        fieldnames = [key for key in content[-1].keys()]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for each in content:
            writer.writerow(each)


@Gooey(
    program_name="CUCM Extraction Tool",
    program_description="Cisco Unified Communications Manager Tool",
    # default_size=(610, 850),
    menu=[
        {"name": "File", "items": []},
        {"name": "Tools", "items": []},
        {
            "name": "Help",
            "items": [
                {
                    "type": "Link",
                    "menuTitle": "Find us on Github",
                    "url": "https://github.com/bradh11/cucm-exporter",
                }
            ],
        },
    ],
    # image_dir=IMG_DIR,
    tabbed_groups=True,
)
def main():
    date_time = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")

    # initialize the CLI parser
    parser = GooeyParser(description="Cisco Unified Communications Manager Tool")
    cucm_group = parser.add_argument_group(title="cucm connection")
    file_group = parser.add_argument_group(title="output file")
    email_group = parser.add_argument_group(
        title="optional email parameters",
        description="send the output to an email address",
    )

    cucm_group.add_argument(
        "--address",
        "-a",
        action="store",
        dest="cucm_address",
        help="specify cucm address",
        default="ucm1.presidio.cloud",
        required=True,
    )

    cucm_group.add_argument(
        "--version",
        "-v",
        action="store",
        dest="cucm_version",
        choices=["8.5", "10.0", "10.5", "11.0", "11.5", "12.0", "12.5"],
        help="specify cucm AXL version",
        required=False,
        default="11.0",
    )

    cucm_group.add_argument(
        "--username",
        "-u",
        action="store",
        dest="cucm_username",
        help="specify ucm account username with AXL permissions",
        required=True,
        default="Administrator",
    )

    cucm_group.add_argument(
        "--password",
        "-p",
        action="store",
        dest="cucm_password",
        help="specify ucm account password",
        required=True,
        default="Dev@1998",
        widget="PasswordField",
    )

    file_group.add_argument(
        "--out",
        "-o",
        action="store",
        dest="filename",
        help='filename of export file (.csv format) - default="export.csv"',
        required=False,
        default="export.csv",
    )

    file_group.add_argument(
        "--timestamp",
        "-t",
        action="store_true",
        dest="timestamp",
        help="append filename with timestamp",
    )

    cucm_group.add_argument(
        "--export",
        "-e",
        action="store",
        dest="cucm_export",
        choices=["users", "phones", "translations", "sip-trunks", "registered-phones"],
        help="specify what you want to export",
        required=False,
        default="users",
    )

    email_group.add_argument(
        "--smtpserver",
        "-s",
        action="store",
        dest="smtpserver",
        required=False,
        help="smtp server name or ip address",
    )

    email_group.add_argument(
        "--mailto",
        "-m",
        action="store",
        dest="mailto",
        required=False,
        help="send output to mail recipient",
    )

    # update variables from cli arguments
    cli_args = parser.parse_args()
    filename = cli_args.filename
    # print(cli_args)

    # store the UCM details
    cucm_address = cli_args.cucm_address
    cucm_username = cli_args.cucm_username
    cucm_password = cli_args.cucm_password
    cucm_version = cli_args.cucm_version

    # initialize Cisco AXL connection
    ucm_axl = axl(
        username=cucm_username,
        password=cucm_password,
        cucm=cucm_address,
        cucm_version=cucm_version,
    )
    ucm_ris = ris(
        username=cucm_username,
        password=cucm_password,
        cucm=cucm_address,
        cucm_version=cucm_version,
    )

    if cli_args.cucm_export == "users":
        output = cucm.export_users(ucm_axl)
        if len(output) > 0:
            write_csv(filename=filename, results=cli_args, content=output)
        else:
            print(f"status: no {cli_args.cucm_export} found...")
        print(f"status: elapsed time -- {datetime.now() - start_time}\n")
    elif cli_args.cucm_export == "phones":
        output = cucm.export_phones(ucm_axl)
        if len(output) > 0:
            write_csv(filename=filename, results=cli_args, content=output)
        else:
            print(f"status: no {cli_args.cucm_export} found...")
        print(f"status: elapsed time -- {datetime.now() - start_time}\n")
    elif cli_args.cucm_export == "translations":
        output = cucm.export_translations(ucm_axl)
        if len(output) > 0:
            write_csv(filename=filename, results=cli_args, content=output)
        else:
            print(f"status: no {cli_args.cucm_export} found...")
        print(f"status: elapsed time -- {datetime.now() - start_time}\n")
    elif cli_args.cucm_export == "sip-trunks":
        output = cucm.export_siptrunks(ucm_axl)
        if len(output) > 0:
            write_csv(filename=filename, results=cli_args, content=output)
        else:
            print(f"status: no {cli_args.cucm_export} found...")
        print(f"status: elapsed time -- {datetime.now() - start_time}\n")
    else:
        print(f"exporting {cli_args.cucm_export} is not yet supported")
        return

    # send email if selected
    if cli_args.mailto and cli_args.smtpserver:
        response = send_email(
            smtp_server=cli_args.smtpserver,
            send_to_email=cli_args.mailto,
            fileToSend=filename,
        )
        print(
            f"status: mail sent to {cli_args.mailto} via {cli_args.smtpserver} at {date_time}"
        )
    elif cli_args.mailto and not cli_args.smtpserver:
        print(f"status: mail unable to send.  no smtp server was defined")
    elif cli_args.smtpserver and not cli_args.mailto:
        print(f"status: mail unable to send.  no mailto address was defined")


if __name__ == "__main__":
    main()
