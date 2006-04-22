SOME_VAR = 124

# some comment
addhandler tinderclient_eventhandler
python tinderclient_eventhandler() {
    from bb.event import NotHandled

    return NotHandled
}

