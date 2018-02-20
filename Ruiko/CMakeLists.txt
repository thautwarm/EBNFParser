cmake_minimum_required(VERSION 3.8)
project(cflowerq)

set(CMAKE_CXX_STANDARD 14)
list(APPEND CMAKE_LIBRARY_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Lib)
list(APPEND CMAKE_INCLUDE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Include)
set(SOURCE_FILES main.cpp Lib/List.cpp Include/Match.hpp Lib/Data.cpp Include/List.hpp Include/Tuple.hpp Include/IO.hpp Include/Composition.hpp)
add_executable(cflowerq ${SOURCE_FILES})