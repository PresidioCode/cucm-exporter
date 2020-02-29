import sys, csv
from datetime import datetime
from ciscoaxl import axl
import argparse

# initialize the CLI parser
parser = argparse.ArgumentParser()
cucm_group = parser.add_argument_group(title='cucm connection')
file_group = parser.add_argument_group(title='output file')

cucm_group.add_argument('--address','-a', action='store',
                    dest='cucm_address',
                    help='specify cucm address',
                    required=True)

cucm_group.add_argument('--version','-v', action='store',
                    dest='cucm_version',
                    choices=['11.0', '11.5', '12.0', '12.5'],
                    help='specify cucm AXL version',
                    required=False,
                    default='11.0')

cucm_group.add_argument('--username','-u', action='store',
                    dest='cucm_username',
                    help='specify ucm account username with AXL permissions',
                    required=True,
                    default='CCMAdministrator')

cucm_group.add_argument('--password','-p', action='store',
                    dest='cucm_password',
                    help='specify ucm account password',
                    required=True,
                    default='admin')

file_group.add_argument('--out','-o', action='store',
                    dest='filename',
                    help='filename of export file (.csv format) - default="export.csv"',
                    required=False,
                    default='export.csv')

file_group.add_argument('--timestamp','-t', action='store_true',
                    dest='timestamp',
                    help='append filename with timestamp')

cucm_group.add_argument('--export','-e', action='store',
                    dest='cucm_export',
                    choices=['users','phones'],
                    help='specify what you want to export',
                    required=False,
                    default='users')

# update variables from cli arguments
results = parser.parse_args()
filename = results.filename
# print(results)

# Update UCM details
cucm_address = results.cucm_address
cucm_username = results.cucm_username
cucm_password = results.cucm_password
cucm_version = results.cucm_version

# initialize Cisco AXL connection
ucm = axl(username=cucm_username,
        password=cucm_password,
        cucm=cucm_address,
        cucm_version=cucm_version)

def output_filename(filename):
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

def write_csv(filename, all_users):
    """
    write output to csv file
    """
    filename = output_filename(filename)

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['username','firstname', 'lastname','displayname','primary_extension', 'telephone_number','directory_uri']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in all_users:
            writer.writerow(user)


def export_users(ucm):
    """
    retrieve users from ucm
    """
    user_list = ucm.get_users()
    all_users = []

    for user in user_list:
        user_dict = dict()
        user_dict["username"] = user.userid
        user_dict["firstname"] = user.firstName
        user_dict["lastname"] = user.lastName
        user_dict["displayname"] = user.displayName
        user_dict["primary_extension"] = user.primaryExtension.pattern
        user_dict["telephone_number"] = user.telephoneNumber
        user_dict["directory_uri"] = user.directoryUri

        all_users.append(user_dict)
        print(f"{user_dict.get('username')} -- {user_dict.get('firstname')} {user_dict.get('lastname')}:  {user_dict.get('primary_extension')}")

    print("-" * 35)
    print(f"number of users: {len(all_users)}")
    return all_users


def main():
    if results.cucm_export == 'users':
        all_users = export_users(ucm)
        write_csv(filename=filename, all_users=all_users)
    else:
        print(f"exporting {results.cucm_export} is not yet supported")

if __name__ == "__main__":
    main()