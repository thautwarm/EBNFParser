
import re
token = re.compile('|'.join(['\`','\\n','\)','\(','[^\(\)\s\`]+'])).findall
