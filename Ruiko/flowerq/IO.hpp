/*
#ifndef FLOWERQ_IO
    #include "IO.hpp"
#endif
*/
#ifndef FLOWERQ_IO
#define FLOWERQ_IO

#ifndef FLOWERQ_MATCH
    #include "Match.hpp"
#endif

#include <iostream>
#include <tuple>
#include <string>
namespace flowerq{

    namespace IO{

        

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
        std::string inspect(T t);
        
        
        template<typename T>
        std::string tuple_inspect(std::tuple<T> tp){
            return inspect<T>(std::get<0> (tp));
        }

        template<typename T, typename G>
        std::string tuple_inspect(std::tuple<T, G> tp){
            return inspect<T>(std::get<0> (tp)) + ", " + inspect<G>(std::get<1> (tp));
        }

        template<typename T, typename... VARARGS>
        std::string tuple_inspect(std::tuple<T, VARARGS...> tp){
            return inspect<T>(std::get<0> (tp)) + ", " + tuple_inspect(dependency::tail(tp));
        }

        template<typename T>
        std::string inspect(std::tuple<T> tp) {
            return "(" + tuple_inspect(tp) + ",)";
        }

        template<typename ...VARARGS>
        std::string inspect(std::tuple<VARARGS...> tp) {
            return "(" + tuple_inspect(tp) + ")";
        }
        
        template<typename T>
        std::string inspect(T lst) {
            return lst.to_string();
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
#endif