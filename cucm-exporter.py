import csv
from datetime import datetime
from ciscoaxl import axl
import argparse
from email_util import send_email

start_time = datetime.now()
print(f"status: starting {start_time}")

# initialize the CLI parser
parser = argparse.ArgumentParser()
cucm_group = parser.add_argument_group(title="cucm connection")
file_group = parser.add_argument_group(title="output file")
email_group = parser.add_argument_group(title="email options")

cucm_group.add_argument(
    "--address",
    "-a",
    action="store",
    dest="cucm_address",
    help="specify cucm address",
    required=True,
)

cucm_group.add_argument(
    "--version",
    "-v",
    action="store",
    dest="cucm_version",
    choices=["8.0", "10.0", "10.5", "11.0", "11.5", "12.0", "12.5"],
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
    default="admin",
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
    choices=["users", "phones"],
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
ucm = axl(
    username=cucm_username,
    password=cucm_password,
    cucm=cucm_address,
    cucm_version=cucm_version,
)


def output_filename(filename):
    """
    Construct the output filename
    """
    if cli_args.timestamp:
        date_time = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")
        lname = filename.split(".")[0]
        rname = filename.split(".")[-1]
        new_filename = f"{lname}_{date_time}.{rname}"
    else:
        new_filename = filename

    return new_filename


def write_csv(filename, data):
    """
    write output to csv file
    """

    with open(filename, "w", newline="") as csvfile:
        fieldnames = [key for key in data[-1].keys()]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_users(ucm):
    """
    retrieve users from ucm
    """
    user_list = ucm.get_users(
        tagfilter={
            "userid": "",
            "firstName": "",
            "lastName": "",
            "directoryUri": "",
            "telephoneNumber": "",
            "enableCti": "",
            "mailid": "",
            "primaryExtension": {"pattern": ""},
        }
    )
    all_users = []

    for user in user_list:
        user_dict = dict()
        user_dict["userid"] = user.userid
        user_dict["firstName"] = user.firstName
        user_dict["lastName"] = user.lastName
        user_dict["telephoneNumber"] = user.telephoneNumber
        user_dict["primaryExtension"] = user.primaryExtension.pattern
        user_dict["directoryUri"] = user.directoryUri
        user_dict["mailid"] = user.mailid

        all_users.append(user_dict)
        print(
            f"{user_dict.get('userid')} -- {user_dict.get('firstName')} {user_dict.get('lastName')}:  {user_dict.get('primaryExtension')}"
        )

    print("-" * 35)
    print(f"number of users: {len(all_users)}")
    return all_users


def export_phones():
    """
    export phone details
    """
    phone_list = ucm.get_phones(tagfilter={"userid": "",})


def main():
    date_time = datetime.now().strftime("%m-%d-%Y_%H.%M.%S")

    if cli_args.cucm_export == "users":
        all_users = export_users(ucm)
        filename = output_filename(cli_args.filename)
        write_csv(filename=filename, all_users=all_users)
        print(f"status: elapsed time -- {datetime.now() - start_time}")
    elif cli_args.cucm_export == "phones":
        all_phones = export_phones(ucm)
        filename = output_filename(cli_args.filename)
        write_csv(filename=filename, all_users=all_phones)
        print(f"status: elapsed time -- {datetime.now() - start_time}")
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
