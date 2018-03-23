namespace Ruikowa.Components
{
    public interface SExpr<T>
    {
        /// <summary>
        /// TC means the composed one while TS refers to the singleton.
        /// </summary>
        string Name { get; }

        string Dumps(int indent);

        T Content { get; }
    }
}