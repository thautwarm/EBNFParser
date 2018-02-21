cmake_minimum_required(VERSION 3.8)
project(cflowerq)

set(CMAKE_CXX_STANDARD 14)
list(APPEND CMAKE_LIBRARY_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Lib)
list(APPEND CMAKE_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cfarfar)
set(SOURCE_FILES main.cpp cfarfar/Match.hpp cfarfar/List.hpp cfarfar/Tuple.hpp cfarfar/IO.hpp cfarfar/Composition.hpp)
add_executable(cflowerq ${SOURCE_FILES})