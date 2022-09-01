#!/usr/bin/env python3
"""
Alvisofin Okta Users Management
mkorenbaum@paloaltonetworks.com
Version: 2.0.0 b1
"""
from okta.client import Client as OktaClient
import asyncio
import os
import sys
import argparse
import uuid
import random
import string
import uuid
import prisma_sase

GLOBAL_MY_SCRIPT_NAME = "Manage Alvisofin Demo Portal Users"
GLOBAL_MY_SCRIPT_VERSION = "v2.0"

# Check for okta_settings.py config file in cwd.
sys.path.append(os.getcwd())
try:
    from okta_settings import OKTA_CLIENT_TOKEN
    from okta_settings import OKTA_CLIENT_ORGURL
    from okta_settings import CLIENT_ID
    from okta_settings import SECRET
    from okta_settings import TSG

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
    if "CLIENT_ID" in os.environ:
        CLIENT_ID = os.environ.get('CLIENT_ID')
    else:
        CLIENT_ID = None
    if "SECRET" in os.environ:
        SECRET = os.environ.get('SECRET')
    else:
        SECRET = None
    if "TSG" in os.environ:
        TSG = os.environ.get('TSG')
    else:
        TSG = None
# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.

if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes

def generate_pw(length):
    chars = "!@#$%^&*()"
    digit = ''.join(random.SystemRandom().choice(string.digits) for _ in range(int(length/4)))
    lower = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(int(length/4)))
    upper = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(int(length/4)))
    punct = ''.join(random.choice(chars) for _ in range(int(length/4)))
    password = digit+lower+upper+punct
    return password



# Create a user
async def create_user(client, unique_user, email):
    # create user without custom attribute

    pw = generate_pw(12)

    body = {
        "profile": {
            "firstName": 'demo',
            "lastName": unique_user,
            "email": 'demo-'+unique_user+'@'+email,
            "login": 'demo-'+unique_user+'@'+email,
        },
        "credentials": {
            "password": {"value": pw}
        }
    }
    result, response, error = await client.create_user(body)
    return result, pw, response, error

# delete provided user
async def delete_user(client, user):
    resp, err = await client.deactivate_or_delete_user(user)
    return resp, err

async def get_user(client,user):
    user, resp, err = await client.get_user(user)
    return user, resp, err

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
    action.add_argument('--delete', '-D', help="Delete Provided User Name", default=None)
    action.add_argument('--new', '-N', help="Create a random new user, provide email domain", default=None)
    action.add_argument('--find', '-F', help="Find a user", default=None)
    action.add_argument('--add', '-A', nargs='+', help=" Create new user on Okta provided domain, and Add Access Policy to provided TSG ID ", default=None)

    # Okta login API Login
    okta_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    okta_group.add_argument("--org", "-O",
                                  help="Okta orgUrl, ex. 'https://dev-04352742.okta.com'",
                                  default=None)

    token_group = parser.add_argument_group('Token', 'Specify the OKTA_CLIENT_TOKEN on the Command Line')
    token_group.add_argument("--token", "-T", help="Use this OKTA_CLIENT_TOKEN instead of okta_settings.py ", default=None)

    args = vars(parser.parse_args())

    # Build SDK Constructor

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

    # Run find user request
    if args['find']:
        loop = asyncio.get_event_loop()
        user, resp, err = loop.run_until_complete(get_user(okta_client,args['find']))
        if resp.get_status() == 200:
            print(user)
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

    # Create a random new user for supplied domain
    if args['new']:

        # generate unique id
        unique_user = str(uuid.uuid4())

        # validate this user does not exist generate new if required
        email = 'demo-'+unique_user+'@'+args['new']
        loop = asyncio.get_event_loop()
        user, resp, err = loop.run_until_complete(get_user(okta_client, email))
        if resp.get_status() == 404:
            # create user
            loop = asyncio.get_event_loop()
            result, pw, resp, err = loop.run_until_complete(create_user(okta_client, unique_user, args['new']))
            if resp.get_status() == 200:
                print( "New user Successfully Created: demo-"+unique_user+"@"+args['new']+"  | Initial password: "+pw)
            else:
                print(err)
        else:
            print("Unlikely UUID Collision Try running again")

    # Create a random new user for supplied domain AND assign demo user access policy to provided TSG ID
    if args['add']:

        n = len(args['add'])
        if (n != 2):
            print("Too few arguments provided, need to provide OKTA domain and TSG ID /n "
                  "Example: python3 manage_okta_users.py -A alvisofincorp.com 1530391577")
        else:
            # generate unique id
            unique_user = str(uuid.uuid4())

            # validate this user does not exist generate new if required
            email = 'demo-' + unique_user + '@' + args['add'][0]
            loop = asyncio.get_event_loop()
            user, resp, err = loop.run_until_complete(get_user(okta_client, email))
            if resp.get_status() == 404:
                # create user
                loop = asyncio.get_event_loop()
                result, pw, resp, err = loop.run_until_complete(create_user(okta_client, unique_user, args['add'][0]))
                if resp.get_status() == 200:
                    new_user = "demo-" + unique_user + "@" + args['add'][0]
                    user_tsg = args['add'][1]
                    print("New user Successfully Created: "+ new_user + " | Initial password: " + pw)
                    print("Assigning Access Policy for TSG ID: "+ user_tsg)

                    #initialize SASE SDK  --
                    client_id = CLIENT_ID
                    secret = SECRET
                    tsg = TSG
                    sdk = prisma_sase.API(ssl_verify=False)
                    sdk.interactive.login_secret(client_id=client_id, client_secret=secret, tsg_id=tsg)

                    # TODO create function to assign permissions to user

                    # Template for access policy
                    prn = "prn:"+user_tsg+"::::".format(tsg)
                    user_email = new_user
                    role = "superuser"

                    data = {
                        "role": role,
                        "principal": user_email,
                        "resource": prn
                    }
                    url = "https://api.sase.paloaltonetworks.com/iam/v1/access_policies"
                    resp = sdk.rest_call(url=url, data=data, method="POST")
                    print(resp.cgx_content)
                else:
                    print(err)
            else:
                print("Unlikely UUID Collision Try running again")


    if args['delete']:
        loop = asyncio.get_event_loop()
        resp, err = loop.run_until_complete(delete_user(okta_client, args['delete']))
        if resp.get_status() == 204:
            loop = asyncio.get_event_loop()
            resp2, err = loop.run_until_complete(delete_user(okta_client, args['delete']))
            if resp2.get_status() == 204:
                print("Successfully deleted user: "+args['delete'])
        else:
            print(err)


if __name__ == "__main__":
    go()