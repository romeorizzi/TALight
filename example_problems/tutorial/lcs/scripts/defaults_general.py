#!/usr/bin/env python3
import os

# PATHS (Relative to where this defaults.py module and the scripts resting on it are placed):
REL_PATH_SOLUTIONS = os.path.join('..','my_solutions')
REL_PATH_CERTIFICATES = os.path.join('..','my_certificates')
REL_PATH_INSTANCES = os.path.join('..','instances_catalogue','all_instances')

# SERVERS:
SERVERS_LIST = { 'local': None, 'cpt': 'xxx', 'ioi': 'xxx' }
SERVER = 'local'

# NAMING:
SOL_FILE_PREFIX = 'sol_'

# COLORS:

# In case your terminal cannot manage colors thought the ANSI escape sequences then turn off the colors with the following flag (or adapt the subsequent codes/sequences to your situation when possible):
TURN_OFF_COLORS = False
#TURN_OFF_COLORS = True

CEND      = '' if TURN_OFF_COLORS  else '\33[0m'
CBOLD     = '' if TURN_OFF_COLORS  else '\33[1m'
CITALIC   = '' if TURN_OFF_COLORS  else '\33[3m'
CURL      = '' if TURN_OFF_COLORS  else '\33[4m'
CBLINK    = '' if TURN_OFF_COLORS  else '\33[5m'
CRED      = '' if TURN_OFF_COLORS  else '\33[31m'
CGREEN    = '' if TURN_OFF_COLORS  else '\33[32m'
CYELLOW   = '' if TURN_OFF_COLORS  else '\33[33m'
CBLUE     = '' if TURN_OFF_COLORS  else '\33[34m'
CVIOLET   = '' if TURN_OFF_COLORS  else '\33[35m'
CBEIGE    = '' if TURN_OFF_COLORS  else '\33[36m'
CWHITE    = '' if TURN_OFF_COLORS  else '\33[37m'
