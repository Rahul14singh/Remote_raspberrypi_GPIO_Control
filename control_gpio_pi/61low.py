import RPi.GPIO as ir
print "PIN 5 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(5,ir.OUT)
ir.output(5,ir.LOW)
