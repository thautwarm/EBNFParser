/*
#ifndef FLOWERQ_COMP
    #include "Composite.hpp"
#endif
*/
#ifndef FLOWERQ_COMP
#define FLOWERQ_COMP
#include <functional>

namespace flowerq{


    template<typename T, typename G>
    std::function<void(T)> and_then(std::function<T(G)> f1, std::function<void(G)> f2){
        return [=](T input){
            f2(f1(input));
        };
    }

    // template<typename T, typename G, typename R>
    // auto and_then(std::function<T(G)> f1, std::function<R(G)> f2){
    //     return [=](T input){
    //         return f2(f1(input));
    //     };
    // }


}

#endif