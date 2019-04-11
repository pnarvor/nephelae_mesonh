find_package(PkgConfig)

# find netcdf-cxx4
pkg_check_modules(PC_IVY_C REQUIRED ivy-c)

set(IVY_C_DEFINITIONS ${PC_IVY_C_CFLAGS_OTHER})

find_path(IVY_C_INCLUDE_DIR Ivy/ivy.h
    HINTS ${PC_IVY_C_INCLUDE_DIRS}
)

# list(APPEND PC_IVY_C_LIBRARIES "test")
foreach(library ${PC_IVY_C_LIBRARIES})

    find_library(${library}_full_path NAME ${library}
        HINTS ${PC_IVY_C_LIBRARY_DIRS}
    )

    list(APPEND IVY_C_LIBRARIES_TO_CHECK ${library}_FOUND)
    if(NOT ${${library}_full_path} EQUAL ${library}-NOTFOUND)
        set(${library}_FOUND "${${library}_full_path}")
    endif()

    list(APPEND IVY_C_LIBRARIES ${${library}_full_path})
endforeach()

message(STATUS "IVY_C_LIBRARIES : ${IVY_C_LIBRARIES}")

##

include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ivy-c DEFAULT_MSG
    ${IVY_C_LIBRARIES_TO_CHECK}
    IVY_C_INCLUDE_DIR
)
mark_as_advanced(${IVY_C_LIBRARIES_TO_CHECK} IVY_C_INCLUDE_DIR)

if(ivy-c_FOUND AND NOT TARGET Ivy_C)
    add_library(Ivy_C INTERFACE)
    target_include_directories(Ivy_C
        INTERFACE ${PC_IVY_C_INCLUDE_DIRS}
    )
    target_link_libraries(Ivy_C
        INTERFACE ${IVY_C_LIBRARIES}
    )
    target_compile_definitions(Ivy_C
        INTERFACE ${PC_IVY_C_CFLAGS_OTHER}
    )
endif()


