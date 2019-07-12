#########################################################
#  https://nsetools.readthedocs.io/en/latest/usage.html#and-the-index-quote
#########################################################
from nsetools import Nse  # Nse Driver
from pprint import pprint # just for neatness of display
import pandas as pd
import numpy as np
nse = Nse()
print(nse)
q = nse.get_quote('lt') # it's ok to use both upper or lower case for codes.
pprint(q)
