from Misakawa.ErrorFamily import handle_error
from parser import Test, token
import argparse
parser = handle_error(Test.match)
cmdparser = argparse.ArgumentParser(description='Test Lisp Parser Generated From EBNFParser.')
cmdparser.add_argument("Codes",  metavar = 'lispCodes', type = str,
                       help='Input some lisp codes here.')
args = cmdparser.parse_args()

tokenized = token.findall(args.Codes)
print(parser(tokenized, partial = False))






