// #define UNICODE
#include <iostream>
#include "flowerq/List.hpp"
#include "flowerq/Composite.hpp"
#include "flowerq/IO.hpp"

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
    List<Char> string_ = list::create(rstr('1'), rstr('2'), rstr('3'), rstr('4'));
    IO::putstrln(string_.length());
    IO::putstrln("string here:");
    IO::putstrln(string_);

    // 垃圾推导
    list::create(0, 1, 2).map<int>([&](auto e){ return lst.at(e);}).forEach(IO::puts<int>);
    
    
    // 陈独秀同学你先下来
    std::function<int(int)> f1 = [&](auto e){ return lst.at(e);};
    std::function<void(int)> f2 = IO::puts<int>;
    and_then(f1, f2)(2);
    
    auto writer = IO::open<IO::Writer>("test.txt");
    writer.write(rstr("a ::= b [c [d [e f{2, 3}]]]"));
    writer.close();
    
    auto reader = IO::open<IO::Reader>("test.txt");
    auto s = reader.read();
    IO::puts(s);


    auto xxx = lst;
    IO::putstrln(lst);
    lst = list::create(-1, -1, -1);
    IO::putstrln(xxx);
    IO::putstrln(lst);
    IO::putstrln(lst.zip(lst));
}