#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
from xmlrpclib import ServerProxy
import sys
import logging
import os
import molsys
import getpass
from decorator import faulthandler, download

logger = logging.getLogger("mofplus")
logger.setLevel(logging.DEBUG)
shandler = logging.StreamHandler()
shandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m-%d %H:%M')
shandler.setFormatter(formatter)
logger.addHandler(shandler)


class user_api(object):
    """
    Via the user_api class the API routines of MOFplus which are accessable for normal users can be used.
    The credentials can be set either as environment variables MFPUSER and MFPPW or can be given interactively.

    :Attrributes[MaÈ[MaÇ[MaÇ:
        - mfp (obj)     : ServerProxy XMLRPCLIB object holding the connection to MOF+
        - username (str): Username on MOF+
        - pw (str)      : Pa[MaÇ[MaÇssword corresponding to the username

    :Args:
        - experimental (bool, option[MaÆal): Use to connect to experimental DB, defaults to False
        - banner       (bool, optional): If True, the MFP API banner is printed to SDTOUT, defaults to False
    """

    def __init__(self,experimental=False, banner = False):
        if banner: self.print_banner()
        try:
            self.username = os.environ['MFPUSER']
            self.pw       = os.environ['MFPPW']
        except KeyError:
            logger.error("Credentials not found!")
            self.username, self.pw = self.credentials_from_cmd()
        if experimental:
	    self.mfp = ServerProxy('https://%s:%s@www.mofplus.org/MFP_JPD/API/user/xmlrpc' % (self.username, self.pw))
        else:
            #self.mfp = ServerProxy('https://%s:%s@www.mofplus.org/API/call/xmlrpc' % (username, pw))
            self.mfp = ServerProxy('https://%s:%s@www.mofplus.org/API/user/xmlrpc' % (self.username, self.pw))
        self.check_connection()
        return

    def credentials_from_cmd(self):
        """
        Method to get the credentials from the command line
        """
        username = raw_input("Email:")
        pw       = getpass.getpass()
        return username, pw

    def check_connection(self):
        """
        Method to check if the connection to MFP is alive
        """
        try:
            self.mfp.add(2,2)
            logger.info("Connection to user API established")
        except xmlrpclib.ProtocolError:
            logger.error("Not possible to connect to MOF+. Check your credentials")
            exit()
        return

    def print_banner(self):
        """
        Prints the MFP banner
        """
        print  ":##::::'##::'#######::'########:::::::::::::::'###::::'########::'####:\n\
:###::'###:'##.... ##: ##.....::::'##::::::::'## ##::: ##.... ##:. ##::\n\
:####'####: ##:::: ##: ##::::::::: ##:::::::'##:. ##:: ##:::: ##:: ##::\n\
:## ### ##: ##:::: ##: ######:::'######::::'##:::. ##: ########::: ##::\n\
:##. #: ##: ##:::: ##: ##...::::.. ##.::::: #########: ##.....:::: ##::\n\
:##:.:: ##: ##:::: ##: ##::::::::: ##:::::: ##.... ##: ##::::::::: ##::\n\
:##:::: ##:. #######:: ##:::::::::..::::::: ##:::: ##: ##::::::::'####:\n\
:..:::::..:::.......:::..:::::::::::::::::::..:::::..::..:::::::::....:"

   
    @download('topology')
    def get_net(self,netname, mol = False):
        """Downloads a topology in mfpx file format
        :Parameters:
            -netname (str): name of the net
            -mol    (bool,optional): if true a mol object is returned, if false
                            topology is written to a file, defaults to False
        """
        lines = self.mfp.get_net(netname)
        return lines

    def get_list_of_nets(self):
        """Returns a list of all topologies in the db"""
        return self.mfp.get_list_of_nets()
    

    def get_list_of_bbs(self):
        """Returns a list of all BBS in the db"""
        return self.mfp.get_list_of_bbs()

    @download('building block')
    def get_bb(self,bbname, mol = False):
        """Downloads a bb in mfpx file format
        :Parameters:
            -bbname (str): name of the bb
            -mol    (bool,optional): if true a mol object is returned, if false
                            bb is written to a file, defaults to False
        """
        lines = self.mfp.get_bb(bbname)
        return lines
    
    @download('MOF')
    def get_mof_structure_by_id(self,strucid, mol = False):
        """Downloads a MOF structure in mfpx file format
        :Parameters:
            -strucid (str): id of the MOF structure in the DB
            -mol    (bool,optional): if true a mol object is returned, if false
                            bb is written to a file, defaults to False
        """
        lines,name = self.mfp.get_mof_structure_by_id(strucid)
        return lines

    def get_cs(self,name):
        """
        Returns the coordinations sequences of a topology as a list of lists.
        :Parameters:
            -name (str): Name of the topology
            
        """
        return self.mfp.get_cs(name)
    
    def get_vs(self,name):
        """
        Returns the vertex symbol of a topology as a list of strings
        :Parameters:
            -name (str): Name of the topology
        """
        return self.mfp.get_vs(name)

    def search_cs(self, cs, vs, cfilter = True):
        """
        Searches nets with a given coordination sequences and given vertex symbols and returns
        the corresponding netnames as a list of strings.
        :Parameters:
            -cs (list): List of the coordination sequences
            -vs (list): List of the vertex symbols
            -cfilter (bool): If true no catenated nets are returned, defaults to True
        """
        assert type(cs) == list
        assert type(vs) == list
        nets = self.mfp.search_cs(cs, vs)
        rl = []
        if cfilter:
            for i,n in enumerate(nets):
                if n.find('-c') != -1: rl.append(n)
            for i in rl: nets.remove(i)
        return nets
