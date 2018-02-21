/*
#ifndef FLOWERQ_TRAITS
    #include "Traits.hpp"
#endif
*/

#ifndef FLOWERQ_TRAITS
#define FLOWERQ_TRAITS
#include "iostream"
#include "string"

namespace flowerq::traits{

    template <typename T>

    class Representable{
        typedef int yes;
        typedef int no;

        template <typename C> static yes test(decltype(&C::to_string));
        template <typename C> static no  test(...);    

    public:
        const static bool value = sizeof(test<T>(0)) == sizeof(yes);
    };

        /*
        template<typename R>
        typename std::enable_if<Representable<R>::value, std::string>::type
        funcname(){

        }
        */

}
#endif
