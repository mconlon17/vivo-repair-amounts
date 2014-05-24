#!/user/bin/env/python
"""
    repair-amounts.py -- Replace invalid alues with valid values. Write
    a repair function to transforma before value to an after value.

    For the examples here, remove dollars signs, commas and HTML elements
    from values intended to contain numbers.

    Version 1.0 MC 2014-05-24
    --  Works as expected.  Used to repair 401 directAwardAmounts

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "1.0"

from vivotools import update_data_property
from vivotools import vivo_sparql_query
from vivotools import rdf_header
from vivotools import rdf_footer
from datetime import datetime

def make_data_dictionary(pred="vivo:totalAwardAmount", debug=False):
    """
    Create a dictionary of the specified data pred.  Key is uri.
    """
    query = """
    SELECT ?uri ?data
    WHERE {
        ?uri {{pred}} ?data .
    }
    """
    query = query.replace('{{pred}}', pred)
    result = vivo_sparql_query(query)
    if debug:
        print "Query = ", query
        print "Result = ", len(result['results']['bindings'])
    dictionary = {}
    for row in result['results']['bindings']:
        uri = row['uri']['value']
        data = row['data']['value']
        dictionary[uri] = data
    return dictionary

def repair(before):
    """
    Given a string of data, return the improved version
    """
    after = before.replace('$', '')
    after = after.replace(',', '')
    after = after.replace('<p>', '')
    after = after.replace('</p>', '')
    after = after.replace('&nbsp;', '')
    after = after.replace('<br />', '')
    if before != after:
        print before, after
    return after

#  Start here

pred = "vivo:totalAwardAmount"
print datetime.now(), "Start"
print datetime.now(), "Making data dictionary for", pred
data_dictionary = make_data_dictionary(pred)
print datetime.now(), "Data dictionary has ", len(data_dictionary), " entries."
ardf = rdf_header()
srdf = rdf_header()
for uri, data in data_dictionary.items():
    [add, sub] = update_data_property(uri, pred, data, repair(data))
    ardf = ardf + add
    srdf = srdf + sub
srdf = srdf + rdf_footer()
ardf = ardf + rdf_footer()
add_file = open('add.rdf', 'w')
print >>add_file, ardf
add_file.close()
sub_file = open('sub.rdf', 'w')
print >>sub_file, srdf
sub_file.close()
print datetime.now(), "Finished"
