#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A wrapper of config
"""
import ConfigParser
import os


__all__ = ['get_config']
__config = None


def abs_dir(fname):
    """ get absolute path of config file name.
    args:
        fname: config file name in conf path.
    return:
        abs_fname: absolute path of config file name `fname`.
    """
    abs_fname = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '../../conf',
        fname,
    )
    return abs_fname


def get_config(**kwargs):
    """Get a config instance.

    Args:
        config_file: config file. default is server.cfg

    Returns:
        return a ConfigParser object.
    """
    global __config

    if __config is None:
        config = ConfigParser.ConfigParser()
        # the path is `conf` dir under root dir.
        bs_config_file = kwargs.get('bs_config', 'bs.cfg')
        update_config_file = kwargs.get('update_config', 'update.cfg')
        config_files = [
            abs_dir(bs_config_file),
            abs_dir(update_config_file),
        ]
        config.read(config_files)

    return config

