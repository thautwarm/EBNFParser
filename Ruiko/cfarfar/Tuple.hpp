//
// Created by misakawa on 18-2-21.
//

#ifndef CFLOWERQ_TUPLE_H
#define CFLOWERQ_TUPLE_H

#include <tuple>
namespace cfarfar {
//    template<typename T, typename G>
//    struct Tuple {
//    public:
//        T _1;
//        G _2;
//
//        Tuple(T t, G g) {
//            _1 = t;
//            _2 = g;
//        }
//    };
//
//    template<typename T1,
//            typename T2,
//            typename T3>
//    struct Tuple {
//    public:
//        T1 _1;
//        T2 _2;
//        T3 _3;
//
//        Tuple(T1 _1, T2 _2, T3 _3) {
//            this->_1 = _1;
//            this->_2 = _2;
//            this->_3 = _3;
//        }
//    };

    namespace tuple {
        template<typename V1, typename V2>
        static std::tuple<V1, V2> create(V1 t, V2 g) {
            return std::make_tuple(t, g);
        };
    }
}
#endif //CFLOWERQ_TUPLE_H