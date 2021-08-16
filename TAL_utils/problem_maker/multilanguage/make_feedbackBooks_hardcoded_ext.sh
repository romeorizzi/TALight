#!/bin/bash
# script che estrae il ${servername}_feedbackBook.hardcoded_ext.yaml  file per tutti i servizi di tutti i problemi contenuti nella collection tutorial.

BOLD='\e[1m'
RED='\033[0;31m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

for prob in $( ls /home/romeo/TALight/example_problems/tutorial | xargs ) ; do
    echo -e "\nwith problem ${GREEN}${BOLD}${prob}${NC} we do:"
    for server in /home/romeo/TALight/example_problems/tutorial/${prob}/services/*_server.py ; do
	echo  -e "\n   - with server ${BOLD}${server}${NC} we do:"
	servernamewithextension=$( basename $server)
	servername=${servernamewithextension%.py}
	echo ./extract_feedbackBook_hardcoded.py ${server} fstring_count -preamble_file=preamble.hardcoded_ext.yaml > /home/romeo/TALight/example_problems/tutorial/${prob}/lang/hardcoded_ext/${servername}_feedbackBook.hardcoded_ext.yaml
	./extract_feedbackBook_hardcoded.py ${server} fstring_count -preamble_file=preamble.hardcoded_ext.yaml > /home/romeo/TALight/example_problems/tutorial/${prob}/lang/hardcoded_ext/${servername}_feedbackBook.hardcoded_ext.yaml
    done
done

