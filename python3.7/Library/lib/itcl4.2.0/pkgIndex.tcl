if {[package vsatisfies 8.0 [package provide Tcl]]} {
    set add 80
} else {
    set add {t}
}
if {[::tcl::pkgconfig get debug] && \
        [file exists [file join $dir itcl420${add}g.dll]]} {
    package ifneeded Itcl 4.2.0 [list load [file join $dir itcl420${add}g.dll] Itcl]
} else {
    package ifneeded Itcl 4.2.0 [list load [file join $dir itcl420${add}.dll] Itcl]
}
unset add
