/*
#ifndef FLOWERQ_MATCH
    #include "Match.hpp"
#endif
*/
#ifndef FLOWERQ_MATCH
#define FLOWERQ_MATCH
#include <tuple>
#include <utility>

namespace flowerq {
    namespace dependency {

        /// reference:
        ///  url   : https://stackoverflow.com/questions/10626856/how-to-split-a-tuple
        ///  author: André Bergner

       

        template<std::size_t... Ns, typename... Ts>
        auto tail_impl(std::index_sequence<Ns...>, std::tuple<Ts...> t) {
            return std::make_tuple(std::get<Ns + 1u>(t)...);
        }

        template<typename... Ts>
        auto tail(std::tuple<Ts...> t) {
            return tail_impl(std::make_index_sequence<sizeof...(Ts) - 1u>(), t);
        }

        template<std::size_t... Ns, typename... Ts>
        auto tail2_impl(std::index_sequence<Ns...>, std::tuple<Ts...> t) {
            return std::make_tuple(std::get<Ns + 2u>(t)...);
        }

        template<typename... Ts>
        auto tail2(std::tuple<Ts...> t){
            return tail_impl(std::make_index_sequence<sizeof...(Ts) - 2u>(), t);
        }
    }

    namespace pattern {

        template<typename T, typename G>
        void match(std::tuple<T, G> tp, T &t, G &g) {
            t = std::get<0>(tp);
            g = std::get<1>(tp);
        }

        template<typename T, typename ...VARARGS>
        void match(std::tuple<T, VARARGS...> tp, T &t, VARARGS &... args) {
            t = std::get<0>(tp);
            match(dependency::tail(tp), args...);
        }

        template<typename T>
        void match(std::tuple<T> tp, T &t) {
            t = std::get<0>(tp);
        }
    }
}
#endif
