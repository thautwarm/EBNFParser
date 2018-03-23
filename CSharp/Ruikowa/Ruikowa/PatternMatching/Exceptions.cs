using System;

namespace Ruikowa.PatternMatching
{
    public class UnsolvedException : Exception
    {
        public UnsolvedException(string info) : base(info)
        {
        }
    }
}