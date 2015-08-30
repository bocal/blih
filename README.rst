BLIH - Bocal Lightweight Interface for Humans
=============================================

|build-status|

Script for using the bocal api (BLIH).

Usage::

 usage: blih [-h] [-u USER] [-t TOKEN] [-v] {repository,sshkey} ...
 
 positional arguments:
   {repository,sshkey}   The main command
     repository          Manage your repository
     sshkey              Manage your sshkey
 
 optional arguments:
   -h, --help            show this help message and exit
   -u USER, --user USER  The user
   -t TOKEN, --token TOKEN
                         Specify the token on the command line
   -v, --verbose         Increase the verbosity level

Repository ::

 usage: blih repository [-h] {create,delete,info,list,getacl,setacl} ...
 
 positional arguments:
    {create,delete,info,list,getacl,setacl}
                        The subcommand
     create              Create a repository
     delete              Delete a repository
     info                Get information about a repository
     list                Get the list of your repositories
     getacl              Manage repository acls
     setacl              Get repository acls
 
 optional arguments:
   -h, --help            show this help message and exit

SSHKey ::

 usage: blih sshkey [-h] {upload,list,delete} ...
 
 positional arguments:
   {upload,list,delete}  The sshkey subcommand
     upload              Upload a new sshkey
     list                List your sshkey(s)
     delete              Delete a sshkey
 
 optional arguments:
   -h, --help            show this help message and exit


.. |build-status| image:: https://circleci.com/gh/bocal/blih.svg?&style=shield
   :target: https://circleci.com/gh/bocal/blih
