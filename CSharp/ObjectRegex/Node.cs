using System.Text.RegularExpressions;
using System;
using System.Runtime.Serialization;
using System.Linq;
using System.Collections.Generic;
using System.Collections;
namespace CSharp.ObjectRegex
{
    
    public class ObjRegexError : Exception
    {
        public ObjRegexError(string info) : base(info)
        {
        }
    }

    public class RegexTool{
         
        public static Tuple<string, Func<string, string>> reMatch(string a, bool escape = false){
            var token_rule = escape?Regex.Escape(a):a;
        
            var re_        = new Regex( token_rule );
           
            return new Tuple<string, Func<string, string>>
                    (token_rule,
                     (string str)=>{
                        if (str.Length==0)
                            return null;
                        var r = re_.Match(str);
                        if (r.Index !=0)
                            throw new ObjRegexError("empty tokenized word.");
                        if (r.Length!=str.Length)
                            return null;
                        return str;
                        }
                    );
        } 
    } 
    public class Mode :List<Mode>{
        
        
        public string name = null;
        public string value= null;
    
        public Mode setName(string name){
            this.name = name;
            return this;
        } 
        public Mode setValue(string value){
            this.value = value;
            return this;
        }
  
        public string Dump(int i=0){
            var space = "\n"+new String(' ', i);
            var toDump = string.Join("", 
                this.Select(
                    mode =>{
                        if (mode.value != null){
                            if (mode.value.Equals("\n")){
                                return $"{mode.name}[{@"\n"}]";
                            }
                            return $"{mode.name}[{mode.value}]";
                        }
                        else{
                            
                            return mode.Dump(i+1);
                        }
                            
                    }
            ));
            return $"{this.name}[{toDump+space}]";
        }
    }

    public class MetaInfo{
        public int count = 0;
        public int rdx = 0;
        

    };
    public class Liter{
        public string token_rule;
        public string name;
        public bool   has_recur;
        public Func<string, string> f;


        public Liter(string i, string name = null, bool escape = false ){

            var (token_rule, f) = RegexTool.reMatch(i, escape);
            this.name = name;
            this.has_recur = false;
            this.token_rule = token_rule;
            this.f = f;
        }
        public Mode Match(string[] objs, MetaInfo meta = null, bool partial = true){
            if (meta==null){
                meta = new MetaInfo();
            }
            int left = objs.Length - meta.count ;
            if (left==0) return null;
            var r = f(objs[meta.count]);  
            if ( r == null || ( (!partial)&&(left !=1 ))){
                    return null;
            }
            if (r == "\n")
                meta.rdx += 1;
            meta.count += 1;
            return new Mode().setName(this.name).setValue(r);
        }
        public Liter ELiter(string i, string name = null){
            return new Liter(i, name, true);
        }
    }
    
    

}