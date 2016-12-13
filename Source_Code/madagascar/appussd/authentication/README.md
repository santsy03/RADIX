# User Management and Authentication Service #

This app handles user management and authentication.

### Who can use this? ###

* Any application that needs user / password authentication requirements
* An API that needs to authenticate clients


### Features and APIs exposed ###

* authenticate ( using username / password )
* authenticate ( using authentication key )
* change password
* unlock locked user account
* reset user account
* create new user account

* get allowed packages for API user
* get allowed services for API user


### Requirements ###

* memcache >= 1.5
* utilities module
```
#!python

from utilities.logging.core import log
from utilities.secure.core import decrypt, encrypt, salt
from utilities.memcache.core import MemcacheHandler
from utilities.db.core import execute_query, call_stored_procedure
```
* central config in configs/config.py  . Sample below:

```
#!python

databases = {
            'core':{
                    'username': '551f5023',
                    'password': '551f5023',
                    'string': '192.168.1.51:1521/xe'
            }
        }

kannel = {
        'username':'5511461d5c',
        'password':'5511461d5c',
        'url':'http://127.0.0.1:14020/cgi-bin/sendsms?username=%s&password=%s&'
        }

MEMCACHE = {}
MEMCACHE['host'] = '192.168.1.95:11211'
MEMCACHE['retention_period'] = 86400   #seconds
```


### Set up ###

* edit HOME variable on authentication/configs/\_\_init\_\_.py  -  point to application home directory
* create log location directories:  
```
#!bash

mkdir -p authentication/logs/cdr
```
* start service on authentication/http:  
```
#!bash

twistd -y site-auth-http.py
```

### Usage examples ###

* authenticate user
```
#!bash

curl "http://127.0.0.1:8006/authenticate?username=test_user&password=1234&channel=radix"
```

* unlock user account  
```
#!bash

curl "http://127.0.0.1:8006/unlock?username=test_user&channel=radix"
```


* create API user

```
#!bash

curl "http://127.0.0.1:8006/create_api_user?username=foo&channel=radix"
```

* assign packages to API user  
```
#!bash

curl "http://127.0.0.1:8006/assign_user_packages?username=foo&packages=1,2,3&action=add"
```

* assign services to API user  
```
#!bash

curl "http://127.0.0.1:8006/assign_user_services?username=foo&services=3,4,5&action=add"
```


### Response Status Codes ###


```
#!python

STATUS = {}
# Status code : definition mapping
STATUS['no_user'] = '1'
STATUS['auth_success'] = '0'
STATUS['auth_fail'] = '2'
STATUS['error'] = '3'
STATUS['user_created'] = '4'
STATUS['user_create_fail'] = '6'
STATUS['password_change_success'] = '7'
STATUS['password_change_fail'] = {}
STATUS['password_change_fail']['auth_fail'] = '8'
STATUS['password_change_fail']['create_user_fail'] = '9'
STATUS['account_locked'] = '10'
STATUS['password_reset_success'] = '11'
STATUS['password_reset_fail'] = '12'
STATUS['unlock_success'] = '13'
STATUS['unlock_fail'] = '14'
STATUS['update_list_successful'] = '15'
STATUS['incorrect_parameters'] = '16'
STATUS['update_list_fail'] = '17'
```