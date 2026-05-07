# Config

## Server config:
The main configuration is just an `eneverre.ini` file and another ini file for each camera definition.  Look at the [examples](/doc/example), it's quite easy.

## User management:
By default, it creates an administrator user named `Admin` with the password `enverre`.
Then, the user management is done via the command line using the [manage_users.py](/cmd/manage_users.py) script.

``` bash
$ ./manage_users.py 
usage: manage_users.py [-h] {list,create,passwd,role,delete} ...

Manage users

positional arguments:
  {list,create,passwd,role,delete}

options:
  -h, --help            show this help message and exit

```
