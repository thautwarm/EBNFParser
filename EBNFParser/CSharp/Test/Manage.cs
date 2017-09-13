using System;
namespace CSharp.Test
{
    public class Manage
    {
        public static Func<string, string> GetTest(string argv){
            switch(argv){
                case "se":
                    //self-examination
                    return Test.NaiveTest.SelfExamination;
                
                default:

                    return Test.NaiveTest.SelfExamination;
            }

        }

    }
}