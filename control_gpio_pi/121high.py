import RPi.GPIO as ir
print "PIN 21 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(21,ir.OUT)
ir.output(21,ir.HIGH)
