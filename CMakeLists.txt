cmake_minimum_required(VERSION 3.10.0)
project(pxd-cpp-template VERSION 0.1.0 LANGUAGES C CXX)

LIST(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmakes)
set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/install)

include(CTest)
enable_testing()

set(CXX_VERSION 20)
set(CMAKE_CXX_STANDARD ${CXX_VERSION})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++${CXX_VERSION}")
endif()

if(NOT WIN32)
  set(IWYU_ARGS "include-what-you-use -w -Xiwyu --verbose=7")
  add_compile_definitions(CMAKE_CXX_INCLUDE_WHAT_YOU_USE=${IWYU_ARGS})
endif(NOT WIN32)

if(${CMAKE_BUILD_TYPE} MATCHES "Release")

  message(STATUS "Optimizations are opened for ${PROJECT_NAME}")

  include(CheckIPOSupported)
  check_ipo_supported(RESULT is_supported OUTPUT error)

  if(is_supported)
    message(STATUS "Opening LTO")
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION TRUE)
  endif(is_supported)

  if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(STATUS "Adding -O3 -march=native -flto flags")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -march=native -flto")
  endif(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")

endif(${CMAKE_BUILD_TYPE} MATCHES "Release")


set(PXD_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/includes)
set(PXD_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/sources)
set(PXD_THIRD_PARTY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third-party)

option(PXD_BUILD_TEST "Build test executable" OFF)

set(PXD_HEADER_FILES
  ${PXD_INCLUDE_DIR}/logger.hpp
  ${PXD_INCLUDE_DIR}/assert_checks.hpp
)

set(PXD_SOURCE_FILES
  ${PXD_SOURCE_DIR}/logger.cpp
  ${PXD_SOURCE_DIR}/assert_checks.cpp

  ${PXD_HEADER_FILES}
)

include_directories(
    ${PXD_INCLUDE_DIR}
)

set(COMMON_STD_HEADERS

)

# ---------------------------------------------------------------
include(FetchContent)
set(BUILD_SHARED_LIBRARY OFF)

# --- fmt
FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt
  GIT_TAG master
)
FetchContent_MakeAvailable(fmt)


# ---------------------------------------------------------------

set(LIBS_TO_LINK
  fmt::fmt
)

add_executable(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp ${PXD_SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} ${LIBS_TO_LINK})

target_precompile_headers(
    ${PROJECT_NAME} PRIVATE
    ${COMMON_STD_HEADERS}
    ${PXD_HEADER_FILES}
)

# ------------------------------------------------------------------------------
# -- Test Executable

if(PXD_BUILD_TEST)
    set(PXD_TEST_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/tests)

    set(PXD_TEST_PROJECT_NAME ${PROJECT_NAME}_test)

    set(PXD_TEST_SOURCE_FILES
        ${PXD_TEST_SOURCE_DIR}/test.cpp

        ${PXD_SOURCE_FILES}
    )

    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest/
        GIT_TAG main
    )

    if(WIN32)
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    endif(WIN32)
    FetchContent_MakeAvailable(googletest)

    enable_testing()

    add_executable(${PXD_TEST_PROJECT_NAME} ${PXD_TEST_SOURCE_FILES})

    target_link_libraries(${PXD_TEST_PROJECT_NAME} ${LIBS_TO_LINK} GTest::gtest_main)

    include(GoogleTest)
    gtest_discover_tests(${PXD_TEST_PROJECT_NAME})

    target_precompile_headers(
        ${PXD_TEST_PROJECT_NAME} PRIVATE
        ${COMMON_STD_HEADERS}
        ${PXD_HEADER_FILES}
    )
endif(PXD_BUILD_TEST)
unset(PXD_BUILD_TEST CACHE)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
