#include "Include/List.hpp"
#include "Include/Match.hpp"
#include "Include/IO.hpp"


int double_it(int e) {
    return e + 1;
}

int main() {
    auto x = cfarfar::list::create(1, 2, 3);
    auto z = cfarfar::list::create<int>();
    auto println = [=](int e) { std::cout << e << std::endl; };

    x.forEach([=](int e) {
        std::cout << e << std::endl;
    });

    x.map<int>([=](int e) -> int {
        return e * 2;
    }).forEach(println);
    int a;

    cfarfar::List<int> b;

    cfarfar::pattern::match(a, b, x.destruct());
    println(a);
    b.forEach(println);

    cfarfar::list::create(x);

    x.forEach(println);
//
    x = cfarfar::list::create(1, 2, 3, 4, 5);

    auto zipped = x.zip(x.map<int>(double_it));
    zipped.forEach([=](cfarfar::Tuple<int, int> i) {
        std::cout << i._2 * i._1 << std::endl;
    });

    std::cout << "reduced:" << std::endl;
    println(x.reduce<int>([=](int s1, int s2) { return s1 + s2; }, 0));
    cfarfar::IO::puts(x);
    cfarfar::IO::puts(z);
    cfarfar::IO::puts(zipped);

}