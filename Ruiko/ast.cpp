#include "flowerq/List.hpp"
#include "flowerq/IO.hpp"
#include <string>
#define DEBUB


class Mixed;
using Ast = flowerq::List<Mixed>;

#ifdef DEBUB
    typedef std::string TokenType;
#else
    typedef int TokenType;
#endif

struct Token{

public:
    int lineno;
    int colno;
    TokenType name;
    std::string value;
    Token(int lineno, int colno, TokenType name, std::string value){
        this->lineno = lineno;
        this->colno = colno;
        this->name = name;
        this->value = value;
    }
    
    std::string to_string(){
        return flowerq::IO::inspect(this->name) + "[" + flowerq::IO::inspect(this->value) + "]";
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

    std::string to_string(){
        if (is_primitive()){
            return token_ptr -> to_string();
        }
        return ast_ptr -> to_string();
    }

    Mixed() = default;
    
};

