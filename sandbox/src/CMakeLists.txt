cmake_minimum_required(VERSION 3.10)

# set the project name
project(myapp VERSION 1.0.0)

# add the executable
add_executable(myapp main.cpp)

set(CMAKE_CXX_FLAGS "")
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
