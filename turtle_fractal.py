from turtle import Turtle


class L_System:
    def __init__(self, initial_string, angle_change=90, speed=5):
        self.rules = {}
        self.current_string = initial_string
        self.saved_positions = []
        self.angle_change = angle_change
        self.turtle = Turtle()
        self.speed = speed
        self.turtle.speed(0)

    def __repr__(self):
        return self.current_string

    def add_rule(self, char, string):
        """
        Add a new rule, specifying what a given
        character should be replaced with.
        """
        self.rules[char] = string

    def update(self):
        """
        Apply all the rules to generate a new string.
        """
        new_string = ""
        for char in self.current_string:
            if char in self.rules.keys():
                new_string += self.rules[char]
            else:
                new_string += char

        self.current_string = new_string

    def print(self):
        """
        Convert the current string into Turtle instructions,
        and draw the result.
        """
        for char in self.current_string:
            if char == "+":
                self.turtle.right(self.angle_change)
                self.turtle.forward(self.speed)
            elif char == "-":
                self.turtle.left(self.angle_change)
                self.turtle.forward(self.speed)
            elif char == "[":
                self.save_position()
            elif char == "]":
                self.load_position()
            elif char == "0" or char == "1":
                self.turtle.forward(self.speed)

    def save_position(self):
        """Save the current position of the turtle."""
        self.saved_positions.append(self.turtle.pos())

    def load_position(self):
        """Load the most recently saved turtle position."""
        self.turtle.penup()
        self.turtle.setpos(self.saved_positions.pop())
        self.turtle.pendown()


def square_snowflake():
    system = L_System("M-M-M-M", 90)
    system.add_rule("+", "+")
    system.add_rule("-", "-")
    system.add_rule("M", "M-M+M+MM-M-M+M")
    return system


def tree():
    system = L_System("0", 45)
    system.add_rule("1", "11")
    system.add_rule("0", "1[-0]+0")
    return system


running = True

system = tree()
while running:
    system.turtle.clear()
    system.save_position()
    system.update()
    system.print()
    system.load_position()

    if not (input("continue?") == "Y"):
        running = False
