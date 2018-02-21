#include "ast.cpp"
#include "flowerq/IO.hpp"

int main(){
    using namespace flowerq;
    Token tk;
    Mixed m;
    m.token_ptr = &tk;
    tk.name = "definition";
    tk.value = "def";
    IO::puts(tk);
}