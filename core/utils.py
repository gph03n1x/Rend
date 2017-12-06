#!/usr/bin/env python
# -*- coding: utf-8 -*-


def merge_dicts(dictionaries):
    result = {}
    for dictionary in dictionaries:
        result.update(dictionary)
    return result


def get_allowed_actions(action_parameters):
    return [action_parameters[action_name]['action'] for action_name in action_parameters]