# manage-okta-users
Use this script to reset an existing OKTA users password to a new value Or to list out the set of users in the OKTA database

#### Requirements
* Active OKTA Account
* Python >=3.6
* Python modules:
    * OKTA https://github.com/okta/okta-sdk-python
    * AsyncIO

#### License
MIT

#### Installation:
 - Download files to a local directory
 - Copy the okta_settings.py.example file to okta_settings.py 
    - Edit the okta_settings.py file to have an API Token and Org URL
 - Manually run `manage_okta_users.py`. 

### Examples of usage:
Change Password for an existing user:

```
(venv) M-C02FRBGKMD6M:manage_okta_users mkorenbaum$ ./manage_okta_users.py -P mike@alvisofincorp.com
mike@alvisofincorp.com New password is: 083xwgMZO/+:
````

Help Text:

```angular2

$ ./manage_okta_users.py -h
usage: manage_okta_users.py [-h] (--password PASSWORD | --list) [--org ORG] [--token TOKEN]

Manage Alvisofin Demo Portal Users (v1.0)

optional arguments:
  -h, --help            show this help message and exit

Actions:
  User Operations

  --password PASSWORD, -P PASSWORD
                        Generate New Password for supplied User
  --list, -L            List all users

API:
  These options change how this program connects to the API.

  --org ORG, -O ORG     Okta orgUrl, ex. 'https://dev-04352742.okta.com'

Token:
  Specify the OKTA_CLIENT_TOKEN on the Command Line

  --token TOKEN, -T TOKEN
                        Use this OKTA_CLIENT_TOKEN instead of okta_settings.py

```


#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |
