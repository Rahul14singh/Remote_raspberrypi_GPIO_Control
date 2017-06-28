import RPi.GPIO as ir
print "PIN 13 Low"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(13,ir.OUT)
ir.output(13,ir.LOW)
