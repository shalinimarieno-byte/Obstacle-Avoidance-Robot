cmake_minimum_required(VERSION 3.8)
project(vacuum_bot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/lidar_scanner.py
  scripts/path_planner.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()