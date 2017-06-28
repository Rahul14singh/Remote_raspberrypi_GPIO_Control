import RPi.GPIO as ir
print "PIN 12 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(12,ir.OUT)
ir.output(12,ir.LOW)
