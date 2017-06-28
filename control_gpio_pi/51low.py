import RPi.GPIO as ir
print "PIN 3 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(3,ir.OUT)
ir.output(3,ir.LOW)
