//
// Created by misakawa on 18-2-21.
//

#ifndef CFLOWERQ_TUPLE_H
#define CFLOWERQ_TUPLE_H


namespace cfarfar {
    template<typename T, typename G>
    struct Tuple {
    public:
        T _1;
        G _2;

        Tuple(T t, G g) {
            _1 = t;
            _2 = g;
        }
    };
    namespace tuple {
        template<typename V1, typename V2>
        static Tuple<V1, V2> create(V1 t, V2 g) {
            return Tuple<V1, V2>(t, g);
        };
    }
}
#endif //CFLOWERQ_TUPLE_H