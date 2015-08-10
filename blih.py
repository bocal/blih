#!/usr/bin/env python3

#-
# Copyright 2013-2015 Emmanuel Vadot <elbarto@bocal.org>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Bocal Lightweight Interface for Humans
"""

import sys
import os

from argparse import ArgumentParser
import hmac
import hashlib
import requests
import json
import getpass
import urllib

VERSION = 1.7
USER_AGENT = 'blih-' + str(VERSION)
URL = 'https://blih.epitech.eu'

def sign_data(user, token, data=None):
    """
    Calculate the signature
    """
    if token == None:
        token = hashlib.sha512(bytes(getpass.getpass(), 'utf8')).hexdigest()
    signature = hmac.new(bytes(token, 'utf8'), msg=bytes(user, 'utf8'), digestmod=hashlib.sha512)
    signed_data = {}

    if data:
        json_data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        signature.update(bytes(json_data, 'utf8'))
        signed_data['data'] = data

    signed_data['user'] = user
    signed_data['signature'] = signature.hexdigest()

    return signed_data

def blih_get(resource, user, token, data):
    """
    Wrapper around requests.get
    """
    try:
        req = requests.get(
            URL + resource,
            headers={'User-Agent' : USER_AGENT, 'Content-Type' : 'application/json'},
            data=json.dumps(sign_data(user, token, data=data))
        )
        data = req.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print('Can\'t connect to ', URL)
        sys.exit(1)
    except requests.exceptions.HTTPError:
        print('An HTTP Error occured')
        sys.exit(1)

    if req.status_code != 200:
        try:
            print(data['error'])
        except KeyError:
            print('Unknown error')
        sys.exit(1)

    return data

def blih_post(resource, user, token, data):
    """
    Wrapper around requests.post
    """
    try:
        req = requests.post(
            URL + resource,
            headers={'User-Agent' : USER_AGENT, 'Content-Type' : 'application/json'},
            data=json.dumps(sign_data(
                user,
                token,
                data=data
            ))
        )
        data = req.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print('Can\'t connect to ', URL)
        sys.exit(1)
    except requests.exceptions.HTTPError:
        print('An HTTP Error occured')
        sys.exit(1)

    if req.status_code != 200:
        try:
            print(data['error'])
        except KeyError:
            print('Unknown error')
        sys.exit(1)

    return data

def blih_delete(resource, user, token, data):
    """
    Wrapper around requests.post
    """
    try:
        req = requests.delete(
            URL + resource,
            headers={'User-Agent' : USER_AGENT, 'Content-Type' : 'application/json'},
            data=json.dumps(sign_data(
                user,
                token,
                data=data
            ))
        )
        data = req.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print('Can\'t connect to ', URL)
        sys.exit(1)
    except requests.exceptions.HTTPError:
        print('An HTTP Error occured')
        sys.exit(1)

    if req.status_code != 200:
        try:
            print(data['error'])
        except KeyError:
            print('Unknown error')
        sys.exit(1)

    return data

def repository_create(args):
    """
    Create a repository
    """
    data = blih_post(
        '/repositories',
        args.user,
        args.token,
        {'name' : args.name, 'type' : 'git'}
    )

    if data['message']:
        print(data['message'])


def repository_delete(args):
    """
    Delete a repository
    """
    data = blih_delete(
        '/repository/' + args.name,
        args.user,
        args.token,
        None
    )

    if data['message']:
        print(data['message'])

def repository_info(args):
    """
    Get some info about a repository
    """
    data = blih_get(
        '/repository/' + args.name,
        args.user,
        args.token,
        None
    )

    for key, value in data['message'].items():
        print(key, ':', value)

def repository_list(args):
    """
    List the users repositories
    """
    data = blih_get(
        '/repositories',
        args.user,
        args.token,
        None
    )

    for repo in data['repositories']:
        print(repo)

def repository_getacl(args):
    """
    Get the defined acls for one repo
    """
    data = blih_get(
        '/repository/' + args.name + '/acls',
        args.user,
        args.token,
        None
    )

    for key, value in data.items():
        print(key, ':', value)

def repository_setacl(args):
    """
    Set some acls on one repository
    """
    print('repository setacl ' + str(args))
    data = blih_post(
        '/repository/' + args.name + '/acls',
        args.user,
        args.token,
        data={'user' : args.user_acl, 'acl' : args.acl}
    )

    if data['message']:
        print(data['message'])

def sshkey_upload(args):
    """
    Upload a new sshkey
    """
    try:
        handle = open(args.keyfile, 'r')
    except (PermissionError, FileNotFoundError):
        print("Can't open file : " + args.keyfile)
        sys.exit(1)
    key = urllib.parse.quote(handle.read().strip('\n'))
    handle.close()
    data = blih_post(
        '/sshkeys',
        args.user,
        args.token,
        {'sshkey' : key}
    )

    if data['message']:
        print(data['message'])

def sshkey_list(args):
    """
    List the sshkeys
    """
    data = blih_get(
        '/sshkeys',
        args.user,
        args.token,
        None
    )

    for comment, key in data.items():
        print(key, comment)

def sshkey_delete(args):
    """
    Delete a sshkey
    """
    data = blih_delete(
        '/sshkey/' + args.comment,
        args.user,
        args.token,
        None
    )

    if data['message']:
        print(data['message'])

#pylint: disable=R0914
def main():
    """
    Main entry point
    """

    parser = ArgumentParser()
    parser.add_argument(
        '-u', '--user',
        help='The user',
        default=getpass.getuser()
    )
    parser.add_argument(
        '-t', '--token',
        help='Specify the token on the command line',
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Increase the verbosity level',
        action='store_true'
    )

    subparser = parser.add_subparsers(help='The main command')

    # Create the subparser for the repository argument
    parser_repository = subparser.add_parser(
        'repository',
        help='Manage your repository'
    )
    subparser_repository = parser_repository.add_subparsers()

    # Create the subparser for the repository create command
    parser_repo_create = subparser_repository.add_parser(
        'create',
        help='Create a repository'
    )
    parser_repo_create.add_argument('name', help='The repository name')
    parser_repo_create.set_defaults(func=repository_create)

    parser_repo_delete = subparser_repository.add_parser(
        'delete',
        help='Delete a repository'
    )
    parser_repo_delete.add_argument('name', help='The repository name')
    parser_repo_delete.set_defaults(func=repository_delete)

    parser_repo_info = subparser_repository.add_parser(
        'info',
        help='Get information about a repository'
    )
    parser_repo_info.add_argument('name', help='The repository name')
    parser_repo_info.set_defaults(func=repository_info)

    parser_repo_list = subparser_repository.add_parser(
        'list',
        help='Get the list of your repositories'
    )
    parser_repo_list.set_defaults(func=repository_list)

    parser_repo_getacl = subparser_repository.add_parser(
        'getacl',
        help='Manage repository acls'
    )
    parser_repo_getacl.add_argument('name', help='The repository name')
    parser_repo_getacl.set_defaults(func=repository_getacl)

    parser_repo_setacl = subparser_repository.add_parser(
        'setacl',
        help='Get repository acls'
    )
    parser_repo_setacl.add_argument('name', help='The repository name')
    parser_repo_setacl.add_argument('user_acl', help='The user to apply acls to')
    parser_repo_setacl.add_argument('acl', help='The acl (r or w)')
    parser_repo_setacl.set_defaults(func=repository_setacl)

    parser_sshkey = subparser.add_parser(
        'sshkey',
        help='Manage your sshkey'
    )
    subparser_sshkey = parser_sshkey.add_subparsers()

    parser_sshkey_upload = subparser_sshkey.add_parser(
        'upload',
        help='Upload a new sshkey'
    )
    parser_sshkey_upload.add_argument(
        'keyfile',
        help='The sshkey file to upload',
        nargs='?',
        default=os.getenv('HOME') + '/.ssh/id_rsa.pub'
    )
    parser_sshkey_upload.set_defaults(func=sshkey_upload)

    parser_sshkey_list = subparser_sshkey.add_parser(
        'list',
        help='List your sshkey(s)'
    )
    parser_sshkey_list.set_defaults(func=sshkey_list)

    parser_sshkey_delete = subparser_sshkey.add_parser(
        'delete',
        help='Delete a sshkey'
    )
    parser_sshkey_delete.add_argument('comment', help='The comment of the sshkey file to delete')
    parser_sshkey_delete.set_defaults(func=sshkey_delete)

    argument = parser.parse_args()
    argument.func(argument)

if __name__ == "__main__":
    main()
