using System;
using System.Collections.Generic;

namespace Ruikowa.PatternMatching
{
    public class Trace<T> : List<T>
    {
        public int VirtualLength;

        public readonly Action New;

        public Trace(Func<T> elemCons = null, Action<T> elemDest = null, int capacity = 1) : base(capacity)
        {
            if (elemCons != null && elemDest != null)
                New = () =>
                {
                    if (VirtualLength == Count)
                    {
                        ++VirtualLength;
                        Add(elemCons());
                    }
                    else if (VirtualLength < Count)
                    {
                        elemDest?.Invoke(this[VirtualLength]);
                        ++VirtualLength;
                    }
                };
        }

        public void Append(T elem)
        {
            if (VirtualLength == Count)
            {
                ++VirtualLength;
                Add(elem);
            }
            else if (VirtualLength < Count)
            {
                this[VirtualLength] = elem;
                ++VirtualLength;
            }
        }


        public T Pop()
        {
            --VirtualLength;
            return this[VirtualLength];
        }

        public void Dispose()
        {
            VirtualLength = 0;
        }
    }
}