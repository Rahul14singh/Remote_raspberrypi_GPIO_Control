import RPi.GPIO as ir
print "PIN 5 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(5,ir.OUT)
ir.output(5,ir.HIGH)
