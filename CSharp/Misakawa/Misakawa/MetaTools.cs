using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
namespace Misakawa
{
    public class ObjectUsageError : Exception
    {
        public ObjectUsageError(string info) : base(info){}
    }
    public class CheckCondictionError : Exception{
        public CheckCondictionError(string info):base(info){}    
    }
    public class UnsolvedError : Exception
    {
        public   UnsolvedError(string info):base(info){}
    }
    
    public class MetaInfo
    {
        public int Count;
        public Stack<(string, int)> Trace;
        public int Rdx;
        public Stack<(int, int, int)> History;

        public MetaInfo(int count = -1, int rdx = -1, Stack<(string, int)> trace = null)
        {
            this.Count = count==-1? 0 : count;
            this.Trace = trace?? new Stack<(string, int)>();
            this.Rdx   = rdx  ==-1? 0 : rdx ;
            History    = new Stack<(int, int, int)>();
        }

        public void Branch()
        {
            History.Push((Count, Rdx, Trace.Count));
        }

        public void Rollback()
        {
            try
            {
                int length;
                (Count, Rdx, length) = History.Pop();
                while (Trace.Count > length)
                {
                    Trace.Pop();
                }
            }
            catch (IndexOutOfRangeException e)
            {
                Console.WriteLine(e);
            }
        }

        public void Pull()
        {
            try
            {
                History.Pop();
            }
            catch (IndexOutOfRangeException e)
            {
                Console.WriteLine(e);
            }
        }
    }
    public static class Tools{
        public static (string, Func<string, string>) RegexMatchFunc(string literal, bool escape = false)
        {
            var tokenRule = escape == true ? Regex.Escape(literal) : literal;
            var regex      = new Regex(tokenRule);
            return (tokenRule, str =>
            {
                if (str.Length.Equals(0))
                    return null;
                var r = regex.Match(str);
                if (r.Index != 0 || r.Length != str.Length)
                    return null;
                return str;
            });
        }
//        public static Func<string[], Ast> ErrorHandler(Func<string[], Ast> f)
//        {
//            return f;
//        }
    }
    

    

}