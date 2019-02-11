"""
Saleban Olow, Victor Alves
CSI-480-01
Due Thursday, February 7, 2019

Saleban: main, rooms
Victor: bridges
"""
import random
import tkinter as tk

def show_rooms(canvas, rooms, color='blue'):
    """
    Visualizes the rooms.

    Args:
         canvas(canvas): tk.Canvas object
         rooms(list): List of rooms to visualize
         color(string): room color
    """
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
    """
    Visualizes the bridges.

    Args:
         canvas(canvas): tk.Canvas object
         bridges(list): List of bridges to visualize
         color(string): Bridge color
    """
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
        """
        Exploring the tree

        Args:
             node_size(list): finding the min the node
        """
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

    def get_rooms(self, room=[]):
        """
        Get the room - after exploring the tree

        Args:
             room(list): storing rooms as we exploring the tree
        """
        if self.rooms is not None:
            room.append(self.rooms)
        if self.before_splitting is not None:
            self.before_splitting.get_rooms(room)
        if self.after_splitting is not None:
            self.after_splitting.get_rooms(room)
        return room
    
    # Saleban's part
    def add_rooms(self, bias=.5, s=0):
        """
        adding rooms

        Args:
             
        """
        if self.before_splitting is None and self.after_splitting is None:
            self.rooms = build_rooms((self.origin[0], self.origin[1], self.bounds[0], self.bounds[1]))
        if self.before_splitting is not None:
            self.before_splitting.add_rooms(bias, s)
        if self.after_splitting is not None:
            self.after_splitting.add_rooms(bias, s)

def build_rooms(pos):
    """
    Building rooms randomly

    Args:
         position(list): 
    """
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

def build_bridges(left, right):
    """
    Randomly generates the bridge between two rooms..

    Args:
        left(room): First room.
        right(room): Second room.

    Returns:
        list: The bridge between the two rooms.

    """
    bridge_exists = False
    # Obtain the direction
    direction = (right[0] - left[2], right[1] - left[3])

    # Check to see if the bridge already exists
    if direction[0] == 0 or direction[1] != 0:
        if min(abs(direction[0]), abs(direction[1])) == abs(direction[0]):
            bridge_exists = True
    else:
        return []

    bridge = []
    width = random.randint(0, 1)
    if bridge_exists:
        # Check x coordinates
        # If the direction is left
        if direction[0] > 0:
            global x_start, y_start, x_end, y_end, bridget_pos
            x_start = left[2]
            x_end = right[0]
            y_start = random.randint(min(left[1], left[3]), max(left[1], left[3]))
            y_end = random.randint(min(right[1], right[3]), max(right[1], right[3]))
            bridget_pos = random.randint(min(left[2], right[0]), max(left[2], right[0]))
        # If direction is right
        elif direction[0] < 0:
            x_start = right[2]
            x_end = left[0]
            y_start = random.randint(min(right[1], right[3]), max(right[1], right[3]))
            y_end = random.randint(min(left[1], left[3]), max(left[1], left[3]))
            bridget_pos = random.randint(min(left[0], right[2]), max(left[0], right[2]))

        bridge.append((x_start, y_start - width, bridget_pos, y_start + width))
        bridge.append((bridget_pos - width, y_start - width, bridget_pos + width, y_end + width))
        bridge.append((bridget_pos, y_end - width, x_end, y_end + width))
    else:
        # Check y coordinates
        # If direction = up
        if direction[1] < 0:
            y_start = left[3]
            y_end = right[1]
            # Generate random x value
            x_start = random.randint(min(left[0], left[2]), max(left[0], left[2]))
            x_end = random.randint(min(right[0], right[2]), max(right[0], right[2]))
            bridget_pos = random.randint(min(left[3], right[1]), max(left[3], right[1]))
        # If direction is down
        elif direction[1] > 0:
            y_start = right[3]
            y_end = left[1]
            x_start = random.randint(min(right[0], right[2]), max(right[0], right[2]))
            x_end = random.randint(min(left[0], left[2]), max(left[0], left[2]))
            bridget_pos = random.randint(min(right[3], left[1]), max(right[3], left[1]))

        bridge.append((x_start - width, y_start, x_start + width, bridget_pos))
        bridge.append((x_start - width, bridget_pos - width, x_end + width, bridget_pos + width))
        bridge.append((x_end - width, bridget_pos, x_end + width, y_end))
    return bridge

def connect_bridges(rooms):
    """
    Generates all the briges relevant to each room.

    Args:
        rooms(list): List of rooms.
    Returns:
        list: List of bridges.
    """
    # List of bridges
    bridges = []
    # List of rooms that are yet to be connected
    rooms_to_connect = rooms
    # Initial room
    starting_room = rooms_to_connect[0]

    while True:
        # Remove the initial room from the original list
        rooms_to_connect.remove(starting_room)
        # Find the room closest to the current room (starting_room)
        nearest_room = get_nearest_room(starting_room, rooms_to_connect)
        if not nearest_room:
            break
        else:
            # If there is another room in the list, extend the "bridges" list
            # Then, build a bridge between the current room and the nearest room
            bridges.extend(build_bridges(starting_room, nearest_room))
            # Repeat the same for the nearest room
            starting_room = nearest_room
    return bridges

def midpoint(rooms):
    """
    Helper function to help find the midpoint between the two rooms.

    Args:
        rooms: list of rooms
    Returns:
        int: Midpoint
    """
    return rooms[0] + (rooms[0] + rooms[2]) // 2, rooms[1] + (rooms[1] + rooms[3]) // 2

def get_nearest_room(rooms, list_of_rooms):
    """
    Helper function for finding the nearest room on builting bridges

    Args:
         rooms(int)
         list_of_rooms(list): 
    """
    starting_room = None
    nearest_room = None
    center_point = midpoint(rooms)

    for room in list_of_rooms:
        new_center = midpoint(rooms)
        dist = ((new_center[0] - center_point[0]) ** 2 + (new_center[1] - center_point[1]) ** 2) ** 0.5
        if not starting_room or (starting_room and dist < nearest_room):
            starting_room = room
            nearest_room = dist
    return starting_room


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Generative Binary Space Partitioning')
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.configure(background='#434751')
    canvas.pack()

    dungeonTree = BSP((0, 0), (100, 100), (20, 20))
    dungeonTree.add_rooms()

    rooms = dungeonTree.get_rooms()
    show_rooms(canvas, rooms, "#f2f4f7")

    bridges = connect_bridges(rooms)
    show_bridges(canvas, bridges, "#333")
    root.mainloop()
