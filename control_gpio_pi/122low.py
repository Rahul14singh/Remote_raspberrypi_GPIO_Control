import RPi.GPIO as ir
print "PIN 36 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(36,ir.OUT)
ir.output(36,ir.LOW)
