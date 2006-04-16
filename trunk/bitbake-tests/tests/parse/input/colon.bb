T = "123"
A := "${B} ${A} test ${T}"
T = "456"
B = "${T} bval"

C = "cval"
C := "${C}append"
