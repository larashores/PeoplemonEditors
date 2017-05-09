class Frame:
    """
    Stores all frames of an animation
    """
    def __init__(self):
        self.images = []
        self.length = 30
        self.loop = False

    def draw(self):
        """
        Draws all images in the frame
        """
        for img in self.images:
            img.draw()

    def draw_unprocessed(self):
        for img in self.images:
            img.draw_unprocessed()

    def copy(self):
        """
        Copies the frame
        """
        new = Frame()
        new.length = self.length
        for img in self.images:
            new.images.append(img.copy())
        return new