import RPi.GPIO as ir
print "PIN 15 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(15,ir.OUT)
ir.output(15,ir.LOW)
