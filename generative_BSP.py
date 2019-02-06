import random
import tkinter as tk

def show_rooms(canvas, rooms, color='blue'):
    size = (100, 100)
    x = 500 / size[0]
    y = 500 / size[1]
    for room in rooms:
        x1 = room[0] * x + 2
        y1 = room[1] * y + 2
        x2 = room[2] * x - 2
        y2 = room[3] * y - 2
        canvas.create_rectangle(x1, y1, x2, y2, width=0, fill=color)


def show_bridges(canvas, bridges, color='green'):
    size = (100, 100)
    x = 500 / size[0]
    y = 500 / size[1]
    for bridge in bridges:
        x1 = min(bridge[0], bridge[2]) * x
        y1 = min(bridge[1], bridge[3]) * y
        x2 = max(bridge[0], bridge[2]) * x
        y2 = max(bridge[1], bridge[3]) * y
        canvas.create_rectangle(x1, y1, x2, y2, width=0, fill=color)


class BSP:
    def __init__(self, origin, bounds, node_size):
        self.origin = origin
        self.bounds = bounds
        self.before_splitting = None
        self.after_splitting = None
        self.rooms = None
        self.get_tree(node_size)

    def get_tree(self, node_size):
        a, b = self.origin[0], self.origin[1]
        c, d = self.bounds[0], self.bounds[1]
        if random.random() >= 0.5:
            spacing = node_size[1]
            if not b + spacing >= d - spacing:
                pos = random.randint(b + spacing, d - spacing)
                self.before_splitting = BSP((a, b), (c, pos), node_size)
                self.after_splitting = BSP((a, pos), (c, d), node_size)
        else:
            b = self.origin[0]
            d = self.bounds[0]
            spacing = node_size[0]
            if not b + spacing >= d - spacing:
                pos = random.randint(b + spacing, d - spacing)
                self.before_splitting = BSP((a, b), (pos, d), node_size)
                self.after_splitting = BSP((pos, b), (c, d), node_size)

    def get_bridges(self, bridge=[]):
        bridge.extend(self.bridges)
        if self.before_splitting is not None:
            self.before_splitting.get_bridges(bridge)
        if self.after_splitting is not None:
            self.after_splitting.get_bridges(bridge)
        return bridge

    def get_rooms(self, room=[]):
        if self.rooms is not None:
            room.append(self.rooms)
        if self.before_splitting is not None:
            self.before_splitting.get_rooms(room)
        if self.after_splitting is not None:
            self.after_splitting.get_rooms(room)
        return room

    def add_rooms(self, bias=.5, s=0):
        if self.before_splitting is None and self.after_splitting is None:
            self.rooms = build_rooms((self.origin[0], self.origin[1], self.bounds[0], self.bounds[1]))
        if self.before_splitting is not None:
            self.before_splitting.add_rooms(bias, s)
        if self.after_splitting is not None:
            self.after_splitting.add_rooms(bias, s)

# This builds our room randomly
def build_rooms(pos):
    x1 = random.randrange(pos[0], (pos[0] + pos[2]) // 2)
    x1_points = pos[0] + (pos[2] - pos[0]) * (1 - 1)
    final_x1 = int(x1 + (x1_points - x1) * 0)

    y1 = random.randrange(pos[1], (pos[1] + pos[3]) // 2)
    y1_points = pos[1] + (pos[3] - pos[1]) * (1 - 1)
    final_y1 = int(y1 + (y1_points - y1) * 0)

    x2 = random.randrange((pos[0] + pos[2]) // 2, pos[2])
    x2_points = pos[2] - (pos[2] - pos[0]) * (1 - 1)
    final_x2 = int(x2 + (x2_points - x2) * 0)

    y2 = random.randrange((pos[1] + pos[3]) // 2, pos[3])
    y2_points = pos[3] - (pos[3] - pos[1]) * (1 - 1)
    final_y2 = int(y2 + (y2_points - y2) * 0)
    return final_x1, final_y1, final_x2, final_y2


def build_bridges(r1, r2):
    bridge_exists = False
    direction = (r2[0] - r1[2], r2[1] - r1[3])
    if direction[0] == 0 or direction[1] != 0:
        if min(abs(direction[0]), abs(direction[1])) == abs(direction[0]):
            bridge_exists = True
    else:
        return []
    bridge = []
    width = random.randint(0, 1)
    if bridge_exists:
        if direction[0] > 0:
            global x_start
            global y_start
            global x_end
            global y_end
            global bridget_pos
            x_start = r1[2]
            y_start = random.randint(min(r1[1], r1[3]), max(r1[1], r1[3]))
            x_end = r2[0]
            y_end = random.randint(min(r2[1], r2[3]), max(r2[1], r2[3]))
            bridget_pos = random.randint(min(r1[2], r2[0]), max(r1[2], r2[0]))
        elif direction[0] < 0:
            x_start = r2[2]
            y_start = random.randint(min(r2[1], r2[3]), max(r2[1], r2[3]))
            x_end = r1[0]
            y_end = random.randint(min(r1[1], r1[3]), max(r1[1], r1[3]))
            bridget_pos = random.randint(min(r1[0], r2[2]), max(r1[0], r2[2]))
        bridge.append((x_start, y_start - width, bridget_pos, y_start + width))
        bridge.append((bridget_pos - width, y_start - width, bridget_pos + width, y_end + width))
        bridge.append((bridget_pos, y_end - width, x_end, y_end + width))
    else:
        if direction[1] < 0:
            y_start = r1[3]
            x_start = random.randint(min(r1[0], r1[2]), max(r1[0], r1[2]))
            y_end = r2[1]
            x_end = random.randint(min(r2[0], r2[2]), max(r2[0], r2[2]))
            bridget_pos = random.randint(min(r1[3], r2[1]), max(r1[3], r2[1]))
        elif direction[1] > 0:
            y_start = r2[3]
            x_start = random.randint(min(r2[0], r2[2]), max(r2[0], r2[2]))
            y_end = r1[1]
            x_end = random.randint(min(r1[0], r1[2]), max(r1[0], r1[2]))
            bridget_pos = random.randint(min(r2[3], r1[1]), max(r2[3], r1[1]))
        bridge.append((x_start - width, y_start, x_start + width, bridget_pos))
        bridge.append((x_start - width, bridget_pos - width, x_end + width, bridget_pos + width))
        bridge.append((x_end - width, bridget_pos, x_end + width, y_end))
    return bridge


def connect_bridges(rooms):
    all_bridges = []
    rooms_left = rooms[:]
    starting_room = rooms_left[0]
    while True:
        rooms_left.remove(starting_room)
        nearest_room = get_nearest_room(starting_room, rooms_left)
        if nearest_room:
            all_bridges.extend(build_bridges(starting_room, nearest_room))
            starting_room = nearest_room
        else:
            break
    return all_bridges


def get_nearest_room(rooms, list_of_rooms):
    starting_room = None
    nearest_room = None
    center_point = (rooms[0] + (rooms[0] + rooms[2]) // 2, rooms[1] + (rooms[1] + rooms[3]) // 2)
    for room in list_of_rooms:
        new_center = (room[0] + (room[0] + room[2]) // 2, room[1] + (room[1] + room[3]) // 2)
        dist = ((new_center[0] - center_point[0]) ** 2 + (new_center[1] - center_point[1]) ** 2) ** 0.5
        if starting_room is not None and dist < nearest_room:
            starting_room = room
            nearest_room = dist
        elif starting_room is None:
            starting_room = room
            nearest_room = dist
    return starting_room


if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    dungeonTree = BSP((0, 0), (100, 100), (20, 20))
    dungeonTree.add_rooms()

    rooms = dungeonTree.get_rooms()
    show_rooms(canvas, rooms)

    bridges = connect_bridges(rooms)
    show_bridges(canvas, bridges, 'red')
    root.mainloop()
