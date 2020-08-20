cmake_minimum_required(VERSION 2.8.12)
project(cmake_wrapper)

message(STATUS "Conan CMake Wrapper")
include(conanbuildinfo.cmake)
conan_basic_setup()

add_definitions("-Wno-nullability-completeness -Wno-nullability-extension -Wno-expansion-to-defined")

add_subdirectory("source_subfolder")
