#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    command script for benten-meta
"""

import argparse
import os

import benten_meta

__author__ = "Takahiro Matsumoto"
__date__ = "2021-03-22"

g_par = {}
g_par["command"] = "benten-meta"
g_par["version"] = "0.0.1"


class ConvertYaml2Json:
    def __init__(self, subparsers, subcommand):

        self.__subcommand = subcommand
        self.__command = "{} {}".format(g_par["command"], subcommand)
        self.set(subparsers)

    def set(self, subparsers):

        sub = subparsers.add_parser(self.__subcommand,
                                    help='see `{} -h`'.format(self.__subcommand))

        sub.add_argument("input_filename", help="input_filename (yml ext.)")
        sub.add_argument("output_filename", help="output_filename (json ext.)")

        sub.set_defaults(handler=self.command)

    def command(self, args):

        benten_meta.log("### {} ###".format(self.__command))

        input_filename  = args.input_filename
        output_filename = args.output_filename

        if os.path.splitext(input_filename)[-1] != ".yml":
            raise benten_meta.Error("input_filename={} required yml extention".format(input_filename))
           
        if os.path.splitext(output_filename)[-1] != ".json":
            raise benten_meta.Error("output_filename={} required json extention".format(input_filename))
        
        
        input_dict = benten_meta.load_yaml(input_filename)
        output_dict = benten_meta.convert_hierarchy2flat(input_dict)

        benten_meta.log("==> convert from {} into {}".format(input_filename, output_filename))
        benten_meta.dump_json(output_dict, output_filename)
        
class ConvertJson2Yaml:
    def __init__(self, subparsers, subcommand):

        self.__subcommand = subcommand
        self.__command = "{} {}".format(g_par["command"], subcommand)
        self.set(subparsers)

    def set(self, subparsers):

        sub = subparsers.add_parser(self.__subcommand,
                                    help='see `{} -h`'.format(self.__subcommand))

        sub.add_argument("input_filename", help="input filename (json ext.)")
        sub.add_argument("output_filename", help="output filename (yml ext)")

        sub.set_defaults(handler=self.command)

    def command(self, args):

        benten_meta.log("### {} ###".format(self.__command))

        input_filename  = args.input_filename
        output_filename = args.output_filename

        if os.path.splitext(input_filename)[-1] != ".json":
            raise benten_meta.Error("input_filename={} required json extention".format(input_filename))
           
        if os.path.splitext(output_filename)[-1] != ".yml":
            raise benten_meta.Error("output_filename={} required yml extention".format(input_filename))
        
        input_dict = benten_meta.load_json(input_filename)
        output_dict = benten_meta.convert_flat2hierarchy(input_dict)

        benten_meta.log("==> convert from {} into {}".format(input_filename, output_filename))
        benten_meta.dump_yaml(output_dict, output_filename)

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog=g_par["command"],description='%s command' % g_par["command"])
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(g_par["version"]))

    subparsers = parser.add_subparsers()
    
    ConvertYaml2Json(subparsers, "convert_yaml2json")
    ConvertJson2Yaml(subparsers, "convert_json2yaml")

    # execute handler
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
    
