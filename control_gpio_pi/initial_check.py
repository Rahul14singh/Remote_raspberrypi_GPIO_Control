import RPi.GPIO as ir
print "started"
ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(3,ir.OUT)
ir.setup(5,ir.OUT)
ir.setup(7,ir.OUT)
ir.setup(11,ir.OUT)
ir.setup(13,ir.OUT)
ir.setup(15,ir.OUT)
ir.setup(19,ir.OUT)
ir.setup(21,ir.OUT)
ir.setup(23,ir.OUT)
ir.setup(29,ir.OUT)
ir.setup(31,ir.OUT)
ir.setup(35,ir.OUT)
ir.setup(12,ir.OUT)
ir.setup(16,ir.OUT)
ir.setup(18,ir.OUT)
ir.setup(22,ir.OUT)
ir.setup(24,ir.OUT)
ir.setup(26,ir.OUT)
ir.setup(32,ir.OUT)
ir.setup(36,ir.OUT)
ir.setup(38,ir.OUT)
ir.setup(40,ir.OUT)
ir.setup(33,ir.OUT)
ir.setup(37,ir.OUT)
pins=[3,5,7,11,13,15,19,21,23,29,31,33,35,37,12,16,18,22,24,26,32,36,38,40]
i=0
while i<len(pins):
    ir.output(pins[i],ir.LOW)
    i+=1
print "Ended"
