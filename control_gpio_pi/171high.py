import RPi.GPIO as ir
print "PIN 35 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(35,ir.OUT)
ir.output(35,ir.HIGH)
