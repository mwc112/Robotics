class Canvas:
    def cmToPx(self, value):
        return 200 + 8 * value

    def drawParticles(self, particles):
        print "drawParticles:" + str([(self.cmToPx(x), self.cmToPx(y), theta) for (x, y, theta) in particles])
       
    def drawLine(self, line):
        print "drawLine:" + str((self.cmToPx(line[0]), self.cmToPx(line[1]), self.cmToPx(line[2]), self.cmToPx(line[3])))  
