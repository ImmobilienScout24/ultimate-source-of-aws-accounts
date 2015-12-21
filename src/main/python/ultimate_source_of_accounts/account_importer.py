# -*- coding: utf-8 -*-
"""Read yaml files with AWS account information and run a consistency check"""

from __future__ import print_function, absolute_import, division

import yamlreader
import logging
import six


def read_directory(yaml_path):
    """Read yaml files and return merged yaml data"""
    accounts = yamlreader.yaml_load(yaml_path)

    for account in accounts.values():
        account['id'] = str(account['id'])
    _check_account_data(accounts)

    logging.debug("Read yaml files from directory '%s'", yaml_path)

    return accounts


def _check_account_data(accounts):
    """Raise exception if account data looks wrong, otherwise return True"""
    if not accounts:
        raise Exception("Account data is empty.")

    all_account_ids = set()
    for account_name, account_data in accounts.items():
        account_id = account_data.get("id")
        if account_id in all_account_ids:
            raise Exception("duplicated id {0} found".format(account_id))
        all_account_ids.add(account_id)
        if not account_data.get("email"):
            raise Exception("Account data {0} has no email.".format(account_name))
        if "@" not in account_data.get("email"):
            raise Exception("Account data {0} without @ in email.".format(account_name))
        if not account_id:
            raise Exception("Account data {0} has no account id.".format(account_name))
        if 'owner' not in account_data:
            raise Exception("Account {0} has no 'owner' field".format(account_name))
        owner = account_data['owner']
        if not isinstance(owner, six.string_types):
            raise Exception("'owner' field of account {0} is not a string".format(account_data))
        if owner == "":
            raise Exception("'owner' field of account {0} is empty".format(account_data))
