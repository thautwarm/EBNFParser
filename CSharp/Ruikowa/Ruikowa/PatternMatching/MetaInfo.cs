using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using Ruikowa.Components;

namespace Ruikowa.PatternMatching
{
    public class MetaInfo
    {
        private static readonly Func<Trace<string>> TraceCons = () => new Trace<string>(null, null, 3);
        private static readonly Action<Trace<string>> TraceDest = (Trace<string> trace) => trace.VirtualLength = 0;

        private int _count;
        private readonly string _fileName;
        private Trace<Trace<string>> _traces;


        public string FileName => _fileName;
        public int Count => _count;

        public MetaInfo(
            int count,
            string fileName,
            Trace<Trace<string>> previous = null)
        {
            _count = count;
            _fileName = fileName;
            _traces = previous ?? new Trace<Trace<string>>(
                          TraceCons, TraceDest
                      );
        }

        public void NewTrace()
        {
            ++_count;
            _traces.New();
        }

        public (int, int) Commit() => (_count, _traces[_count].Count);

        public void Rollback((int, int) history)
        {
            var (count, traceLength) = history;
            _count = count;
            _traces[count].VirtualLength = traceLength;
        }

        public (int, string) Fork()
        {
            return (_count, _fileName);
        }

        public int MaxFetched => _traces.Count;
    }
}