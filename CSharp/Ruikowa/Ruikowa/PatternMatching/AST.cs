using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using Ruikowa.Components;

namespace Ruikowa.PatternMatching
{
    public class SExpr<T> : LinkedList<SExpr<T>>
    {
        public readonly string Name;

        SExpr(string name)
        {
            Name = name;
        }

        public override string ToString()
        {
            return Dumps(0);
        }

        public string Dumps(int indent = 0)
        {
            
            var tabs = new string('\t', indent);
            var nextTabs = new string('\t', indent + 1);
            
            var content =
                string
                    .Join('\n',
                        this.Select(_ => _.Dumps(indent + 1))
                            .AndThen(_ => string.Join(nextTabs, _)));
            
            return $"{tabs}{Name}[";

            return "";
        }
    }
}