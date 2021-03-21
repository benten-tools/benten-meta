# -*- coding: utf-8 -*-
"""
benten tool for metadata
This provides the function of metadata treatment for BENTEN 
"""
import re
import json
import yaml
import codecs
import collections
from logging import getLogger, StreamHandler, DEBUG

__copyright__    = 'Copyright (C) 2021 Takahiro Matsumoto'
__version__      = '0.0.1'
__license__      = 'Apache License 2.0'
__author__       = 'Takahiro Matsumoto'
__author_email__ = 'matumot@spring8.or.jp'
__url__          = 'https://github.com/benten-tools/benten-meta'

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def log(message, level="DEBUG", flush=False):
    """
    log output using logger

    :param message: message for the log
    :param level: log output level, default is "DEBGU"
    :param flush: option for log flush, default is False
    """
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)

    if flush:
        logger.handlers[0].flush()

class Error(BaseException):
    def __init__(self, message, flag_print=True):
        self.__message = message

        if flag_print:
            log(" ==> benten_meta.Error()", "ERROR")
            log("     message = {}".format(self.__message), "ERROR")

    def message(self):
        return self.__message

def load_json(filename):
    """
    load json file and return dict, order in the file is reserved

    :param: filename: input filename
    """

    ret_dict = collections.OrderedDict()
    with codecs.open(filename, "r", "utf-8") as f:
        ret_dict = json.load(f, object_pairs_hook=collections.OrderedDict)
    return ret_dict

def load_yaml(filename):
    """
    load yaml file and return dict, order in the file is reserved

    :param filename: input filename
    """
    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                         lambda loader, node: collections.OrderedDict(loader.construct_pairs(node)))

    vdict = collections.OrderedDict()
    with codecs.open(filename, "r", "utf-8") as f:
        vdict = yaml.load(f, Loader=yaml.SafeLoader)
    return vdict

def dump_json(out_dict, filename, debug=False):
    """
    dump dict into  json file

    :param out_dict: dict for output
    :param filename: output filename (json)
    :param debug: debug option, default is False
    """
    
    if debug:
        if filename is not None:
            log("--> filename = {}".format(filename))
        log(json.dumps(out_dict, indent=4,
                         separators=(',', ':'), ensure_ascii=False))

    with codecs.open(filename, "w", "utf-8") as f:
        json.dump(out_dict, f, indent=4, separators=(
                ',', ':'), ensure_ascii=False)

def dump_yaml(out_dict, filename, debug=False):
    """
    dump dict into yaml file

    :param out_dict: dict for output
    :param filename: output filename (yaml)
    :param debug: debut option, default is False
    """
    
    def represent_odict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    yaml.add_representer(collections.OrderedDict, represent_odict)

    if debug:
        if filename is not None:
            log("--> filename = {}".format(filename))
        log(json.dumps(out_dict, indent=4,
                         separators=(',', ':'), ensure_ascii=False))
    
    if filename is not None:
        with codecs.open(filename, "w", "utf-8") as f:
            yaml.dump(out_dict, f, encoding="utf-8",
                      allow_unicode=True, default_flow_style=False)


def convert_hierarchy2flat(vmeta_dict, exclude_local=False, flag_top=True):
    """
    convert metadata dict in hiearchy style and retrun metadata dict in flat key style

    :param vmeta_dict: metadata dict for input (hiearchy style)
    :param exclude_local: option to output local metadata, default is False
    :param flag_top: option to specify if return metadata is started from "@", default is True
    """

    class ConvertMetadata:
        def __init__(self):
            self.__metadata_flat =  collections.OrderedDict()

        def metadata_flat(self):
            return self.__metadata_flat

        def set_metadata_hiearachy_value(self, key, val):
            v_check_unit = re.search("\[.*\]$", key)
            if v_check_unit is not None:
                v_unit_all = v_check_unit.group()
                v_unit = v_unit_all[1:-1]
                key_base = key[:-len(v_unit_all)]
                self.__metadata_flat[key_base] = val
                key_unit = key_base  + "_unit"
                self.__metadata_flat[key_unit] = v_unit
            else:
                self.__metadata_flat[key] = val
            
        def set_metadata_hiearachy(self, vdict, key=None, flag_top=False):
            if type(vdict) not in [collections.OrderedDict, dict]:
                return
            
            for key_sub in vdict:
                if flag_top and exclude_local and key_sub.find("local") == 0:
                    continue

                key_flat = None
                if key is None:
                    key_flat = key_sub
                else:
                    key_flat = "{}@{}".format(key,key_sub)
                if flag_top:
                    key_flat = "@" + key_sub
                val = vdict[key_sub]
                
                if type(val) in [collections.OrderedDict, dict]:
                    self.set_metadata_hiearachy(val, key=key_flat)
                elif type(val) in [list]:
                    vlist_mod = []
                    for v_each in val:
                        m = ConvertMetadata()
                        m.set_metadata_hiearachy(v_each,flag_top=False)
                        v_each_mod = m.metadata_flat()
                        if type(v_each) in [collections.OrderedDict, dict]:
                            vlist_mod.append(v_each_mod)
                        else:
                            vlist_mod.append(v_each)
                    self.__metadata_flat[key_flat] = vlist_mod
                else:
                    self.set_metadata_hiearachy_value(key_flat, val)    

    conv = ConvertMetadata()
    conv.set_metadata_hiearachy(vmeta_dict, flag_top=flag_top)

    return conv.metadata_flat()
    
def convert_flat2hierarchy(vmeta_dict, exclude_local=False, flag_top=True):
    """
    convert metadata dict in flat key style and retrun metadata dict in hiearchy style

    :param vmeta_dict: metadata dict for input (hiearchy style)
    :param exclude_local: option to exclude output local metadata, default is False
    :param flag_top: option to specify if input metadata is started from "@", default is True
    """

    vh = collections.OrderedDict()

    vmeta_h = collections.OrderedDict()

    for key in vmeta_dict:
        if flag_top and exclude_local and key.find("@local") == 0:
            continue
            
        key_mod = key

        key_mod_split = []
        if flag_top:
            key_mod_split = key_mod.split("@")[1:]
        else:
            key_mod_split = key_mod.split("@")
        
        vmeta_tmp = vmeta_h
        count_max = len(key_mod_split)
        for count in range(count_max):
            key_sub = key_mod_split[count]
            if key_sub not in vmeta_tmp:
                vmeta_tmp[key_sub] = collections.OrderedDict()
            if count == count_max -1:
                val = vmeta_dict[key]
                if type(val) not in [list]:
                    vmeta_tmp[key_sub] = val
                else:
                    v_list = []
                    for v_each in val:
                        if type(v_each) in [collections.OrderedDict, dict]:
                            v_list.append(convert_flat2hierarchy(v_each, flag_top=False))
                        else:
                            v_list.append(v_each)
                    vmeta_tmp[key_sub] =  v_list
            vmeta_tmp = vmeta_tmp[key_sub]

    # move local meta to last
    vmeta_h_local = vmeta_h.get("local")
    if vmeta_h_local:
        del vmeta_h["local"]
        vmeta_h["local"] = vmeta_h_local

    return vmeta_h
