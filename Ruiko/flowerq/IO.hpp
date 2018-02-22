/*
#ifndef FLOWERQ_IO
    #include "IO.hpp"
#endif
*/
#ifndef FLOWERQ_IO
#define FLOWERQ_IO

#include "Match.hpp"
#include "Macro.hpp"
#include <iostream>
#include <tuple>
namespace flowerq{

    namespace IO{

        StringBuff
        inspect(int e) {
            return to_string(e);
        }

        StringBuff
        inspect(Char e) {
            return to_string(e);
        }


        StringBuff
        inspect(const Char *buf) {
            if (buf == NULL){
                //TODO: not sure how to handle the null value.
                return rstr("");
            }
            StringBuff s(buf);
            return s;
        }

        StringBuff
        inspect(Char *buf) {
            if (buf == NULL){
                //TODO: not sure how to handle the null value.
                return rstr("");
            }
            StringBuff s(buf);
            return s;
        }

        StringBuff
        inspect(float e) {
            return to_string(e);
        }

        StringBuff
        inspect(double e) {
            return to_string(e);
        }

        StringBuff
        inspect(std::string e) {
            #ifdef UNICODE
                StringBuff ws;
                ws.assign(e.begin(), e.end());
                return ws;
            #else
                return e;
            #endif
        }

        StringBuff
        inspect(std::wstring e){
            #ifndef UNICODE
                StringBuff s;
                s.assign(e.begin(), e.end());
                return s;
            #else
                return e;
            #endif
        }


        StringBuff
        inspect(bool e) {
            return e ? rstr("true") : rstr("false");
   
        }

        template<typename T>
        StringBuff inspect(T t);
        
        
        template<typename T>
        StringBuff tuple_inspect(std::tuple<T> tp){
            return inspect<T>(std::get<0> (tp));
        }

        template<typename T, typename G>
        StringBuff tuple_inspect(std::tuple<T, G> tp){
            return inspect(std::get<0> (tp)) + rstr(", ") + inspect(std::get<1> (tp));
        }

        template<typename T, typename... VARARGS>
        StringBuff tuple_inspect(std::tuple<T, VARARGS...> tp){
            return inspect<T>(std::get<0> (tp)) + rstr(", ") + tuple_inspect<VARARGS...>(dependency::tail(tp));
        }

        template<typename T>
        StringBuff inspect(std::tuple<T> tp) {
            return rstr("(") + tuple_inspect(tp) + rstr(",)");
        }

        template<typename ...VARARGS>
        StringBuff inspect(std::tuple<VARARGS...> tp) {
            return rstr("(") + tuple_inspect<VARARGS...>(tp) + rstr(")");
        }
        
        template<typename T>
        StringBuff inspect(T t) {
            return t.toString();
        }

        template<typename T>
        void puts(T t) {
            StringBuff res = inspect(t);
            cout << res << '\t';
        }
        

        template<typename T>
        void putstrln(T t) {
            StringBuff res = inspect(t);
            cout << res << std::endl;
        }

        void putstrln() {
            printf("\n");
        }
     }
}
#endif