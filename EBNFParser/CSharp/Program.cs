using System;
using System.IO;
namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            // Gen source
            string source = File.ReadAllText("../selfexamine.ebnf");
            var (testfunc, path) = (Test.Manage.GetTest(args[0]), args[1]);
	    var res = testfunc(source);
	    Console.WriteLine(res);
            File.WriteAllText(path, res);
        }
    }
}
