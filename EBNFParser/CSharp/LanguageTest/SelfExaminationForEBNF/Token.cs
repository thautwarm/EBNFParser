using CSharp.ObjectRegex;
using System.Text.RegularExpressions;
namespace CSharp.LanguageTest.SelfExaminationForEBNF
{
    public class DefualtToken
    {
        
        public static Liter Name   = new Liter("[a-zA-Z_][a-zA-Z0-9]*", "Name");
        public static Liter Number = new Liter(@"\d+", "Number");
        public static Liter Str    = new Liter(@"[R]{0,1}'[\w|\W]*?'","Str");
        public static Liter NEWLINE=new Liter("\n", "NEWLINE");

        public static Liter LBB    = Liter.ELiter("{","LBB");
        public static Liter LB     = Liter.ELiter("[","LB");
        public static Liter LP     = Liter.ELiter("(","LP");
        
        public static Liter RBB    = Liter.ELiter("}","RBB");
        public static Liter RB     = Liter.ELiter("]","RB");
        public static Liter RP     = Liter.ELiter(")","RP");

        public static Liter SeqStar= Liter.ELiter("*", "SeqStar");
        public static Liter SeqPlus= Liter.ELiter("+", "SeqPlus");
        public static Liter Def    = Liter.ELiter("::=", "Def");
        public static Liter OrSign = Liter.ELiter("|", "OrSign");

        public static Regex Token(){
            var re = new Regex(
                string.Join("|",
                new string[]{
                    Name.token_rule,
                    Number.token_rule,
                    Str.token_rule,
                    NEWLINE.token_rule,
                    LBB.token_rule,
                    RBB.token_rule,
                    LP.token_rule,
                    RP.token_rule,
                    LB.token_rule,
                    RB.token_rule,
                    SeqPlus.token_rule,
                    SeqStar.token_rule,
                    Def.token_rule,
                    OrSign.token_rule
                })
            );
            return re;
        }


        
    }
}