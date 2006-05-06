addhandler base_eventhandler
python base_eventhandler() {
	from bb import note, error, data
	from bb.event import Handled, NotHandled, getName
	import os

 
	name = getName(e)
	if name.startswith("BuildStarted"):
		bb.data.setVar( 'BB_VERSION', bb.__version__, e.data )
        bb.data.setVar( 'SEEN_TARGET_FPU', bb.data.getVar('TARGET_FPU', e.data), e.data )

	return NotHandled
}

addtask build
do_build = ""
do_build[nostamp] = "1"
do_build[func] = "1"


