using CSharp.ObjectRegex;
using CSharp.LanguageTest.SelfExaminationForEBNF;
using System;

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
    public class SelfExamination
    {
        public static void Test(string source){
            



        }
    }
}