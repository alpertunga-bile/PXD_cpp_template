from platform import system
from os.path import exists, join, realpath
from subprocess import run
from typing import Tuple
from os import makedirs


def get_venv_foldername(json_filename: str) -> Tuple[str, str]:
    from json import load

    with open(json_filename) as json_file:
        json_infos = load(json_file)

    try:
        return (json_infos["venv_folder"], json_infos["target_folder"])
    except:
        return ("venv", "third-party")


def create_cmake_file(packages_folder: str) -> None:
    file = open("CMakeLists.txt", "w")

    file.write(
        f"""
cmake_minimum_required(VERSION 3.5.0)
project(pxd-cpp-template VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

include(setup.cmake)

set_cxx(20)
enable_iwyu()

set(PXD_THIRD_PARTY_DIR ${{CMAKE_CURRENT_SOURCE_DIR}}/{packages_folder})
set(PXD_INCLUDE_DIR ${{CMAKE_CURRENT_SOURCE_DIR}}/includes)
set(PXD_SOURCE_DIR ${{CMAKE_CURRENT_SOURCE_DIR}}/sources)

set(PXD_HEADER_FILES

)

set(PXD_SOURCE_FILES

)

include_directories(

)

set(COMMON_STD_HEADERS

)

set(LIBS_TO_LINK

)

add_executable(${{PROJECT_NAME}} ${{PXD_SOURCE_FILES}})

target_link_libraries(${{PROJECT_NAME}} ${{LIBS_TO_LINK}})

target_precompile_headers(
    ${{PROJECT_NAME}} PRIVATE
    ${{COMMON_STD_HEADERS}}
    ${{PXD_HEADER_FILES}}
)

set(CPACK_PROJECT_NAME ${{PROJECT_NAME}})
set(CPACK_PROJECT_VERSION ${{PROJECT_VERSION}})
include(CPack)
        """
    )

    file.close()


if __name__ == "__main__":
    json_filename = "packages.json"
    cmake_utility_filename = "setup.cmake"
    os_name = system()

    if exists(json_filename) is False:
        print(f"/_\ {json_filename} file is not exists")
        exit(1)

    venv_foldername, packages_folder = get_venv_foldername(json_filename)

    if exists(venv_foldername) is False:
        run(
            f"python third_wheel.py --setup_venv",
            shell=True,
            check=True,
        )

    python_exec = (
        join(venv_foldername, "Scripts", "python.exe")
        if os_name == "Windows"
        else realpath(join(venv_foldername, "bin", "python"))
    )

    run(f"{python_exec} third_wheel.py", shell=True, check=True)

    makedirs("includes", exist_ok=True)
    makedirs("sources", exist_ok=True)

    print("/_\ Creating CMakeLists file")
    create_cmake_file(packages_folder)
