import RPi.GPIO as ir
print "PIN 35 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(35,ir.OUT)
ir.output(35,ir.LOW)
