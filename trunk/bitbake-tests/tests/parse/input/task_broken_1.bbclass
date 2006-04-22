
# missing  '_' between make and foo
python do_makefoo() {
}

addtask make_foo before do_build after do_fetch
