import socket


class Server(object):
    """
    An adventure game socket server
    
    An instance's methods share the following variables:
    
    * self.socket: a "bound" server socket, as produced by socket.bind()
    * self.client_connection: a "connection" socket as produced by socket.accept()
    * self.input_buffer: a string that has been read from the connected client and
      has yet to be acted upon.
    * self.output_buffer: a string that should be sent to the connected client; for
      testing purposes this string should NOT end in a newline character. When
      writing to the output_buffer, DON'T concatenate: just overwrite.
    * self.done: A boolean, False until the client is ready to disconnect
    * self.room: one of 0, 1, 2, 3. This signifies which "room" the client is in,
      according to the following map:
      
                                     3                      N
                                     |                      ^
                                 1 - 0 - 2                  |
                                 
    When a client connects, they are greeted with a welcome message. And then they can
    move through the connected rooms. For example, on connection:
    
    OK! Welcome to Realms of Venture! This room has brown wall paper!  (S)
    move north                                                         (C)
    OK! This room has white wallpaper.                                 (S)
    say Hello? Is anyone here?                                         (C)
    OK! You say, "Hello? Is anyone here?"                              (S)
    move south                                                         (C)
    OK! This room has brown wall paper!                                (S)
    move west                                                          (C)
    OK! This room has a green floor!                                   (S)
    quit                                                               (C)
    OK! Goodbye!                                                       (S)
    
    Note that we've annotated server and client messages with *(S)* and *(C)*, but
    these won't actually appear in server/client communication. Also, you'll be
    free to develop any room descriptions you like: the only requirement is that
    each room have a unique description.
    """

    game_name = "Realms of Venture"

    def __init__(self, port=50000):
        self.input_buffer = ""
        self.output_buffer = ""
        self.done = False
        self.socket = None
        self.client_connection = None
        self.port = port

        self.room = 0

    def connect(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP)

        address = ('127.0.0.1', self.port)
        self.socket.bind(address)
        self.socket.listen(1)

        self.client_connection, address = self.socket.accept()

    def room_description(self, room_number):
        """
        For any room_number in 0, 1, 2, 3, return a string that "describes" that
        room.

        Ex: `self.room_number(1)` yields "Brown wallpaper covers the walls, bathing
        the room in warm light reflected from the half-drawn curtains."

        :param room_number: int
        :return: str
        """

        room_descriptions = {
            0: "This room has white wallpaper.",
            1: "This room has brown wall paper!",
            2: "This room has a green floor!",
            3: "This room has a red ceiling!"
        }

        return room_descriptions.get(room_number, "This room is empty.")

    def greet(self):
        """
        Welcome a client to the game.
        
        Puts a welcome message and the description of the client's current room into
        the output buffer.
        
        :return: None 
        """
        self.output_buffer = "Welcome to {}! {}".format(
            self.game_name,
            self.room_description(self.room)
        )

    def get_input(self):
        """
        Retrieve input from the client_connection. All messages from the client
        should end in a newline character: '\n'.
        
        This is a BLOCKING call. It should not return until there is some input from
        the client to receive.
         
        :return: None 
        """

        client_input = ""
        # Read from the client until we get a newline character
        # This is a blocking call, so it will wait until the client sends something
        while not client_input.endswith('\n'):
            try:
                client_input += self.client_connection.recv(4096).decode('utf-8')
            except ConnectionAbortedError:
                print("Connection closed by host.")
                self.done = True
                return

        # Strip the trailing newline character    
        self.input_buffer = client_input.strip()

    def move(self, argument):
        """
        Moves the client from one room to another.
        
        Examines the argument, which should be one of:
        
        * "north"
        * "south"
        * "east"
        * "west"
        
        "Moves" the client into a new room by adjusting self.room to reflect the
        number of the room that the client has moved into.
        
        Puts the room description (see `self.room_description`) for the new room
        into "self.output_buffer".
        
        :param argument: str
        :return: None
        """
        room_moves = {
            0: {'north': 3, 'south': 1, 'east': 2, 'west': 4},
            1: {'north': 0, 'south': None, 'east': None, 'west': None},
            2: {'north': None, 'south': None, 'east': None, 'west': 0},
            3: {'north': None, 'south': 0, 'east': None, 'west': None},
            4: {'north': None, 'south': None, 'east': 0, 'west': None}
        }

        direction = argument.lower()

        if direction in room_moves[self.room]:
            new_room = room_moves[self.room][direction]
            if new_room is not None:
                self.room = new_room
                self.output_buffer = self.room_description(self.room)
            else:
                self.output_buffer = "You can't go that way!"
        else:
            self.output_buffer = "Invalid direction: {}".format(direction)

    def say(self, argument):
        """
        Lets the client speak by putting their utterance into the output buffer.
        
        For example:
        `self.say("Is there anybody here?")`
        would put
        `You say, "Is there anybody here?"`
        into the output buffer.
        
        :param argument: str
        :return: None
        """

        self.output_buffer = 'You say, "{}"'.format(argument)

    def quit(self, argument):
        """
        Quits the client from the server.
        
        Turns `self.done` to True and puts "Goodbye!" onto the output buffer.
        
        Ignore the argument.
        
        :param argument: str
        :return: None
        """

        self.done = True
        self.output_buffer = "Goodbye!"

    def route(self):
        """
        Examines `self.input_buffer` to perform the correct action (move, quit, or
        say) on behalf of the client.
        
        For example, if the input buffer contains "say Is anybody here?" then `route`
        should invoke `self.say("Is anybody here?")`. If the input buffer contains
        "move north", then `route` should invoke `self.move("north")`.
        
        :return: None
        """

        if self.input_buffer.startswith("move "):
            direction = self.input_buffer[5:].strip()
            self.move(direction)
        elif self.input_buffer.startswith("say "):
            message = self.input_buffer[4:].strip()
            self.say(message)
        elif self.input_buffer.startswith("quit"):
            self.quit(self.input_buffer[4:].strip())
        else:
            self.output_buffer = "Unknown command: {}".format(self.input_buffer)
        
        # Clear the input buffer after processing
        self.input_buffer = ""

    def push_output(self):
        """
        Sends the contents of the output buffer to the client.
        
        This method should prepend "OK! " to the output and append "\n" before
        sending it.
        
        :return: None 
        """

        self.client_connection.sendall(
            ("OK! " + self.output_buffer + "\n").encode('utf-8')
        )

    def serve(self):
        self.connect()
        self.greet()
        self.push_output()

        while not self.done:
            self.get_input()
            self.route()
            self.push_output()

        self.client_connection.close()
        self.socket.close()
