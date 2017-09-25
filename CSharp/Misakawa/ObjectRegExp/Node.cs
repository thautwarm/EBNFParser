using System;
using System.Collections;
using Misakawa;
using System.Collections.Generic;
using System.Linq;

namespace ObjectRegExp
{

    public abstract class Ast
    {
        public string  Name;

    }

    public class LiteralAst : Ast
    {
        public string Value;

        public LiteralAst(string value, string name = null)
        {
            Value = value;
            Name = name ?? Value;
        }


    }

    public class ComposedAst : Ast
    {
        public List<Ast> Value;
        public ComposedAst(string name)
        {
            Name  = name;
            Value = new List<Ast>(); 
            
        }
        
    }
    
    
    public abstract class Parser
    {// Abstract Class for Parser.
        public string Name = null;
        public bool HasRecur = false;

        public abstract Ast Match(string[] unparsedObjs,
                            ref MetaInfo meta,
                            bool partial = false);
    }

    public class RefParser : Parser
    {
        public RefParser(string name)
        {
            Name = name;
        }
        public override Ast Match(string[] unparsedObjs, ref MetaInfo meta, bool partial = true) =>
            throw new ObjectUsageError($"Reference of Ast {Name} cannot be used in this way.");
    }

    public class LiteralParser : Parser
    {
        public Func<string, string> MatchFunc;
        public string tokenRule;
        public bool isRegex;
        public LiteralParser(string literal, string name = null, bool escape = false)
        {
            (tokenRule, MatchFunc) = Tools.RegexMatchFunc(literal, escape);
            isRegex = !escape;
            Name = name ?? tokenRule;
        }

        public override Ast Match(string[] unparsedObjs,
                                ref MetaInfo meta,
                                bool partial = false)
        {
            int left = unparsedObjs.Length - meta.Count;
            if (left == 0) return null;
            string r = MatchFunc(unparsedObjs[meta.Count]);
            if (r == null || (!partial && left != 1))
                return null;
            if (r.Equals("\n"))
                ++meta.Rdx;
            ++meta.Count;
            return new LiteralAst(r, Name);
        }
        public static LiteralParser ELiteral(string regex_literal, string name)=>
          new LiteralParser(regex_literal, name, true);
        
        public class ComposedParser : Parser
        {
            public List<List<Parser>> Possibilities;
            public Parser[][] Cache;
            public bool Compiled = false;

            public ComposedParser(string name = null, params Parser[][] ebnf)
            {
                Cache = ebnf;
                Name = name ?? 
                       string.Join("|",
                           ebnf.Select(possibility => 
                               string.Join(" ", possibility.Select(unit => unit.Name))));
            }

            public override Ast Match(string[] unparsedObjs,
                ref MetaInfo meta,
                bool partial = false)
            {
                var result = new ComposedAst(Name);
                Ast r;
#if DEBUG
                Console.WriteLine($"{Name} With TraceLength {meta.Trace.Count}");
#endif
                foreach (var possibility in Possibilities)
                {   
                    meta.Branch();
                    foreach (var astStruct in possibility)
                    {
                        var history = (astStruct.Name, meta.Count);
                        if (astStruct.HasRecur)
                        {
                                if (meta.Trace.Contains(history))
                                {
#if DEBUG
                                    Console.WriteLine($"Found L-R. Count :{meta.Count}  Name: {astStruct.Name}");
#endif
                                    r = null;
                                }
                                else
                                {
                                    meta.Trace.Push(history);
                                    r = astStruct.Match(unparsedObjs, ref meta);
                                }
                        }
                        else
                        {
#if DEBUG
    meta.Trace.Push(history);
#endif
                            r = astStruct.Match(unparsedObjs, ref meta);
                            
                        }
                        if(r == null)
                        {
                            result.Value.Clear();
                            meta.Rollback();
                            goto NextPossibility;
                        }
                        if (astStruct is SequenceParser)
                        {
                            result.Value.AddRange(((SequenceParser) r).Value);
                        }
                        else
                        {
                            result.Value.Add(r);
                        }
#if DEBUG
                        Console.Write($"{astStruct.Name} << \n{r}");
#endif
                            
                    }
                    goto SuccessfullyParsed;
                    NextPossibility:
                    ;
                }
                return null;
                
                
                SuccessfullyParsed:
                meta.Pull();
                if (partial || meta.Count == unparsedObjs.Length)
                    return result;
                return null;

            }
        }

        public class SequenceParser : ComposedAst
        {
            
        }
        
    }
    
    
}