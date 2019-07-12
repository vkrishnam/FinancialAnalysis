################################################
## https://nsepy.readthedocs.io/en/latest/
################################################

from nsepy import get_history
from datetime import date
import pprint
data = get_history(symbol="LT", start=date(2019,7,1), end=date(2019,7,9))
print(data[['Close']])
