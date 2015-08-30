#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from __future__ import print_function

import sys
import os

from argparse import ArgumentParser
import getpass

__version__ = '2.0'

USER_AGENT = 'blih-' + __version__
API_VERSION = '2.0'
URL = 'https://blih.epitech.eu/' + API_VERSION

class BlihError(Exception):
    """
    Base exception class
    """
    pass

def blih(method, resource, auth, data=None):
    """
    Wrapper around requests
    """
    try:
        import requests
    except ImportError:
        raise
    try:
        requests_method = getattr(requests, method)
        req = requests_method(
            URL + resource,
            auth=auth,
            headers={'User-Agent' : USER_AGENT},
            data=data
        )
        if req.status_code != 204:
            data = req.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise BlihError('Can\'t connect to {0}'.format(URL))
    except requests.exceptions.HTTPError:
        raise BlihError('An HTTP Error occured')
    except ValueError:
        raise BlihError('Unknown Error')

    if req.status_code in [400, 401, 403, 404, 405, 409]:
        raise BlihError(data['message'])

    return data

# pylint: disable=unused-argument
def repository_create(user, password, name, **kwargs):
    """
    Create a repository
    """
    data = blih(
        'post',
        '/repositories',
        (user, password),
        data={'name' : name, 'type' : 'git'}
    )

    return {data : data}

# pylint: disable=unused-argument
def repository_delete(user, password, name, **kwargs):
    """
    Delete a repository
    """
    data = blih(
        'delete',
        '/repository/' + name,
        (user, password)
    )

    return {data : data}

# pylint: disable=unused-argument
def repository_info(user, password, name, **kwargs):
    """
    Get some info about a repository
    """
    data = blih(
        'get',
        '/repository/' + name,
        (user, password)
    )

    return {data : data}

# pylint: disable=unused-argument
def repository_list(user, password, **kwargs):
    """
    List the users repositories
    """
    data = blih(
        'get',
        '/repositories',
        (user, password)
    )

    return {data : data}

# pylint: disable=unused-argument
def repository_getacl(user, password, name, **kwargs):
    """
    Get the defined acls for one repo
    """
    data = blih(
        'get',
        '/repository/' + name + '/acls',
        (user, password)
    )

    return {data : data}

# pylint: disable=unused-argument
def repository_setacl(user, password, name, user_acl, acl, **kwargs):
    """
    Set some acls on one repository
    """
    data = blih(
        'post',
        '/repository/' + name + '/acls',
        (user, password),
        data={'user' : user_acl, 'acl' : acl}
    )

    return {data : data}

# pylint: disable=unused-argument
def sshkey_upload(user, password, keyfile, **kwargs):
    """
    Upload a new sshkey
    """
    try:
        handle = open(keyfile, 'r')
    except (OSError, IOError):
        raise BlihError('File {0} not found'.format(keyfile))

    keydata = handle.read().strip('\n')
    handle.close()

    try:
        keytype, key, comment = keydata.split(' ')
    except ValueError:
        raise

    data = blih(
        'post',
        '/sshkeys',
        (user, password),
        data={'key' : keytype + ' ' + key, 'comment' : comment}
    )

    return {'data' : data,
            'format' : '{key} {comment}'}

# pylint: disable=unused-argument
def sshkey_list(user, password, **kwargs):
    """
    List the sshkeys
    """
    data = blih(
        'get',
        '/sshkeys',
        (user, password)
    )

    return {'data' : data,
            'format' : '{key} {comment}'}

# pylint: disable=unused-argument
def sshkey_get(user, password, comment, **kwargs):
    """
    Get a sshkey
    """
    data = blih(
        'get',
        '/sshkeys/' + comment,
        (user, password)
    )

    return {'data' : data,
            'format' : '{key} {comment}'}

# pylint: disable=unused-argument
def sshkey_delete(user, password, comment, **kwargs):
    """
    Delete a sshkey
    """
    data = blih(
        'delete',
        '/sshkeys/' + comment,
        (user, password)
    )

    return {'data' : data,
            'format' : ''}

#pylint: disable=R0914,too-many-statements
def main():
    """
    Main entry point
    """

    parser = ArgumentParser()
    parser.add_argument(
        '-u', '--user',
        help='The user',
        default=os.environ.get('BLIH_USER', getpass.getuser())
    )
    parser.add_argument(
        '-t', '--password',
        help='Specify the password on the command line',
        default=os.environ.get('BLIH_PASSWORD', None)
    )

    subparser = parser.add_subparsers(dest='command', help='The main command')
    subparser.required = True

    # Create the subparser for the repository argument
    parser_repository = subparser.add_parser(
        'repository',
        help='Manage your repository'
    )
    subparser_repository = parser_repository.add_subparsers(
        dest='subcommand',
        help='The subcommand'
    )
    subparser_repository.required = True

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
    subparser_sshkey = parser_sshkey.add_subparsers(
        dest='subcommand',
        help='The sshkey subcommand'
    )
    subparser_sshkey.required = True

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

    parser_sshkey_get = subparser_sshkey.add_parser(
        'get',
        help='Get a sshkey'
    )
    parser_sshkey_get.add_argument('comment', help='The sshkey comment')
    parser_sshkey_get.set_defaults(func=sshkey_get)

    parser_sshkey_delete = subparser_sshkey.add_parser(
        'delete',
        help='Delete a sshkey'
    )
    parser_sshkey_delete.add_argument('comment', help='The comment of the sshkey file to delete')
    parser_sshkey_delete.set_defaults(func=sshkey_delete)

    argument = parser.parse_args()

    if argument.password == None:
        try:
            argument.password = getpass.getpass()
        except KeyboardInterrupt:
            sys.exit(1)

    try:
        ret = argument.func(**vars(argument))
    except BlihError as err:
        print('Error: {0}'.format(err))
        sys.exit(1)

    if ret['data']:
        if isinstance(ret['data'], list):
            for item in ret['data']:
                print(ret['format'].format(**item))
        elif isinstance(ret['data'], dict):
            print(ret['format'].format(**ret['data']))
