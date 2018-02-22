
/*
#ifndef FLOWERQ_STR
    #include "Str.hpp"
#endif
*/
#ifndef FLOWERQ_STR
#define FLOWERQ_STR

#include "List.hpp"
#include "Macro.hpp"

namespace flowerq{
    class Str: public List<Char>{
        friend class List<Char>;
        public:

        Str(const Char* &&s){
            size_t n = str_len(s);
            
            auto cursur = this->head_ptr = Node<Char>::_new_head(n);
            for(int i=0; i < n; ++i){
                cursur->Next = new Node<Char>(s[i]);
                cursur = cursur->Next;
            }
            cursur -> Next = nullptr;
        }

        StringBuff toString(){
            Char *buffer = new Char[length()];
            int idx = 0;
            forEach([&](Char& ch){
                buffer[idx++] = ch;
            });
            return buffer;
        }
    };
}
#endif