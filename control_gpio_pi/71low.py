import RPi.GPIO as ir
print "PIN 7 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(7,ir.OUT)
ir.output(7,ir.LOW)
