#!/usr/bin/env python
# -*- coding: utf-8 -*-


def merge_dicts(dictionaries):
    """
    merges all the dictionaries in a list into one.
    :param dictionaries:
    :return:
    """
    result = {}
    for dictionary in dictionaries:
        result.update(dictionary)
    return result


def get_allowed_actions(action_parameters):
    """
    gets the name of each action and creates a list of them
    which is later used as an whitelist of actions.
    :param action_parameters:
    :return:
    """
    return [action_parameters[action_name]['action'] for action_name in action_parameters]