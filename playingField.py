#
# playingField
#


class PlayingField(): 
    def __init__(self):
        self.ground = [400,400,350,400,400,400,400,400,400,400,
                400,400,400,400,400,400,400,400,400,400]
        
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