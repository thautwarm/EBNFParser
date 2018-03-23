using System;
using System.Linq;

namespace Ruikowa.Components
{
    public static class Ext
    {
        public static TR AndThen<TF, TR>(this TF obj, Func<TF, TR> fn)
        {
            return fn(obj);
        }

        public static void AndThen<TF>(this TF obj, Action<TF> fn)
        {
            fn(obj);
        }

        public static void AndThen<TF>(this TF obj, Action fn)
        {
            fn();
        }
    }
}