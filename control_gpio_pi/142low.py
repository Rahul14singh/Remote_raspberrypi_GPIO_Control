import RPi.GPIO as ir
print "PIN 40 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(40,ir.OUT)
ir.output(40,ir.LOW)
