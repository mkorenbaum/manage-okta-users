#!/usr/bin/env python3
"""
Alvisofin Okta Users Management
mkorenbaum@paloaltonetworks.com
Version: 1.0.1 b1
"""
from okta.client import Client as OktaClient
import asyncio
import os
import sys
import argparse
import uuid
import random
import string

GLOBAL_MY_SCRIPT_NAME = "Manage Alvisofin Demo Portal Users"
GLOBAL_MY_SCRIPT_VERSION = "v1.0"

# Check for okta_settings.py config file in cwd.
sys.path.append(os.getcwd())
try:
    from okta_settings import OKTA_CLIENT_TOKEN
    from okta_settings import OKTA_CLIENT_ORGURL


except ImportError:
    # if okta_settings.py file does not exist,
    # Get OKTA_CLIENT_TOKEN from env variable, if it exists.
    if "OKTA_CLIENT_TOKEN" in os.environ:
        OKTA_CLIENT_TOKEN = os.environ.get('OKTA_CLIENT_TOKEN')
    else:
        # not set
        OKTA_CLIENT_TOKEN = None
    if "OKTA_CLIENT_ORGURL" in os.environ:
        OKTA_CLIENT_ORGURL = os.environ.get('OKTA_CLIENT_ORGURL')
    else:
        OKTA_CLIENT_ORGURL = None

# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.

if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

def generate_pw(length):
    digit = ''.join(random.SystemRandom().choice(string.digits) for _ in range(int(length/4)))
    lower = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(int(length/4)))
    upper = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(int(length/4)))
    punct = ''.join(random.SystemRandom().choice(string.punctuation) for _ in range(int(length/4)))
    password = digit+lower+upper+punct
    return password


# take list of users from CSV and create if they don't exist
# to be implemented in the future
# async def create_user(client, user_list):
#     #client = OktaClient(config)
#
#     # parse user_list CSV file
#     # create user without custom attribute
#     body = {
#         "profile": {
#             "firstName": first,
#             "lastName": last,
#             "email": email,
#             "login": email,
#         },
#         "credentials": {
#             "password": {"value": password}
#         }
#     }
#     result = await client.create_user(body)
#     print(result)

async def list_users(client):
    usrs, resp, err = await client.list_users()
    return usrs, resp, err

async def change_password(client, user):
    mypass = generate_pw(12)
    user_creds = {'credentials': {'password': {'value': mypass}}}
    result, response, error = await client.partial_update_user(user, user_creds)
    return result, mypass, response, error

# Start the script.
def go():
    """
    Stub script entry point. Authenticates Okta SDK, and gathers options from command line
    :return: No return
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0} ({1})".format(GLOBAL_MY_SCRIPT_NAME, GLOBAL_MY_SCRIPT_VERSION))

    ####
    #
    # Add custom cmdline argparse arguments here
    #
    ####

    action_group = parser.add_argument_group('Actions', 'User Operations')
    action = action_group.add_mutually_exclusive_group(required=True)
    action.add_argument('--password', '-P', help="Generate New Password for supplied User", default=None)
    # action.add_argument('--new', '-N', help="Create new user(s) from CSV File", default=None)
    action.add_argument('--list', '-L', help="List all users", action='store_true', default=False)

    # Okta login API Login
    okta_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    okta_group.add_argument("--org", "-O",
                                  help="Okta orgUrl, ex. 'https://dev-04352742.okta.com'",
                                  default=None)

    token_group = parser.add_argument_group('Token', 'Specify the OKTA_CLIENT_TOKEN on the Command Line')
    token_group.add_argument("--token", "-T", help="Use this OKTA_CLIENT_TOKEN instead of okta_settings.py ", default=None)

    args = vars(parser.parse_args())

    # Build SDK Constructor
    # config = {
    #     'orgUrl': 'https://dev-04352742.okta.com',
    #     'token': '00yC21cMM-87AFaR5clbeedo01sq12fk8s831rRTe9'
    #       }
    # okta_client = OktaClient(config)

    # check if imported variables exist and no command line override
    if (OKTA_CLIENT_TOKEN and OKTA_CLIENT_ORGURL) and not args['org'] and not args['token']:
        config = {
            'orgUrl': OKTA_CLIENT_ORGURL,
            'token': OKTA_CLIENT_TOKEN
        }
        okta_client = OktaClient(config)

    # use command line args for SDK construction
    if args['org'] and args['token']:
        config = {
        'orgUrl': args['org'],
        'token': args['token']
        }
        okta_client = OktaClient(config)

    # Run list user request
    if args['list']:
        loop = asyncio.get_event_loop()
        usrs, resp, err = loop.run_until_complete(list_users(okta_client))
        if resp.get_status() == 200:
            print("number of users: " + str(len(usrs)))
        else:
            print(err)


    # Generate new password for supplied user
    if args['password']:
        loop = asyncio.get_event_loop()
        result, mypass, resp, err = loop.run_until_complete(change_password(okta_client, args['password']))
        if resp.get_status() == 200:
            print(args['password'] + " New password is: " + mypass)
        else:
            print(err)

# implement later
    # if args['new']:
    #     loop = asyncio.get_event_loop()
    #     resp = loop.run_until_complete(new_user(okta_client, first, last, email, password))

if __name__ == "__main__":
    go()