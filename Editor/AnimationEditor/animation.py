__author__ = 'Vincent'

from Editor.Component import Component
from Editor import structreader


class Animation(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('texture', '')
        self.addParam('loop', True)
        self.frames = []

    def editFrame(self, index, **params):
        self.frames[index].edit(**params)

    def addFrame(self, length, coords, width, height, render_offset, rotation):
        frame = Frame()
        frame.edit(length=length, x=coords[0], y=coords[1], width=width, height=height, render_x=render_offset[0],
                   render_y=render_offset[1], rotation=rotation)
        self.frames.append(frame)

    def addAll(self, num_frames, offset, length, start_coords, width, height, render_offset, rotation):
        """
        Add many frames one after another
        :param num_frames:
        :param offset:
        :return:
        """
        self.frames.clear()
        coords = [start_coords[0], start_coords[1]]
        for frame in range(num_frames):
            self.addFrame(length, coords, width, height, render_offset, rotation)
            coords[0] += (width+offset[0])
            coords[1] += offset[1]

    def toByteArray(self):
        data = bytearray()
        structreader.pack(data, self.paramDict['texture'], 'str')
        structreader.pack(data, int(self.paramDict['loop']), 'u8')
        structreader.pack(data, len(self.frames), 'u16')
        for frame in self.frames:
            data += frame.toByteArray()
        return data

    def fromByteArray(self, byteArray):
        anim = Animation()
        anim.paramDict['texture'] = structreader.unpack(byteArray, 'str')
        anim.paramDict['loop'] = bool(structreader.unpack(byteArray, 'u8'))
        num_frames = structreader.unpack(byteArray, 'u16')
        frame = Frame()
        for _ in range(num_frames):
            anim.frames.append(frame.fromByteArray(byteArray))
        return anim


class Frame(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('length', 100)
        self.addParam('x', 0)
        self.addParam('y', 0)
        self.addParam('width', 10)
        self.addParam('height', 10)
        self.addParam('render_x', 0)
        self.addParam('render_y', 0)
        self.addParam('rotation', 0)

    def edit(self, **params):
        for key in params:
            self.paramDict[key] = params[key]

    def fromByteArray(self, byteArray):
        frame = Frame()
        frame.paramDict['length'] = structreader.unpack(byteArray, 'u32')
        structreader.unpack(byteArray, 'u16')
        frame.paramDict['x'] = structreader.unpack(byteArray, 'u32')
        frame.paramDict['y'] = structreader.unpack(byteArray, 'u32')
        frame.paramDict['width'] = structreader.unpack(byteArray, 'u32')
        frame.paramDict['height'] = structreader.unpack(byteArray, 'u32')
        structreader.unpack(byteArray, 'u32')
        structreader.unpack(byteArray, 'u32')
        frame.paramDict['render_x'] = structreader.unpack(byteArray, 's32')
        frame.paramDict['render_y'] = structreader.unpack(byteArray, 's32')
        frame.paramDict['rotation'] = structreader.unpack(byteArray, 'u32')
        structreader.unpack(byteArray, 'u8')

        return frame

    def toByteArray(self):
        data = bytearray()
        structreader.pack(data, self.paramDict['length'], 'u32')
        structreader.pack(data, 1, 'u16')
        structreader.pack(data, self.paramDict['x'], 'u32')
        structreader.pack(data, self.paramDict['y'], 'u32')
        structreader.pack(data, self.paramDict['width'], 'u32')
        structreader.pack(data, self.paramDict['height'], 'u32')
        structreader.pack(data, 100, 'u32')
        structreader.pack(data, 100, 'u32')
        structreader.pack(data, self.paramDict['render_x'], 's32')
        structreader.pack(data, self.paramDict['render_y'], 's32')
        structreader.pack(data, self.paramDict['rotation'], 'u32')
        structreader.pack(data, 255, 'u8')
        return data
