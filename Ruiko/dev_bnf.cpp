#include "ast.cpp"
#include "flowerq/IO.hpp"

int main(){
    using namespace flowerq;
    Token tk;
    Mixed m;
    m.token_ptr = &tk;
    tk.name = rstr("definition");
    tk.value = rstr("def");
    IO::puts(tk);
}