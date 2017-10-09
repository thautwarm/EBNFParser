
import re
token = re.compile('|'.join(['\n','\<[a-zA-Z_0-9\n]*?\>','\</[a-zA-Z_0-9\n]*?\>','[^\n]*?(?=\</[a-zA-Z_0-9\n]*?\>|\<[a-zA-Z_0-9\n]*?\>|\n)'])).findall
