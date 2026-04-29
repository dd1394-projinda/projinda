#
# field
#


class Field(): 
    def __init__(self):
        self.WIDTH = 20
        #self.ground = [400,400,350,400,400,400,400,400,400,400,
        #        400,400,400,400,400,400,400,400,400,400]
        self.blocks = [[] for _ in range(self.WIDTH)]

        self.build_world()

    def build_world(self):
        self.add_platform(0,self.WIDTH,400,500)
        self.add_platform(2,3,350,400)

    def add_platform(self, x_start, x_end, y_start, y_end):
            for x in range(x_start, x_end):
                self.blocks[x].append((y_start,y_end))

    def is_solid(self, x, y):
        x = int(x // 50)
        y = int(y // 50)

        if x < 0 or x >= self.WIDTH:
            return False
        
        for y1, y2 in self.blocks[x]:
            if y1 // 50 <= y <= y2 // 50:
                return True

        return False

    """
    def get_ground(self, samples):
        min_x = samples[0]

        for x in samples:
            block = int(x // 50)
            min_block = int(min_x // 50)
            if self.ground[block] < self.ground[min_block]:
                min_x = x 

        block = int(min_x // 50)
        block = max(0, min(block, len(self.ground) - 1))
        return self.ground[block]
    """