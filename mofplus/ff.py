#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
from xmlrpclib import ServerProxy
import molsys.stow as stow
import sys
import logging
import os
import molsys
from assign_FF import sort_bond, sort_angle, sort_dihedral, sort_oop
import getpass
from decorator import faulthandler, download
import admin

logger = logging.getLogger("mofplus")

bodymapping = {1:"onebody", 2:"twobody",3:"threebody",4:"fourbody"}

allowed_ptypes = {1: ["charge", "vdw", "equil"],
        2: ["bond", "chargemod", "vdwpr"],
        3: ["angle"],
        4: ["dihedral", "oop"]
        }

allowed_potentials = {"charge": [["point",1], ["gaussian",2], ["slater",2]],
        "equil": [["equil", 1]],
        "vdw": [["LJ",2], ["buck",2], ["buck6d",2]],
        "bond": [["harm",2], ["mm3",2], ["quartic",5], ["morse",3]],
        "chargemod": [["point",1], ["gaussian",2], ["slater",2]],
        "vdwpr": [["LJ",2], ["buck",2], ["damped_buck",2]],
        "angle": [["harm",2],["mm3",2], ["quartic",5], ["fourier",5],  ["strbnd", 3]],
        "dihedral": [["harm",2], ["cos3",3], ["cos4",4]],
        "oop": [["harm",2]]}


class FF_api(admin.admin_api):

    def format_atypes(self, atypes, ptype, potential):
        """
        Helper function to extract fragments out of atypes and to
        order atypes and fragements in dependence of the ptype.
        """
        assert type(ptype) == str
        if ptype == "bond":
            atypes = sort_bond(atypes)
        elif ptype == "angle":
            atypes = sort_angle(atypes)
        elif ptype == "oop":
            atypes = sort_oop(atypes)
        elif ptype == "dihedral":
            atypes = sort_dihedral(atypes)
        latypes = atypes.split(":")
        atypes = []
        fragments = []
        for at in latypes:
            atypes.append(at.split("@")[0])
            fragments.append(at.split("@")[1])
        assert len(atypes) == len(fragments)
        if ptype not in allowed_ptypes[len(atypes)]:
            raise ValueError("ptype %s not allowed for %s term" % (ptype, bodymapping[len(atypes)]))
        if potential not in [i[0] for i in allowed_potentials[ptype]]:
            raise ValueError("potential %s not allowed for ptype %s" % (potential, ptype))
        return atypes, fragments

    def get_params_from_ref(self, FF, ref):
        """
        Method to look up all FF parameters that are available for a reference system
        :Parameters:
            - FF (str): Name of the FF the parameters belong to
            - ref (str): Name of the reference system the parameters belong to
        """
        assert type(FF) == type(ref) == str
        paramsets = self.mfp.get_params_from_ref(FF,ref)
        paramdict = {"onebody":{"charge":{},"vdw":{},"equil":{}},
                "twobody":{"bond":{},"chargemod":{}, "vdwpr":{}},
                "threebody":{"angle":{}},
                "fourbody": {"dihedral":{},"oop":{}}}
        # RS (explanation to be improved by JPD)
        # paramset is a nested list of lists provided by MOF+
        # it is resorted here in to a number of nested directories for an easier retrieval of data
        # i loops over the lists from paramset
        # each entry is
        #      i[0] : atomtype (len i[0] determines n-body via gloabl bodymapping)
        #      i[1] : fragment
        #      i[2] : type (e.g. charge, vdw, equiv)   TODO: change euilv -> equiv
        #      i[3] : ptype
        #      i[4] : paramstring
        for i in paramsets:
            typestr =""
            for a,f in zip(i[0],i[1]):
                typestr+="%s@%s:" % (a,f)
            # cut off last ":"
            typestr = typestr[:-1]
            typedir = paramdict[bodymapping[len(i[0])]][i[2]]
            if typestr in typedir:
                # another term .. append
                typedir[typestr].append((i[3],i[4]))
            else:
                typedir[typestr] = [(i[3],i[4])]
        return paramdict

    @faulthandler
    def get_params(self,FF, atypes, ptype, potential,fitsystem):
        """
        Method to look up parameter sets in the DB
        :Parameters:
            - FF (str): Name of the FF the parameters belong to
            - atypes (list): list of atypes belonging to the term
            - ptype (str): type of requested term
            - potential (str): type of requested potential
            - fitsystem (str): name of the FFfit/reference system the
              parameterset is obtained from
        """
        assert type(FF) == type(ptype) == type(atypes) == type(potential) == str
        atypes, fragments = self.format_atypes(atypes,ptype, potential)
        params = self.mfp.get_params(FF, atypes, fragments, ptype, potential, fitsystem)
        return params

    @faulthandler
    def set_params(self, FF, atypes, ptype, potential, fitsystem,params):
        """
        Method to upload parameter sets in the DB
        :Parameters:
            - FF (str): Name of the FF the parameters belong to
            - atypes (str): list of atypes belonging to the term
            - ptype (str): type of requested term
            - potential (str): type of requested potential
            - params (list): parameterset
            - fitsystem (str): name of the FFfit/reference system the
              parameterset is obtained from
        """
        assert type(FF) == type(ptype) == type(potential) == type(atypes) == str
        assert type(params) == list
        atypes, fragments = self.format_atypes(atypes,ptype, potential)
        rl = {i[0]:i[1] for i in allowed_potentials[ptype]}[potential]
        if len(params) != rl:
            raise ValueError("Required lenght for %s %s is %i" %(ptype,potential,rl))
        ret = self.mfp.set_params(FF, atypes, fragments, ptype, potential, fitsystem,params)
        return ret

    def list_FFrefs(self,FF):
        """
        Method to list names and meta properties of all available reference systems in the DB
        :Parameters:
            - FF (str): Name of the FF the reference systems belong to
        """
        assert type(FF) == str
        return self.mfp.list_FFrefs(FF)

    def set_FFref(self, name, hdf5path, mfpxpath, comment=""):
        """
        Method to create a new entry in the FFref table and to upload a file with
        reference information in the hdf5 file format.
        :Parameters:
            - name (str): name of the entry in the DB
            - path (str): path to the hdf5 reference file
        """
        assert type(name) == type(hdf5path) == type(mfpxpath) == type(comment) == str
        with open(hdf5path, "rb") as handle:
            binary = xmlrpclib.Binary(handle.read())
        with open(mfpxpath, "r") as handle:
            mfpx = handle.read()
        self.mfp.set_FFref(name, binary, mfpx, comment)
        return

    def set_FFref_graph(self,name, mfpxpath):
        with open(mfpxpath, "r") as handle:
            mfpx = handle.read()
        self.mfp.set_FFref_graph(name,mfpx)
        return

    @download("FFref")
    def get_FFref_graph(self,name, mol = False):
        """
        Downloads the reference system in mfpx file format
        :Parameters:
            -name (str): name of the reference system
            -mol    (bool,optional): if true a mol object is returned, if false
                            fragment is written to a file, defaults to False
        """
        assert type(name) == str
        lines = self.mfp.get_FFref_graph(name)
        return lines

    @download("FFref", binary = True)
    def get_FFref(self,name):
        """
        Method to retrieve an reference file in hdf5 file format from the DB
        :Parameters:
            - name (str): name of the entry in the DB
        """
        assert type(name) == str
        bstr = self.mfp.get_FFref(name).data
        return bstr

    def set_FFfrag(self,name,path,comment=""):
        """
        Method to create a new entry in the FFfrags table.
        :Parameters:
            - name (str): name of the entry in the db
            - path (str): path to the mfpx file of the fragment
            - comment (str): comment
        """
        assert type(name) == type(path) == type(comment) == str
        with open(path, "r") as handle:
            lines = handle.read()
            m = molsys.mol()
            m.fromString(lines, ftype = "mfpx")
            prio = m.natoms-m.elems.count("x")
        self.mfp.set_FFfrag(name, lines, prio, comment)
        return

    @download("FFfrag")
    def get_FFfrag(self,name, mol = False):
        """
        Downloads a FFfrag in mfpx file format
        :Parameters:
            -name (str): name of the fragment
            -mol    (bool,optional): if true a mol object is returned, if false
                            fragment is written to a file, defaults to False
        """
        assert type(name) == str
        lines = self.mfp.get_FFfrag(name)
        return lines

    def list_FFfrags(self):
        """
        Method to list names and meta properties of all available FFfrags in the DB
        """
        return self.mfp.list_FFfrags()

    def get_parameter_history(self, id):
        assert type(id) == int
        return self.mfp.get_parameter_history(id)

    def get_FFfit(self, id):
        return

    def set_FFfit(self,id):
        return

if __name__ == '__main__':
    option = [
            ['', 't', 'topology', "Name of topology which is downloaded from mofplus"],
            ['', 'b', 'buildingblock', "Name of building block which is downloaded from mofplus"],
            ]
    shellval = stow.main(stow.sys.argv[1:], option)
    if shellval[0] != '' or shellval[1] != '':
        api = FF_api(banner=False, experimental = False)
        if shellval[0] != '': api.get_net(shellval[0], mol = False)
        if shellval[1] != '': api.get_bb(shellval[1], mol = False)
    else:
        api = FF_api(banner=True, experimental = False)

