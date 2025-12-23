cmake_minimum_required(VERSION 3.12)
project(test-package-d LANGUAGES NONE)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

execute_process(
  COMMAND "${Python3_EXECUTABLE}" -c
          "from pathlib import Path; import sysconfig; print(Path(sysconfig.get_path('purelib')).relative_to(sysconfig.get_path('data')).as_posix())"
  OUTPUT_VARIABLE PYTHON_INSTALL_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

string(REPLACE "-" "_" LIB_NAME "${PROJECT_NAME}")

install(
  DIRECTORY ${LIB_NAME}
  DESTINATION "${PYTHON_INSTALL_DIR}"
)
