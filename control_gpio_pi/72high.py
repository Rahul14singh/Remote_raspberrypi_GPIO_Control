import RPi.GPIO as ir
print "PIN 18 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(18,ir.OUT)
ir.output(18,ir.HIGH)
