using CSharp.ObjectRegex;
using CSharp.LanguageTest.SelfExaminationForEBNF;
using System;
using System.Linq;

namespace CSharp.Test
{

    public class AssertError : Exception{
        public AssertError(string info):base(info){
        }
    }
    public class Assert{
        public static void equals<A>(A a, A b, string str){
            if (!a.Equals(b)){
                throw new AssertError(str);
            }
        }

    }
    public class NaiveTest
    {
        public static string SelfExamination(string source){


            // Initialize parser
            var parser = Parser.GenParser();
            var re     = DefualtToken.Token();

            // Gen tokenized words
            var tokens = re.Matches(source).Select(i => i.ToString()).ToArray();
            
            // Parsing
            var meta = new MetaInfo();
            return parser.Stmt.Match(
                objs   : tokens,
                partial: false,
                meta   : ref meta
            ).Dump();

        }
    }
}