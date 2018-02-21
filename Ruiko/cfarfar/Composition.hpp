//
// Created by misakawa on 18-2-21.
//

#ifndef CFLOWERQ_COMPOSITION_H
#define CFLOWERQ_COMPOSITION_H

namespace cfarfar {
    namespace comp {
        template<typename T, typename G, typename N>
        std::function<N(T)> and_then(std::function<G(T)> first, std::function<N(G)> then) {
            return [=](T t) { return then(first(t)); };
        }
    }
}

#endif //CFLOWERQ_COMPOSITION_H
