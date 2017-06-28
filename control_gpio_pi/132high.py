import RPi.GPIO as ir
print "PIN 38 High"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(38,ir.OUT)
ir.output(38,ir.HIGH)
