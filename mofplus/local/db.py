# -*- coding: utf-8 -*-

from pydal import DAL, Field

db = DAL('mysql://root:d3v_w34v3r@bilbo.aci.rub.de/mysql',lazy_tables=True,fake_migrate_all=True)

path2files = "test"


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('nets',\
    Field('name', 'string', unique=True),\
    Field('spacegroup', 'string'),\
    Field('spacegroup_number', 'integer'),\
    Field('cella','double'),\
    Field('cellb','double'),\
    Field('cellc','double'),\
    Field('cellalpha','double'),\
    Field('cellbeta','double'),\
    Field('cellgamma','double'),\
    Field('p', 'integer'),\
    Field('q', 'integer'),\
    Field('r', 'integer'),\
    Field('s', 'integer'),\
    Field('natoms', 'integer'),\
    Field('thumb', 'string',default='default_thumb'),\
    Field('xyzfile', 'upload', uploadfolder=path2files+'/static/nets/files'),\
    Field('txyzfile','upload',uploadfolder=path2files+'/static/nets/files'),\
    Field('topofile','upload',uploadfolder=path2files+'/static/nets/files'),\
    Field('ptxyzfile','upload',uploadfolder=path2files+'/static/nets/files'))

db.define_table('vertex',\
    Field('netID','reference nets'),\
    Field('idx', 'integer'),\
    Field('coordination_number','integer'),\
    Field('connected_to','list:reference vertex'),\
    Field('connections','list:integer'),\
    Field('symmetry','string'),
    Field('cs1', 'integer'),
    Field('cs2', 'integer'),
    Field('cs3', 'integer'),
    Field('cs4', 'integer'),
    Field('cs5', 'integer'),
    Field('cs6', 'integer'),
    Field('cs7', 'integer'),
    Field('cs8', 'integer'),
    Field('cs9', 'integer'),
    Field('cs10','integer'),
    Field('vs', 'string'))

db.define_table('geoms',\
    Field('name','string'),\
    Field('coordination_number','integer'),\
    Field('symmetry','string'),\
    Field('xyzfile','upload',uploadfolder=path2files+'/static/geoms/files'))

db.define_table('shapes',\
    Field('penalty','double'),\
    Field('vertexID','reference vertex'),\
    Field('geoID', 'reference geoms'))

db.define_table('conn',\
    Field('fromID','reference vertex'),\
    Field('toID','reference vertex'),\
    Field('nconns','integer'),\
    Field('toself','boolean'))

db.define_table('edge',\
    Field('fromID','reference vertex'),\
    Field('toID','reference vertex'),\
    Field('fromcount','integer'),\
    Field('tocount','integer'))

db.define_table('net_relations',\
    Field('pID','reference nets'),\
    Field('cID','reference nets'),\
    Field('pattern','string'))


### MOFs are uniquely defined by its reference to !one topology and !a set of building blocks
db.define_table('mofs',\
    Field('name','string', unique = True),\
    Field('knownas','string'),\
    Field('net','reference nets'),\
    format='%(name)s') #,migrate = True, fake_migrate=True

### since a mof may have several relevant publications and one particular publication can have
### several mofs they refer to, we need a many2many relation here. 
db.define_table('mofspublications',\
    Field('mofID','reference mofs'),\
    Field('publicationID','reference publications'))

###level of theory
db.define_table('lot',\
    Field('name','string'),\
    Field('description','text'),\
    format='%(name)s')

### storage for all MOF models,
db.define_table('structures',\
    Field('filename','upload', uploadfolder=path2files+'/static/mofs/structures'),\
    Field('lot', 'reference lot'),\
    Field('name', 'string'),\
    Field('a', 'double'),\
    Field('b', 'double'),\
    Field('c', 'double'),\
    Field('alpha', 'double'),\
    Field('beta', 'double'),\
    Field('gamma', 'double'),\
    Field('comment', 'text'),\
    Field('mofID','reference mofs'))

### building blocks are stored here
db.define_table('bbs',\
    Field('name','string',unique=True),\
    Field('coordination_number','integer'),\
    Field('sum_formula','string'),\
    Field('type','string'),\
    #requires=IS_IN_SET(('organic','inorganic'))),\
    Field('xyzfile', 'upload', uploadfolder=path2files+'/static/bbs/files'),\
    Field('frag', 'boolean', default=False))
    #Field('stxyzfile','upload',uploadfolder=path2files+'/static/bbs/files'),\
    #Field('reagentID','reference reagents'),\ ### see below for discussion on reagents table.

### many2many to connect MOFs with the BBs
db.define_table('mofsbbs',\
    Field('mofID', 'reference mofs'),\
    Field('bbID', 'reference bbs'))

db.define_table('bbshapes',\
    Field('penalty','double'),\
    Field('bbID','reference bbs'),\
    Field('geoID', 'reference geoms'))

### description of the property
db.define_table('prop_type',\
    Field('name'),\
    Field('unit','string'),\
    Field('description','text'),format='%(name)s')

db.define_table('showmol',\
    Field('name','string'),\
    Field('filename','upload', uploadfolder=path2files+'/static/showmol'),\
    format='%(name)')

### single number features like energies, bulk moduli, surface areas and such are stored here
db.define_table('prop_skal',\
    Field('data','double'),\
    Field('type','reference prop_type'),\
    #Field('unit','string'),\
    Field('description','text'),\
    Field('structureID', 'reference structures'))

### every attribute that is more than just one number, like XY-graphs and such is stored here
db.define_table('prop_xy',\
    Field('data','upload', uploadfolder=path2files+'/static/mofs/spectra'),\
    Field('type','reference prop_type'),\
    #Field('unitx','string'),\
    #Field('unity','string'),\
    Field('description','text'),\
    Field('structureID', 'reference structures'))
#session.connect(request, response, cookie_key='yoursecret', compression_level=None)

db.define_table('bbvertices',\
    Field('mofsbbsID','reference mofsbbs'),\
    Field('vertexID','reference vertex'))

db.define_table('bbedges',\
    Field('mofsbbsID','reference mofsbbs'),\
    Field('edgeID','reference edge'),\
    Field('v0', 'reference vertex'),\
    Field('v1', 'reference vertex'))

db.define_table('special_conn',
    Field('bbID', 'reference bbs'),
    Field('idx',  'integer'),
    Field('nconn','integer'))

db.define_table('scvertices',
    Field('vertexID', 'reference vertex'),
    Field('bbvertexID', 'reference bbvertices'),
    Field('scID', 'reference special_conn'))

db.define_table('scaledtopo',\
    Field('mofID', 'reference mofs'),\
    Field('topofile','upload', uploadfolder=path2files+'/static/mofs/scaledtopo'),\
    Field('orientfile','upload', uploadfolder=path2files+'/static/mofs/scaledtopo'))

db.define_table('firejobs',\
    Field('jobtype', 'string'),\
    Field('jobID', 'integer'),\
    Field('endtime', 'datetime'),\
    Field('starttime', 'datetime'))

db.define_table('fireweaver',\
    Field('mof', 'reference mofs'),\
    Field('name', 'string'),\
    Field('comment', 'text'))

db.define_table('fireanalyzer',\
    Field('structureID', 'reference structures'))


########
###  parameter definitions and fragment tables
########

db.define_table('atypes',\
    Field('name', 'string',unique=True),format='%(name)s')

db.define_table('FFfrags',
    Field('name', 'string', unique = True),
    Field('creationtime', 'datetime'),
    Field('comment', 'text', default = ""),
    Field('priority', 'integer'),
    Field('file', 'upload', uploadfolder=path2files+'/static/FFs/frags'),format='%(name)s')

db.define_table('atypes2FFfrags',
    Field('atypeID', 'reference atypes'),
    Field('fragID', 'reference FFfrags'))

db.define_table('frag_conn',
    Field('frag1', 'reference FFfrags'),
    Field('atype1','reference atypes'),
    Field('frag2', 'reference FFfrags'),
    Field('atype2','reference atypes'))
    #Field('combined', 'reference bbs'))

db.define_table('FF',
    Field('name', 'string', unique = True),
    #Field('vdWtype', 'string', default='Buckingham'),
    Field('mixing', 'string', default='Lorentz-Bertholot'),
    #Field('chargetype', 'string',requires = IS_IN_SET(['gaussian','slater','point']), default = 'gaussian'),
    Field('cutoff', 'double'),
    Field('comment', 'text', default=""), format='%(name)s')

db.define_table('FFrefs',
    Field('name', 'string', unique = True),
    Field('uploadtime', 'datetime'),
    Field('priority', 'integer'),
    Field('reffile','upload', uploadfolder=path2files+'/static/FFs/refs'),
    Field('graph','upload', uploadfolder=path2files+'/static/FFs/refs'),
    Field('comment', 'text', default=""),
    format='%(name)s')

db.define_table("FFfrags2FFrefs",
    Field('fragID', 'reference FFfrags'),
    Field('refID', 'reference FFrefs'))

db.define_table("atypes2FFrefs",
    Field('atypeID', 'reference atypes'),
    Field('refID', 'reference FFrefs'))

db.define_table('FFfits',
    #Field('name', 'string', unique = True),
    Field('FFID', 'reference FF'),
    Field('creationtime', 'datetime'),
    Field('settings', 'json'),
    Field('input', 'upload', uploadfolder=path2files+'/static/FFs/inp'),
    Field('output', 'upload', uploadfolder=path2files+'/static/FFs/out'),
    Field('refID1', 'reference FFrefs'),
    Field('comment', 'text', default=""))

db.define_table('onebody',
    #Field('FFID', 'reference FF'),
    Field('creationtime', 'datetime'),
    Field('fitID', 'reference FFfits'),
    Field(  'type', 'string'),
    Field('pot', 'string'),
    Field('comment', 'text', default=""),
    Field('atype1', 'reference atypes'),
    Field( 'frag1', 'reference FFfrags'),
    Field('params', 'json'))

db.define_table('twobody',
    #Field('FFID', 'reference FF'),
    Field('creationtime', 'datetime'),
    Field('fitID', 'reference FFfits'),
    Field(  'type', 'string',),
    Field('pot', 'string'),
    Field('comment', 'text', default=""),
    Field('atype1', 'reference atypes'),
    Field( 'frag1', 'reference FFfrags'),
    Field('atype2', 'reference atypes'),
    Field( 'frag2', 'reference FFfrags'),
    Field('params', 'json'))

db.define_table('threebody',
    #Field('FFID', 'reference FF'),
    Field('creationtime', 'datetime'),
    Field('fitID', 'reference FFfits'),
    Field('type', 'string'),
    Field('pot', 'string'),
    Field('comment', 'text', default=""),
    Field('atype1', 'reference atypes'),
    Field( 'frag1', 'reference FFfrags'),
    Field('atype2', 'reference atypes'),
    Field( 'frag2', 'reference FFfrags'),
    Field('atype3', 'reference atypes'),
    Field( 'frag3', 'reference FFfrags'),
    Field('params', 'json'))

db.define_table('fourbody',
    #Field('FFID', 'reference FF'),
    Field('creationtime', 'datetime'),
    Field('fitID', 'reference FFfits'),
    Field('type', 'string'),
    Field('pot', 'string'),
    Field('comment', 'text', default=""),
    Field('atype1', 'reference atypes'),
    Field( 'frag1', 'reference FFfrags'),
    Field('atype2', 'reference atypes'),
    Field( 'frag2', 'reference FFfrags'),
    Field('atype3', 'reference atypes'),
    Field( 'frag3', 'reference FFfrags'),
    Field('atype4', 'reference atypes'),
    Field( 'frag4', 'reference FFfrags'),
    Field('params', 'json'))


### software table stores recent versions of molsys, pydlpoly and weaver
db.define_table('software',
    Field(  'name', 'string', unique=True),
    Field(  'changeset', 'integer'),
    Field(  'branch', 'string', default ='default'),
    Field(  'about', 'text'),
    Field(  'logo', 'reference pictures'),
    Field( 'archive', 'upload', uploadfolder=path2files+'/static/software/archive'),
    Field( 'doc', 'upload', uploadfolder=path2files+'/static/software/doc'),format='%(name)s %(changeset)s')
