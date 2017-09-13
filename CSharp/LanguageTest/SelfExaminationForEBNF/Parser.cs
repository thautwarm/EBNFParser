using System.Collections;
using System.Collections.Generic;
using CSharp.ObjectRegex;
using System;
namespace CSharp.LanguageTest.SelfExaminationForEBNF
{
    public class Parser
    {
        public Ast Expr ;
        public Ast Or;
        public Ast SPLIT;
        public Ast Atom;
        public Ast AtomExpr;
        public Ast Eq;
        public Ast Stmt;
        public Ast Trailer;
        public Dictionary<string, Ast> compile_closure;
        public Parser(Ast Expr, Ast Or, Ast SPLIT,
                      Ast Atom, Ast AtomExpr,
                      Ast Eq,   Ast Stmt,
                      Ast Trailer,
                      Dictionary<string, Ast> compile_closure
                      ){
                this.Expr = Expr;
                this.Or   = Or;
                this.SPLIT= SPLIT;
                this.Atom = Atom;
                this.Eq   = Eq;
                this.AtomExpr=AtomExpr;
                this.Stmt = Stmt;
                this.Trailer = Trailer;
                this.compile_closure = compile_closure;

        }
        
        public static Parser GenParser(){
            var compile_closure = new Dictionary<string, Ast>();
            var Expr = new Ast(
                compile_closure:ref compile_closure,
                name:"Expr",
                ebnf: new BaseAst[]{
                    new Seq(
                        compile_closure:ref compile_closure,
                        atleast:0,
                        name:"Or+",
                        ebnf:new BaseAst[]{
                            new LazyDef("Or")
                        }
                    )
                }
            );

            var Or = new Ast(
                compile_closure:ref compile_closure,
                name:"Or",
                ebnf:new BaseAst[]{
                    new LazyDef("AtomExpr"),
                    new Seq(
                        compile_closure:ref compile_closure,
                        atleast:0,
                        name:"('|' AtomExpr)*",
                        ebnf:new BaseAst[]{
                            DefualtToken.OrSign,
                            new LazyDef("AtomExpr")
                        }
                    )
                }
            );
            var AtomExpr = new Ast(
                compile_closure:ref compile_closure,
                name:"AtomExpr",
                ebnf:new BaseAst[]{
                    new LazyDef("Atom"),
                    new LazyDef("Trailer")
                }
            );
            var Trailer = new Seq(
                compile_closure:ref compile_closure,
                name:"Trailer",
                atleast:0,
                ebnf:new BaseAst[][]{
                    new BaseAst[]{
                        DefualtToken.SeqStar
                    }, 
                    new BaseAst[]{
                        DefualtToken.SeqPlus
                    },
                    new BaseAst[]{
                        DefualtToken.LBB,
                        new Seq(
                            compile_closure:ref compile_closure,
                            atleast:1,
                            atmost:2,
                            name:"Number{1 2}",
                            ebnf: new BaseAst[]{
                                DefualtToken.Number
                            }),
                        DefualtToken.RBB
                    }
                }
            );
            var Atom = new Ast(
                compile_closure:ref compile_closure,
                name:"Atom",
                ebnf:new BaseAst[][]{
                    new BaseAst[]{
                        DefualtToken.Name
                    },
                    new BaseAst[]{
                        DefualtToken.Str
                    },
                    new BaseAst[]{
                        DefualtToken.LB,
                        new LazyDef("Expr"),
                        DefualtToken.RB
                    },
                    new BaseAst[]{
                        DefualtToken.LP,
                        new LazyDef("Expr"),
                        DefualtToken.RP
                    }
                }
            );
            var Eq = new Ast(
                compile_closure:ref compile_closure,
                name:"Eq",
                ebnf:new BaseAst[]{
                    DefualtToken.Name,
                    DefualtToken.Def,
                    new LazyDef("Expr")
                }
            );
            var Stmt = new Ast(
                compile_closure:ref compile_closure,
                name:"Stmt",
                ebnf:new BaseAst[]{
                    new Seq(
                        compile_closure:ref compile_closure,
                        name:"Eq*",
                        atleast:0,
                        ebnf:new BaseAst[]{
                            new LazyDef("SPLIT"),
                            new LazyDef("Eq"),
                            new LazyDef("SPLIT"),
                        }
                    )
                }
            );
            var SPLIT = new Seq(
                compile_closure: ref compile_closure,
                name:"SPLIT",
                atleast:0,
                ebnf:new BaseAst[]{
                    DefualtToken.NEWLINE
                }
            );
            var namestore = new HashSet<string>();
            SPLIT.compile(ref namestore);
            Stmt.compile(ref namestore);
                
            return new Parser(
                Expr:Expr,
                Atom:Atom,
                Eq:Eq,
                Or:Or,
                Stmt:Stmt,
                AtomExpr:AtomExpr,
                Trailer:Trailer,
                SPLIT:SPLIT,
                compile_closure:compile_closure
            );

        }
        
        
         
        
    }
}