# JSON
parserGenerator tests/Python/Lang/JSON/grammar tests/Python/Lang/JSON/parser.py -test True -comment True 
python tests/Python/Lang/JSON/testLang.py Atom '
{
"a":"b",
"escapeStr":"\"I am the bone of my sword.\""
}
' -o tests/Python/Lang/JSON/EscapeStr 

python tests/Python/Lang/JSON/testLang.py Atom '
[ {        "a":"b", 
   "escapeStr":"\"I am the bone of my sword.\""}, 
  {"how do you do":["I am fine, thank you and you?", "Good..."],
         "Ice1000":[{"Glavo":"Yutong"}]
  }
]
' -o tests/Python/Lang/JSON/Complex
python tests/Python/Lang/JSON/testLang.py Atom '
[ {     "x":true, 
   	123:"\"I am the bone of my sword.\""}, 
  {     1.2:[3.14159, null],
         false:[{"Glavo":"Yutong"}]
  }
]
' -o tests/Python/Lang/JSON/Const -testTk True

