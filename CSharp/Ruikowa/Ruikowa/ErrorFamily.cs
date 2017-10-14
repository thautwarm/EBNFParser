using System;

namespace Ruikowa.ErrorFamily
{
    public class ObjectUsageError : Exception
    {
        public ObjectUsageError(string info) : base(info)
        {
        }
    }

    public class CheckConditionError : Exception
    {
        public CheckConditionError(string info) : base(info)
        {
        }
    }

    public class UnsolvedError : Exception
    {
        public UnsolvedError(string info) : base(info)
        {
        }
    }
}
