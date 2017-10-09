
import re
token = re.compile('|'.join(['\`','\)','\(','[^\(\)\s\`]+','\n'])).findall
