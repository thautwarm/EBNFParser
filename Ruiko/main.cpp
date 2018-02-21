#include <iostream>
#include "flowerq/List.hpp"

int main() {
    using namespace flowerq;

    // IO::putstrln(list::create(1, 2, 3, 4, 5));
    
    auto lst = list::create(1, 2, 3, 4, 5);

    // IO::putstrln(list::create(list::create(1, 2, 3, 5), list::create(2, 3, 4)));
    // IO::putstrln(std::make_tuple(lst));
    IO::putstrln(lst.destruct());

    // auto new_lst = list::cons(lst, 2);
    
    // IO::putstrln(new_lst.map<int>([=](int e){return e+1;}).filter([=](int e){return e%2==0;}));


    // auto lst2 = list::create<int>();


    // IO::putstrln(new_lst);

    // IO::putstrln(new_lst.tail());


    // IO::putstrln(new_lst.reduce<int>([=](int a, int b){return a+b;}, 0));

}