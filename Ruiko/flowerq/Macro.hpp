/*
#ifndef FLOWERQ_MACRO
    #include "Macro.hpp"
#endif
*/
#ifndef FLOWERQ_MACRO
#define FLOWERQ_MACRO
#include <string>
#include <cstring>
#include <iostream>
#include <fstream>
#ifdef UNICODE

    #define rstr(src) L ## src
    using Char = wchar_t;
    using  ofstream = std::wofstream;
    using  ifstream = std::wifstream;
    using  fstream = std::wfstream;
    static std::wostream& cout = std::wcout;
    static auto str_len = std::wcslen;
    typedef std::wstring StringBuff;
    template<typename T>
    static StringBuff to_string(T t){
        return std::to_wstring(t);
    }
    // #define __FLOWER_MACRO_GETBUFFLEN__ std::wcslen
    // #define __FLOWER_MACRO_TO_BUFF__ std::to_wstring
#else
    #define rstr(src) src
    using Char = char;
    using  ofstream = std::ofstream;
    using  ifstream = std::ifstream;
    using  fstream = std::fstream;
    static std::ostream& cout = std::cout;
    static auto str_len = std::strlen;
    typedef std::string StringBuff;
    template<typename T>
    static StringBuff to_string(T t){
        return std::to_string(t);
    }
#endif
#endif