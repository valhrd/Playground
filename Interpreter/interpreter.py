class Interpreter:
    def __init__(self, filename):
        self.filename = filename
    
    def parse(self):
        with open(self.filename, "r") as file:
            contents = file.read()

        for line in contents.split("\n"):
            print(line)


if __name__ == "__main__":
    filename = "test.math"
    Interpreter(filename).parse()