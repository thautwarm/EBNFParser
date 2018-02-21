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
        inspect(const char *buf) {
            if (buf == NULL)
                return ""; //TODO: not sure how to handle the null value.
            std::string s(buf);
            return s;
        }

        std::string
        inspect(char *buf) {
            if (buf == NULL)
                return ""; //TODO: not sure how to handle the null value.
            std::string s(buf);
            return s;
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


        std::string
        inspect(bool e) {
            return e ? "true" : "false";
        }

        template<typename T>
        std::string _inspect(std::tuple<T> tp) {
            return inspect(std::get<0>(tp));
        }

        template<typename T, typename ...VARARGS>
        std::string _inspect(std::tuple<T, VARARGS...> tp) {
            return inspect(std::get<0>(tp)) + ", " + _inspect(dependency::tail(tp));
        }

        template<typename T>
        std::string inspect(std::tuple<T> tp) {
            return "(" + inspect(std::get<0>(tp)) + ",)";
        }

        template<typename ...VARARGS>
        std::string inspect(std::tuple<VARARGS...> tp) {
            return "(" + _inspect(tp) + ")";
        }


        template<typename T>
        std::string inspect(List<T> list) {

            const int n = list.len();
            if (n == 0) {
                return "List<0>[]";
            }

            T head;
            List<T> tail;
            auto tp = list.destruct();
            pattern::match(tp, head, tail);
            std::string res = "List<" + std::to_string(list.len()) + ">[" + inspect(head);
            tail.forEach([=, &res](T e) {
                res += ", " + inspect(e);
            });
            return res + "]";
        }

        template<typename T>
        void puts(T t) {

            std::string res = inspect(t);
            std::cout << res << '\t';
        }

        template<typename T>
        void putstrln(T t) {

            std::string res = inspect(t);
            std::cout << res << std::endl;
        }

        void putstrln() {
            printf("\n");
        }
    }

}

#endif //CFLOWERQ_IO_H
