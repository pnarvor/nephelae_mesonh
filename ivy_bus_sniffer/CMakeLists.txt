cmake_minimum_required(VERSION 3.5)
project(ivy_bus_tests VERSION 0.1)

set(CMAKE_CXX_STANDARD 11)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(Ivy_C REQUIRED)
find_package(Threads REQUIRED)

add_executable(ivyprobe_test
    src/main_ivyprobe.cpp
)
target_link_libraries(ivyprobe_test
    Ivy_C
)

add_executable(pprz_sink_test
    src/main_pprz_sink_test.cpp
)
target_link_libraries(pprz_sink_test
    Ivy_C
)

add_executable(pprz_send_test
    src/main_pprz_send_test.cpp
)
target_link_libraries(pprz_send_test
    Ivy_C
    Threads::Threads
)
add_executable(pprz_find_aircrafts
    src/main_pprz_find_aircrafts.cpp
)
target_link_libraries(pprz_find_aircrafts
    Ivy_C
    Threads::Threads
)




