# tdbcConfig.sh --
#
# This shell script (for sh) is generated automatically by TDBC's configure
# script. It will create shell variables for most of the configuration options
# discovered by the configure script. This script is intended to be included
# by the configure scripts for TDBC extensions so that they don't have to
# figure this all out for themselves.
#
# The information in this file is specific to a single platform.
#
# RCS: @(#) $Id$

# TDBC's version number
tdbc_VERSION=1.1.1
TDBC_VERSION=1.1.1

# Name of the TDBC library - may be either a static or shared library
tdbc_LIB_FILE=tdbc111t.dll
TDBC_LIB_FILE=tdbc111t.dll

# String to pass to the linker to pick up the TDBC library from its build dir
tdbc_BUILD_LIB_SPEC="@tdbc_BUILD_LIB_SPEC@"
TDBC_BUILD_LIB_SPEC="@tdbc_BUILD_LIB_SPEC@"

# String to pass to the linker to pick up the TDBC library from its installed
# dir.
tdbc_LIB_SPEC="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbc111t.dll"
TDBC_LIB_SPEC="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbc111t.dll"

# Name of the TBDC stub library
tdbc_STUB_LIB_FILE="tdbcstub111.lib"
TDBC_STUB_LIB_FILE="tdbcstub111.lib"

# String to pass to the linker to pick up the TDBC stub library from its
# build directory
tdbc_BUILD_STUB_LIB_SPEC="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\Release_AMD64_VC1916\tdbcstub111.lib"
TDBC_BUILD_STUB_LIB_SPEC="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\Release_AMD64_VC1916\tdbcstub111.lib"

# String to pass to the linker to pick up the TDBC stub library from its
# installed directory
tdbc_STUB_LIB_SPEC="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbcstub111.lib"
TDBC_STUB_LIB_SPEC="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbcstub111.lib"

# Path name of the TDBC stub library in its build directory
tdbc_BUILD_STUB_LIB_PATH="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\Release_AMD64_VC1916\tdbcstub111.lib"
TDBC_BUILD_STUB_LIB_PATH="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\Release_AMD64_VC1916\tdbcstub111.lib"

# Path name of the TDBC stub library in its installed directory
tdbc_STUB_LIB_PATH="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbcstub111.lib"
TDBC_STUB_LIB_PATH="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1\tdbcstub111.lib"

# Location of the top-level source directories from which TDBC was built.
# This is the directory that contains doc/, generic/ and so on.  If TDBC
# was compiled in a directory other than the source directory, this still
# points to the location of the sources, not the location where TDBC was
# compiled.
tdbc_SRC_DIR="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\.."
TDBC_SRC_DIR="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\.."

# String to pass to the compiler so that an extension can find installed TDBC
# headers
tdbc_INCLUDE_SPEC="-Id:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\..\include"
TDBC_INCLUDE_SPEC="-Id:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\..\include"

# String to pass to the compiler so that an extension can find TDBC headers
# in the source directory
tdbc_BUILD_INCLUDE_SPEC="-IC:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\..\generic"
TDBC_BUILD_INCLUDE_SPEC="-IC:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\..\generic"

# Path name where .tcl files in the tdbc package appear at run time.
tdbc_LIBRARY_PATH="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1"
TDBC_LIBRARY_PATH="d:/Users/Administrator/anaconda3/envs/3Dsource\Library\lib\tdbc1.1.1"

# Path name where .tcl files in the tdbc package appear at build time.
tdbc_BUILD_LIBRARY_PATH="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\../library"
TDBC_BUILD_LIBRARY_PATH="C:\ci\tk_1592503260103\work\tcl8.6.10\pkgs\tdbc1.1.1\win\../library"

# Additional flags that must be passed to the C compiler to use tdbc
tdbc_CFLAGS=
TDBC_CFLAGS=

