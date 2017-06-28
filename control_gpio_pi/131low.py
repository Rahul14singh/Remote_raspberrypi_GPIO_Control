import RPi.GPIO as ir
print "PIN 23 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(23,ir.OUT)
ir.output(23,ir.LOW)
