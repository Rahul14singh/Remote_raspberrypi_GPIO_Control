import RPi.GPIO as ir
print "PIN 29 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(29,ir.OUT)
ir.output(29,ir.LOW)
