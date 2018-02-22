#include "flowerq/List.hpp"
#include "flowerq/IO.hpp"
#include "flowerq/Macro.hpp"
#include <string>
#define DEBUB


class Mixed;
using Ast = flowerq::List<Mixed>;

#ifdef DEBUB
    typedef StringBuff TokenType;
#else
    typedef int TokenType;
#endif

struct Token{

public:
    int lineno;
    int colno;
    TokenType name;
    StringBuff value;
    Token(int lineno, int colno, TokenType name, StringBuff value){
        this->lineno = lineno;
        this->colno = colno;
        this->name = name;
        this->value = value;
    }
    
    StringBuff toString(){
        return flowerq::IO::inspect(this->name) + rstr("[") + flowerq::IO::inspect(this->value) + rstr("]");
    }
    Token() = default;

};

class Mixed{
public:
    Token* token_ptr;
    
    Ast* ast_ptr;
    
    bool is_primitive(){
        return ast_ptr == nullptr;
    }

    StringBuff toString(){
        if (is_primitive()){
            return token_ptr -> toString();
        }
        return ast_ptr -> toString();
    }

    Mixed() = default;
    
};

