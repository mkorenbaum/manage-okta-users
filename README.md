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
Create a new demo user with a random email to the supplied domain:
```angular2html

(venv) M-C02FRBGKMD6M:manage-okta-users mkorenbaum$ ./manage_okta_users.py -N alvisofincorp.com
New user Successfully Created: demo-8ef53ddf-452b-4607-a3d5-1330d41a642d@alvisofincorp.com  | Initial password: 174lrhIGK!;!

```
Delete a user by email address:
```angular2html

(venv) M-C02FRBGKMD6M:manage-okta-users mkorenbaum$ ./manage_okta_users.py -D 'demo-6160b244-7896-4311-930a-e41233a1d700@alvisofincorp.com'
Successfully deleted user: demo-6160b244-7896-4311-930a-e41233a1d700@alvisofincorp.com

```
Find a user and print their details:
```angular2html
(venv) M-C02FRBGKMD6M:manage-okta-users mkorenbaum$ ./manage_okta_users.py -F 'demo-8ef53ddf-452b-4607-a3d5-1330d41a642d@alvisofincorp.com'
{'embedded': None, 'links': None, 'activated': '2022-07-15T02:50:31.000Z', 'created': '2022-07-15T02:50:31.000Z', 'credentials': {'password': {'hash': None, 'hook': None, 'value': None}, 'provider': {'name': 'OKTA', 'type': <AuthenticationProviderType.OKTA: 'OKTA'>}, 'recovery_question': None}, 'id': '00u5sli77qNRCDGvU5d7', 'last_login': None, 'last_updated': '2022-07-15T02:50:31.000Z', 'password_changed': '2022-07-15T02:50:31.000Z', 'profile': {'city': None, 'costCenter': None, 'countryCode': None, 'department': None, 'displayName': None, 'division': None, 'email': 'demo-8ef53ddf-452b-4607-a3d5-1330d41a642d@alvisofincorp.com', 'employeeNumber': None, 'firstName': 'demo', 'honorificPrefix': None, 'honorificSuffix': None, 'lastName': '8ef53ddf-452b-4607-a3d5-1330d41a642d', 'locale': None, 'login': 'demo-8ef53ddf-452b-4607-a3d5-1330d41a642d@alvisofincorp.com', 'manager': None, 'managerId': None, 'middleName': None, 'mobilePhone': None, 'nickName': None, 'organization': None, 'postalAddress': None, 'preferredLanguage': None, 'primaryPhone': None, 'profileUrl': None, 'secondEmail': None, 'state': None, 'streetAddress': None, 'timezone': None, 'title': None, 'userType': None, 'zipCode': None}, 'status': <UserStatus.ACTIVE: 'ACTIVE'>, 'status_changed': '2022-07-15T02:50:31.000Z', 'transitioning_to_status': None, 'type': {'links': None, 'created': None, 'created_by': None, 'default': None, 'description': None, 'display_name': None, 'id': 'otytb9oa9WGjdGAg25d6', 'last_updated': None, 'last_updated_by': None, 'name': None}}

```

Create a new user in the supplied OKTA domain, and map the hard coded access policy to the provided TSG ID
```angular2html
(venv) M-C02FRBGKMD6M:manage-okta-users mkorenbaum$ ./manage_okta_users.py -A alvisofincorp.com 1151420510

New user Successfully Created: demo-096a0599-d384-4abd-94bb-a907326b0549@alvisofincorp.com | Initial password: 372dwdHRZ$*|
Assigning Access Policy for TSG ID: 1151420510

```
Help Text:

```angular2

(venv) M-C02FRBGKMD6M:manage-okta-users mkorenbaum$ ./manage_okta_users.py -h
usage: manage_okta_users.py [-h] (--password PASSWORD | --delete DELETE | --new NEW | --find FIND) [--org ORG] [--token TOKEN]

Manage Alvisofin Demo Portal Users (v2.0)

optional arguments:
  -h, --help            show this help message and exit

Actions:
  User Operations

  --password PASSWORD, -P PASSWORD
                        Generate New Password for supplied User
  --delete DELETE, -D DELETE
                        Delete Provided User Name
  --new NEW, -N NEW     Create a random new user, provide email domain
  --find FIND, -F FIND  Find a user

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
| **2.0.0** | **b1** | Updated to include add random new user, delete a user, and find user operations. |
| **1.0.0** | **b1** | Initial Release. |
