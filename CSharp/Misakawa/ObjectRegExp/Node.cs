using System;
using Misakawa;
using System.Collections.Generic;
using System.Linq;


namespace ObjectRegExp
{

    public abstract class Ast
    {
        
        public string  Name;
        public abstract string Dump(int indent = 0);

    }

    public class LiteralAst : Ast
    {
        public readonly string Value;

        public LiteralAst(string value, string name = null)
        {
            Value = value;
            Name = name ?? Value;
        }

        public override string Dump(int indent = 0)
        {
            return Value.Equals("\n")?$@"{Name}[\n]":$"{Name}[Value]";
        }

        public override string ToString()
        {
            return Dump();
        }
    }

    public class ComposedAst : Ast
    {
        public readonly List<Ast> Value;
        public ComposedAst(string name)
        {
            Name  = name;
            Value = new List<Ast>(); 
            
        }

        public override string Dump(int indent = 0)
        {
            string endl = new string(' ', indent);
            int nextIndent = indent + Name.Length + 1;
            string body = string.Join(
                $"\n{new string(' ', nextIndent)}",
                Value.Select( it => it.Dump(nextIndent))
            );
            return $"{Name}[{body}\n{endl}]";
        }
        public override string ToString()
        {
            return Dump(0);
        }
    }
    
    
    public abstract class Parser
    {// Abstract Class for Parser.
        public string Name;
        public bool HasRecur = false;

        public abstract Ast Match(string[] unparsedObjs,
                            ref MetaInfo meta,
                            bool partial = false);

        public abstract void Compile(
            ref Dictionary<string, Parser> NameSpace,
            ref HashSet<string> recurSearcher);
    }

    public class RefParser : Parser
    {
        public RefParser(string name)
        {
            Name = name;
        }

        public override void Compile(
            ref Dictionary<string, Parser> NameSpace,
            ref HashSet<string> recurSearcher)
        { throw  new ObjectUsageError("ReferenceParser shouldn't be compiled!");}
        
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
        public override void Compile(
            ref Dictionary<string, Parser> NameSpace,
            ref HashSet<string> recurSearcher)
        { throw  new ObjectUsageError("LiteralParser shouldn't be compiled!");}
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
            public bool Compiled;

            public override void Compile(
                ref Dictionary<string, Parser> nameSpace,
                ref HashSet<string> recurSearcher
                )
            {
                if (nameSpace == null) throw new ArgumentNullException(nameof(nameSpace));
                if (recurSearcher == null) throw new ArgumentNullException(nameof(recurSearcher));
                
                if (recurSearcher.Contains(Name))
                {
                    HasRecur = true;
                    Compiled = true;
                }
                else
                {
                    recurSearcher.Add(Name);
                }
                if (Compiled) return;
                
                foreach (var es in Cache)
                {
                    var Possibility = new List<Parser>();
                    foreach (var e in es)
                    {
                        switch (e)
                        {
                            case LiteralParser _:
                            {
                                Possibility.Add(e);
                                break;
                            }
                            case RefParser _:
                            {
                                var refered = (ComposedParser) nameSpace[e.Name];
                                refered.Compile(ref nameSpace,
                                                ref recurSearcher);
                                Possibility.Add(refered);
                                if (refered.HasRecur)
                                    HasRecur = true;
                                break;
                            }
                            case ComposedParser _:
                            {
                                Parser refered = nameSpace.ContainsKey(e.Name) ? nameSpace[e.Name] : e;
                                refered.Compile(ref nameSpace, ref recurSearcher);
                                Possibility.Add(refered);
                                if (refered.HasRecur)
                                    HasRecur = true;
                                break;
                            }
                             default:
                                 throw new UnsolvedError("Unknown Parser Type.");
                        }
                    }
                }
#if DEBUG
     if (HasRecur) Console.WriteLine($"Found recursive Parser `{Name}`.");    
#endif
                Cache = null;
                if (!Compiled) Compiled = true;

            }
            
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
#if DEBUG
                Console.WriteLine($"{Name} With TraceLength {meta.Trace.Count}"); // incomplete Trace.print
#endif
                foreach (var possibility in Possibilities)
                {   
                    meta.Branch();
                    foreach (var astStruct in possibility)
                    {
                        var history = (astStruct.Name, meta.Count);
                        Ast r;
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
                            result.Value.AddRange(((ComposedAst) r).Value);
                        }
                        else
                        {
                            result.Value.Add(r);
                        }
#if DEBUG
                        Console.Write($"{astStruct.Name} << \n {r}  "); 
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

        public class SequenceParser : ComposedParser
        {
            private readonly int _atLeast;
            private readonly int _atMost  = -1;

            
            
            public SequenceParser(
                int atleast = 0,
                int atmost = -1,
                string name = null,
                params Parser[][] ebnf) : base(name, ebnf)
            {
                _atLeast = atleast;
                _atMost = atmost;
                if (_atMost < 0)
                {
                    Name = _atLeast == 0 ? $"({Name})*" : $"({Name}){{{_atLeast}}}";
                }
                else
                    Name = $"({Name}){{{_atLeast} {_atMost}}}";
            }

            public override Ast Match(
                string[] unparsedObjs,
                ref MetaInfo meta,
                bool partial = false)
            {
                var result = new ComposedAst(Name);
                var left = unparsedObjs.Length - meta.Count;
                if (left == 0)
                    return _atLeast == 0 ? result : null;
                meta.Branch();
                Ast r;
                int sequenceLengthRecord;
                if (_atMost>0)
                    while (true)
                    {
                        if (sequenceLengthRecord >= _atMost) break;
                        r = base.Match(unparsedObjs, ref meta);
                        if (r == null) break;
                        result.Value.AddRange(((ComposedAst) r).Value);
                        ++sequenceLengthRecord;

                    }
                else
                    while (true)
                    {
                        r = base.Match(unparsedObjs, ref meta);
                        if (r == null) break;
                        result.Value.AddRange(((ComposedAst) r).Value);
                        ++sequenceLengthRecord;
                    }
#if DEBUG
                 Console.WriteLine($"{Name} <= res.Dump() //Dump明儿写 ");
#endif
                if (sequenceLengthRecord < _atLeast)
                {
                    meta.Rollback();
                    return null;
                }
                meta.Pull();
                return result;
            }
            
            
        }
        
    }
    
    
}