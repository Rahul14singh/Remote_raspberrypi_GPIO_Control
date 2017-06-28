import RPi.GPIO as ir
print "PIN 26 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(26,ir.OUT)
ir.output(26,ir.HIGH)
