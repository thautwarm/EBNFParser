//
// Created by misakawa on 18-2-20.
//

#ifndef CFLOWERQ_MATCH_H
#define CFLOWERQ_MATCH_H

namespace cfarfar{

    namespace pattern{
        template <typename T, typename G>
        void match(T &t, G &g, Tuple<T, G> tp){
            t = tp._1;
            g = tp._2;
        };

        template <typename T, typename G, typename ...VARARGS>
        void match(T &t, G &g, Tuple<T, G> tp, VARARGS... args){
            match(t, g, tp);
            match(args...);
        };
    }


}
#endif //CFLOWERQ_DATA_H

