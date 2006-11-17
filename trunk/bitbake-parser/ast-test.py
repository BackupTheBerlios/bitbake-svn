import bb.data
import ast


def test_assign():
    print "Testing assign"
    data = bb.data.init()
    a = ast.Assignment('KEY', 'VALUE')
    a.eval(data, None)

    print "\t", data.getVar('KEY', False) == 'VALUE'
    a = ast.Assignment('KEY', 'NEWVALUE')
    a.eval(data, None)
    print "\t", data.getVar('KEY', False) == 'NEWVALUE'

def test_immediate():
    print "Testing immediate assignment"
    data = bb.data.init()
    a = ast.ImmediateAssignment('KEY', 'VALUE')
    a.eval(data, None)

    print "\t", data.getVar('KEY', False) == 'VALUE'
    a = ast.ImmediateAssignment('KEY', '${@3*3}')
    a.eval(data, None)
    print "\t", data.getVar('KEY', False) == '9'

test_assign()
test_immediate()
