class BrainFuckProgram:
    const_int_floor = 0
    const_int_ceiling = 255  # Pretend they're 8 bit unsigned ints

    def __init__(self, brainfuck_code):
        self.brainfuck_code = brainfuck_code  # Stores our program
        self.program_counter = 0

        self.tape = [0]  # Create our initial, empty tape. Will grow both ways on demand
        self.tape_pointer = 0  # Current pointer on tape

    def run(self):
        while self.program_counter < len(self.brainfuck_code):
            self.step()
        return

    def step(self):
        if len(self.brainfuck_code) <= self.program_counter:
            return

        operation = self.brainfuck_code[self.program_counter]
        self.do_operation(operation)
        return

    def do_operation(self, operation):
        if operation == ">":
            self.op_pointer_right()
            return

        if operation == "<":
            self.op_pointer_left()
            return

        if operation == "+":
            self.op_increment()
            return

        if operation == "-":
            self.op_decrement()
            return

        if operation == ".":
            self.op_output()
            return

        if operation == ",":
            self.op_replace()
            return

        if operation == "[":
            self.op_jump()
            return

        if operation == "]":
            self.op_jump()
            return

        # Fell through, so ignore and increment PC
        self.program_counter += 1

    def op_pointer_right(self):

        # Make sure we have tape at this position
        if len(self.tape) <= (self.tape_pointer + 1):
            self.tape.append(0)

        # Set the new pointer
        self.tape_pointer += 1

        # Increment PC
        self.program_counter += 1
        return

    def op_pointer_left(self):
        # Make sure we have tape at this position

        if self.tape_pointer <= 0:
            self.tape.insert(0, 0)  # Shunt the tape to the right, rather than move the pointer
        else:
            self.tape_pointer += -1

        # Increment PC
        self.program_counter += 1
        return

    def op_increment(self):

        # Get the current cell value
        cell = self.tape[self.tape_pointer]

        if cell == self.const_int_ceiling:
            cell = self.const_int_floor  # Wrap around
        else:
            cell += 1

        self.tape[self.tape_pointer] = cell

        # Increment PC
        self.program_counter += 1
        return

    def op_decrement(self):
        # Get the current cell value
        cell = self.tape[self.tape_pointer]

        if cell == self.const_int_floor:
            cell = self.const_int_ceiling
        else:
            cell += -1

        self.tape[self.tape_pointer] = cell

        # Increment PC
        self.program_counter += 1
        return

    def op_output(self):
        cell = self.tape[self.tape_pointer]

        # Character to ASCII
        alpha = chr(cell)

        # Print character and its ASCII value in the desired format
        # print(f"{alpha} ({cell})")
        print(f"{alpha}", end="")

        # Increment PC
        self.program_counter += 1
        return

    def op_replace(self):
        user_input = self.get_user_input()
        self.tape[self.tape_pointer] = user_input

        # Increment PC
        self.program_counter += 1

    def get_user_input(self):

        user_input = input("Enter a single char:")

        if len(user_input) < 1:
            return 0

        return ord(user_input[0])

        if user_input.isdigit() and self.const_int_floor < int(user_input) < self.const_int_ceiling:
            return int(user_input)

        return 0

    def op_jump(self):

        operation = self.brainfuck_code[self.program_counter]
        cell = self.tape[self.tape_pointer]

        # Set the search direction
        if operation == "[":

            if cell != 0:
                self.program_counter += 1
                return

            search_direction = 1
            counter_operation = "]"
        elif operation == "]":

            if cell == 0:
                self.program_counter += 1
                return

            search_direction = -1
            counter_operation = "["
        else:
            raise Exception("Unexpected loop char")

        depth = 0

        # Find the matching brace
        while len(self.brainfuck_code) > self.program_counter >= 0:
            self.program_counter += search_direction
            tmp_operation = self.brainfuck_code[self.program_counter]

            if tmp_operation == operation:
                depth += 1  # Found a nested loop

            if tmp_operation == counter_operation:
                if depth > 0:
                    depth += -1
                else:
                    return

        raise Exception("Did not find matching counter operation")


if __name__ == '__main__':
    inputFile = open("D:\\LocalStuff\\Dev\\BrainfuckInterpreter\\input.txt", "r")
    inputContent = inputFile.read().replace('\r', '').replace('\n', '')

    program = BrainFuckProgram(inputContent)

    program.run()
