#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngcore" for configuration "RelWithDebInfo"
set_property(TARGET ngcore APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ngcore PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/lib/netgen/ngcore.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/bin/ngcore.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ngcore )
list(APPEND _IMPORT_CHECK_FILES_FOR_ngcore "${_IMPORT_PREFIX}/Library/lib/netgen/ngcore.lib" "${_IMPORT_PREFIX}/Library/bin/ngcore.dll" )

# Import target "netgen" for configuration "RelWithDebInfo"
set_property(TARGET netgen APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(netgen PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/bin/netgen.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS netgen )
list(APPEND _IMPORT_CHECK_FILES_FOR_netgen "${_IMPORT_PREFIX}/Library/bin/netgen.exe" )

# Import target "gui" for configuration "RelWithDebInfo"
set_property(TARGET gui APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gui PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/lib/netgen/libgui.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "togl"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/bin/libgui.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gui )
list(APPEND _IMPORT_CHECK_FILES_FOR_gui "${_IMPORT_PREFIX}/Library/lib/netgen/libgui.lib" "${_IMPORT_PREFIX}/Library/bin/libgui.dll" )

# Import target "togl" for configuration "RelWithDebInfo"
set_property(TARGET togl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(togl PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/lib/netgen/togl.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/bin/togl.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS togl )
list(APPEND _IMPORT_CHECK_FILES_FOR_togl "${_IMPORT_PREFIX}/Library/lib/netgen/togl.lib" "${_IMPORT_PREFIX}/Library/bin/togl.dll" )

# Import target "nglib" for configuration "RelWithDebInfo"
set_property(TARGET nglib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(nglib PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/lib/netgen/nglib.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/Library/bin/nglib.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS nglib )
list(APPEND _IMPORT_CHECK_FILES_FOR_nglib "${_IMPORT_PREFIX}/Library/lib/netgen/nglib.lib" "${_IMPORT_PREFIX}/Library/bin/nglib.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
