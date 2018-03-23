using Ruikowa.Components;

namespace Ruikowa.PatternMatching
{
    public class Tokenizer : SExpr<string>
    {
        public string _name;
        public string _content;
        
        
        public string Content;

        Tokenizer(string name)
        {
            Name = name;
        }

        public string Dumps(int indent = 0)
        {
            return "";
        }
    }
}