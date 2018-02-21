#include "cfarfar/List.hpp"
#include "cfarfar/Match.hpp"
#include "cfarfar/IO.hpp"


int double_it(int e) {
    return e + 1;
}


int main() {
    auto x = cfarfar::list::create(1, 2, 3);
    auto z = cfarfar::list::create<int>();

    cfarfar::IO::putstrln("foreach");
    x.forEach(cfarfar::IO::puts<int>);
    cfarfar::IO::putstrln();

    auto mapped = x.map<int>([=](int e) -> int {
        return e * 2;
    });
    cfarfar::IO::putstrln("mapped");
    cfarfar::IO::putstrln(mapped);

    int a;
    cfarfar::IO::putstrln("pattern matching:");
    cfarfar::List<int> b;
    cfarfar::pattern::match(x.destruct(), a, b);
    cfarfar::IO::putstrln(a);
    cfarfar::IO::putstrln(b);
    cfarfar::IO::putstrln("end pattern matching:");

    cfarfar::List<cfarfar::List<int>> xx = cfarfar::list::create(x);
    cfarfar::IO::putstrln(xx);

//
    x = cfarfar::list::create(1, 2, 3, 4, 5);

    auto zipped = x.zip(x.map<int>(double_it));
    std::cout << "reduced:" << std::endl;
    cfarfar::IO::putstrln(x.reduce<int>([=](int s1, int s2) { return s1 + s2; }, 0));
    cfarfar::IO::putstrln("zipped:");
    cfarfar::IO::puts(zipped);

    std::tuple<int, std::string, cfarfar::List<int>> tp2 = std::make_tuple(1, "123", x);
    int t1;
    std::string t2;
    cfarfar::List<int> t3;
    cfarfar::pattern::match<int, std::string, cfarfar::List<int>>(tp2, t1, t2, t3);

    cfarfar::IO::putstrln("matched:");
    cfarfar::IO::puts(t1);
    cfarfar::IO::puts(t2);
    cfarfar::IO::putstrln(t3);

    cfarfar::del(x);
    cfarfar::del(z);

    cfarfar::IO::putstrln(std::make_tuple(1, 2, 3));
    cfarfar::IO::putstrln(std::make_tuple(1));
}