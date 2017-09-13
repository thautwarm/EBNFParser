using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using CSharp.ObjectRegex;
using CSharp.LanguageTest.SelfExaminationForEBNF;
namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            var parser = Parser.GenParser();
            var re = DefualtToken.Token();
            string s = "a ::= b|a b \n";
            var ss = re.Matches(s).Select(i => i.ToString()).ToArray();
            var meta = new MetaInfo();
            Console.WriteLine(parser.Stmt.Match(
                objs: ss,
                partial: false,
                meta: ref meta
            ).Dump());


        }
    }
}
