SOME_VAR = 124

# some comment
addhandler tinderclient_eventhandler
python tinderclient_eventhandler() {
    # NotHandled should not be known here

    return NotHandled
}

