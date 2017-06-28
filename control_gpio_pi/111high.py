import RPi.GPIO as ir
print "PIN 19 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(19,ir.OUT)
ir.output(19,ir.HIGH)
