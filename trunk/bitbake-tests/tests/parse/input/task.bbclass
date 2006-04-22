python do_make_foo() {
}
addtask make_foo before do_build after do_fetch

addtask showdata
do_showdata[nostamp] = "1"
python do_showdata() {
}

