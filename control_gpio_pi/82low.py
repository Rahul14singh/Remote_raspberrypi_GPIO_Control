import RPi.GPIO as ir
print "PIN 22 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(22,ir.OUT)
ir.output(22,ir.LOW)
