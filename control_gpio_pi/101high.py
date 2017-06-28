import RPi.GPIO as ir
print "PIN 15 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(15,ir.OUT)
ir.output(15,ir.HIGH)
