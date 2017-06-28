import RPi.GPIO as ir
print "PIN 37 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(37,ir.OUT)
ir.output(37,ir.HIGH)
