#-----------------------------------------------------------------------------
#
# OpenCASCADECompileDefinitionsAndFlags-release.cmake - OpenCASCADE CMake file 
# with compile definitions and C/C++ flags for Release configuration.
#
# This file is configured by OpenCASCADE.
#

# The C and C++ flags added by OpenCASCADE to the cmake-configured flags.
set (OpenCASCADE_C_FLAGS_RELEASE      "/MD /O2 /Ob2 /DNDEBUG")
set (OpenCASCADE_CXX_FLAGS_RELEASE    "/MD /O2 /Ob2 /DNDEBUG")

# The compile definitions used by OpenCASCADE.
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:UNICODE>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:_UNICODE>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:_CRT_SECURE_NO_WARNINGS>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:_CRT_NONSTDC_NO_DEPRECATE>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:HAVE_FREEIMAGE>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:HAVE_TBB>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:__TBB_NO_IMPLICIT_LINKAGE>)
set_property(DIRECTORY APPEND PROPERTY COMPILE_DEFINITIONS $<$<CONFIG:Release>:__TBBMALLOC_NO_IMPLICIT_LINKAGE>)

