
import re
token = re.compile('|'.join(['t','\=\>','\:','\)','\('])).findall
