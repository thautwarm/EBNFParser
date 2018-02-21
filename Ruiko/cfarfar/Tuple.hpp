//
// Created by misakawa on 18-2-21.
//

#ifndef CFLOWERQ_TUPLE_H
#define CFLOWERQ_TUPLE_H

#include <tuple>

namespace cfarfar {

    namespace tuple {
        template<typename V1, typename V2>
        static std::tuple<V1, V2> create(V1 t, V2 g) {
            return std::make_tuple(t, g);
        };
    }
}
#endif //CFLOWERQ_TUPLE_H