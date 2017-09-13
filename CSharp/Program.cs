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
            
            var c = new List<string>();
            var d = new List<string>{"1","2"};
            c.AddRange(d);
            c.ForEach(Console.WriteLine);
        }
    }
}
