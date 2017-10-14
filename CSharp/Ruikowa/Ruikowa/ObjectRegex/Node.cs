using System.Collections;

namespace Ruikowa.ObjectRegex
{
    public enum ASTType
    {
        literal, composed
    }
    public class AST
    {
        private ASTType Type;
        public ArrayList Composed;
        public string    Literal;
        public string Name;

        public AST(string name, string literal)
        {
            Name = name;
            Type = ASTType.literal;
            Literal = literal;
        }

        public AST(string name)
        {
            Name     = name;
            Type     = ASTType.composed;
            Composed = new ArrayList();
        }
    }
    public abstract class BaseParser
    {
        public string Name=null;
        public bool HasRecur = false;

        public abstract AST match(string[] objs, ref MetaInfo meta, bool recursive);
    }
}