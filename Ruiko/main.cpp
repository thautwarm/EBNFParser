// #define UNICODE
#include <iostream>
#include "flowerq/List.hpp"
#include "flowerq/Str.hpp"

int main() {
    #ifdef UNICODE
        setlocale(LC_ALL,"");
    #endif
    using namespace flowerq;
    
    // IO::putstrln(list::create(1, 2, 3, 4, 5));
    
    auto lst = list::create(1, 2, 3, 4, 5);

    // IO::putstrln(list::create(list::create(1, 2, 3, 5), list::create(2, 3, 4)));
    // IO::putstrln(std::make_tuple(lst));
    IO::putstrln(lst.destruct());

    auto new_lst = list::cons(2, lst);
    
    IO::putstrln(new_lst.map<int>([=](int e){return e+1;}).filter([=](int e){return e%2==0;}));


    auto lst2 = list::create<int>();


    IO::putstrln(new_lst);

    IO::putstrln(new_lst.tail());


    IO::putstrln(new_lst.reduce<int>([=](int a, int b){return a+b;}, 0));

    IO::putstrln(lst);
    IO::putstrln(lst.at(2));
    IO::putstrln(lst);

    IO::putstrln();
    flowerq::Str mstr(rstr("花Q!"));
    IO::putstrln(mstr);
    IO::putstrln(mstr.length());


    auto xxx = lst;

    IO::putstrln(lst);
    lst = list::create(-1, -1, -1);

    IO::putstrln(xxx);
    IO::putstrln(lst);

    flowerq::Str str2 = rstr("12345");
    IO::putstrln(str2);
    auto ccc = zip(str2, str2);
    IO::putstrln(str2.zip(str2));
}