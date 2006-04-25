SOME_VAR = 124

# some comment
# not the missing 'r'
addhandler tinderclient_eventhandle
python tinderclient_eventhandler() {
    from bb.event import NotHandled

    return NotHandled
}

