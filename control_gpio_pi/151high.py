import RPi.GPIO as ir
print "PIN 31 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(31,ir.OUT)
ir.output(31,ir.HIGH)
