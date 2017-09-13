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
           string s = "b|a b";
           var ss = re.Matches(s).Select(i=>i.ToString()).ToArray();
           var meta = new MetaInfo();
           Console.WriteLine(
           (parser.compile_closure["Expr"] == parser.Expr)+
           " "+
           parser.Eq.possibilities.ToArray().Length+
              parser.Expr.Match(
               objs:ref ss,
               partial:false,
               meta:ref meta
           ).Dump()
          );
        
           
        }
    }
}
