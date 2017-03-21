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
import user
logger = logging.getLogger("mofplus")


class admin_api(user.user_api):

    """
    Via the admin_api class the API routines of MOFplus which are accessable for normal users and for admin users
    can be used. Class is inherited from the user_api class.
    
    The credentials can be set either as environment variables MFPUSER and MFPPW or can be given interactively.

    :Attrributes:
        - mfp (obj)     : ServerProxy XMLRPCLIB object holding the connection to MOF+
        - username (str): Username on MOF+
        - pw (str)      : Password corresponding to the username

    :Args:
        - experimental (bool, optional): Use to connect to experimental DB, defaults to False
        - banner       (bool, optional): If True, the MFP API banner is printed to SDTOUT, defaults to False
    """

    def __init__(self, experimental = False, banner = False):
        user.user_api.__init__(self,experimental, banner)
        if experimental:
	    self.mfp = ServerProxy('https://%s:%s@www.mofplus.org/MFP_JPD/API/admin/xmlrpc' % (self.username, self.pw))
        else:
            self.mfp = ServerProxy('https://%s:%s@www.mofplus.org/API/admin/xmlrpc' % (self.username, self.pw))
        self.check_adminconnection()

    def check_adminconnection(self):
        """
        Method to check if the connection to MFP is alive
        """
        try:
            self.mfp.add2(2,2)
            logger.info("Connection to admin API established")
            print """
            We trust you have received the usual lecture from the MOF+ system administrator.
            It usually boils down to these two things:
                #1) Think before you type.
                #2) With great power comes great responsibility.
            """
        except xmlrpclib.ProtocolError:
            logger.error("Not possible to connect to MOF+ admin API. Check your credentials")
            exit()
        return

    def delete_net(self, name):
        """
        Deletes a net from the db
        :Parameters:
            -name (str): name of the net
        """
        assert type(name) == str
        self.mfp.delete_net(name)
   
    def add_bb_penalties(self,data):
        """
        Method to adds penalties to building blocks
        """
        retstring = self.mfp.add_bb_penalties(data)
        print retstring
        return

    def upload_weaver_run(self, fwid, fname):
        """
        Method to upload the results of a weaver run to the db
        :Parameters:
            -fwid: firework id of the job
            -fname: filename of the structure file
        """
        data = {}
        data['fwid'] = str(fwid)
        f = open(fname, 'r')
        data['fmfpx'] = f.read()
        a = self.mfp.upload_weaver_run(data)
        return

    def upload_mof_structure_by_id(self, fname, strucid):
        """
        Method to upload a structure file to the DB
        :Parameters:
            - fname (str): path to the mfpx file
            - strucid (int): id of the structure in the db
        """
        data = {}
        f = open(fname, 'r')
        data['id'] = strucid
        data['fmfpx'] = f.read()
        self.mfp.upload_mof_structure_by_id(data)
        return

    def upload_topo_file_by_name(self, fname, name):
        """
        Method to upload a topo file to the DB
        :Parameters:
            - fname (str): path to the mfpx file
            - name (str): name of the topology
        """
        data = {}
        f = open(fname, 'r')
        data['name'] = name
        data['fmfpx'] = f.read()
        self.mfp.upload_topo_file_by_name(data)
        return

    ### method in principle obsolete
    def upload_pa_run(self,data):
        ret = self.mfp.upload_pa_run(data)
        return

    def upload_bbfile_by_name(self, fname, name):
        """
        Method to upload a bb file to the DB
        :Parameters:
            - fname (str): path to the mfpx file
            - name (str): name of the bb
        """
        data = {}
        f = open(fname, 'r')
        data['name'] = name
        data['fmfpx'] = f.read()
        self.mfp.upload_bbfile_by_name(data)
        return

    def insert_bb(self,name, fname, chemtype, frag = False):
        """
        Method to create a new entry in the bb table.
        :Parameters:
            - name (str): name of the bb
            - fname (str): path to the mfpx file
            - chemtype (str): string describing the character of the bb
            - frag (bool, optional): Option to set a BB as fragment, defaults to False
        """
        data = {}
        data['name'] = name
        data['fmfpx'] = open(fname, 'r').read()
        data['type'] = chemtype
        self.mfp.insert_bb(data)
        return

    def set_cs(self, name, cs):
        """
        Method to set the cs of a topology.
        :Parameters:
            - name (str): name of the topology
            - cs (list): list of lists with the cs
        """
        data = {}
        data['name'] = name
        data['cs'] = cs
        self.mfp.set_cs(data)
        return
    
    def set_vs(self, name, vs):
        """
        Method to set the vs of a topology.
        :Parameters:
            - name (str): name of the topology
            - vs (list): list with the vs
        """
        data = {}
        data['name'] = name
        data['vs'] = vs
        self.mfp.set_vs(data)
        return
    
    def connect_nets(self, pnet, cnet, pattern):
        """
        Method to create relationchips between nets in the DB
        :Parameters:
            - pnet (str): name of the parent net
            - cnet (str): name of the child net
            - pattern (str): derivation type
        """
        assert type(pnet) == str
        assert type(cnet) == str
        assert type(pattern) == str
        assert cnet != pnet
        self.mfp.connect_nets(pnet,cnet,pattern)
        return

    def add_skal_property(self, strucid, ptype, prop):
        """
        Method to add a skalar property to a structure
        :Parameters:
            - strucid (int): id of the structure in the DB
            - ptype (str): name of the property
            - prop (float): property value
        """
        assert type(strucid) == int
        assert type(ptype) == str
        self.mfp.add_skal_property(strucid, ptype, prop)
        return

    def add_xy_property(self,strucid,ptype,data):
        """
        Method to add a dataset as property to the DB
        :Parameters:
            - strucid (int): id of the structure in the DB
            - ptype (str): name of the property
            - data (dict): dataset as dictionary 
        """
        assert type(strucid) == int
        assert type(ptype) == str
        self.mfp.add_xy_property(strucid, ptype,data)
        return

    def fa_finish(self,faid):
        """
        Method to register a fireanalyzer run as finished
        :Parameters:
            - faid (int): id of fireanalyzer run
        """
        assert type(faid) == int
        self.mfp.fa_finish(faid)
