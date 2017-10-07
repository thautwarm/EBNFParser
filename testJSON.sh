export PYTHONPATH="Python"
# JSON
python Python/parserGenerator.py tests/Python/Lang/JSON/grammar tests/Python/Lang/JSON/parser.py -test True -comment True 
python tests/Python/Lang/JSON/testLang.py Atom '
{
"a":"b",
"escapeStr":"\"I am the bone of my sword.\""
}
' -o EscapeStr -testTk True

python tests/Python/Lang/JSON/testLang.py Atom '
[ {        "a":"b", 
   "escapeStr":"\"I am the bone of my sword.\""}, 
  {"how do you do":["I am fine, thank you and you?", "Good..."],
         "Ice1000":[{"Glavo":"Yutong"}]
  }
]
' -o Complex -testTk True


