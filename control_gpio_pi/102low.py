import RPi.GPIO as ir
print "PIN 26 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(26,ir.OUT)
ir.output(26,ir.LOW)
