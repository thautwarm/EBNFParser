
using System.Collections.Generic;
using System.ComponentModel;
using Ruikowa.ErrorFamily;

namespace Ruikowa.Core
{
    public enum Operate
    {
        Next,
        Last
    };

    public struct ParserType
    {
        public string Name;
    }

    
    public enum Unit
    {    
        none
    }
    public class Trace<T>
    {
        public  int     Length;
        public  List<T> Content;
        private int     _Mem;

        public T fromIndex(int index)
        {
            if (index >= Length)
            throw new WarningException(@"
            You're trying to visit the elems that've been deprecated.
            If it occurred when you're using EBNFParser, report it as 
            a BUG at 
            `https://github.com/thautwarm/EBNFParser`. Thanks a lot!");
            return Content[index];

        }
        public T Get(int index)
        {
            if (index >= Length)
                throw new WarningException(@"
            You're trying to visit the elems that've been deprecated.
            If it occurred when you're using EBNFParser, report it as 
            a BUG at 
            `https://github.com/thautwarm/EBNFParser`. Thanks a lot!");
            return Content[index];
        }

        public T Get(T obj, Operate op)
        {

            int idx = Where(obj);
            switch (op)
            {
                    case Operate.Last:
                        return Get(idx - 1);
                    case Operate.Next:
                        return Get(idx + 1);
                    default:
                        throw new UnsolvedError("Undef Operate Sign");
            }
            return obj;
        }
        public int Where(T obj)
        {
            return Content.IndexOf(obj);
        }
            
    }
}