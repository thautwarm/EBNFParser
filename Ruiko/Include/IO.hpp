//
// Created by misakawa on 18-2-21.
//

#ifndef CFLOWERQ_IO_H
#define CFLOWERQ_IO_H
#ifndef CFLOWERQ_COMPOSITION_H

#include "string"
#include "Composition.hpp"

#endif

namespace cfarfar {
    namespace IO {

        std::string
        inspect(int e) {
            return std::to_string(e);
        }

        std::string
        inspect(float e) {
            return std::to_string(e);
        }

        std::string
        inspect(double e) {
            return std::to_string(e);
        }

        std::string
        inspect(std::string e) {
            return e;
        }

        template<typename T, typename G>
        std::string inspect(Tuple<T, G> tp) {
            return "(" + inspect(tp._1) + ", " + inspect(tp._2) + ")";
        };

        template<typename T>
        std::string inspect(List<T> list) {
            std::string res = "List[" + std::to_string(list.len()) + "]";
            list.forEach([=, &res](T e) {
                res += ", " + inspect(e);
            });
            return "[" + res + "]";
        }


        template<typename T>
        void puts(T t) {
            std::string res = inspect(t);
            std::cout << res << std::endl;
        }
    }

}

#endif //CFLOWERQ_IO_H
