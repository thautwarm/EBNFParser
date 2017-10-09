
import re
token = re.compile('|'.join(['\]','\\n','\[','\:','\/','\-','\,','\+','\*','\)','\(','\%','if(?!\S)','else(?!\S)','lambda(?!\S)','not(?!\S)','or(?!\S)','and(?!\S)','for(?!\S)','in(?!\S)','\d+|\d*\.\d+','True(?!\S)|False(?!\S)|None(?!\S)','[a-zA-Z_][a-zA-Z0-9]*'])).findall
