using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;
using CSharp.ObjectRegex;
namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            var a = new Regex(@"\d+|\d*\.\d+");
            var b = a.Match("23");
            var c = new List<string>();
            var s = new Mode().setName("Node1").setValue("Str1");
            
            var d = new Mode().setName("Root1");
            d.Add(s);
            Console.WriteLine(d.Dump());
        }
    }
}
