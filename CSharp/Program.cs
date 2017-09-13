using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using CSharp.ObjectRegex;
using CSharp.LanguageTest.SelfExaminationForEBNF;
using System.IO;
namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            // Initial parser
            var parser = Parser.GenParser();
            var re     = DefualtToken.Token();

            // Gen source
            string source = File.ReadAllText("../selfexamine.ebnf");
            var tokens = re.Matches(source).Select(i => i.ToString()).ToArray();

            // Parsing.
            var meta = new MetaInfo();
            Console.WriteLine(parser.Stmt.Match(
                objs   : tokens,
                partial: false,
                meta   : ref meta
            ).Dump());


        }
    }
}
