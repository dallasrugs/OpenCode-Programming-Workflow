class Notebook:
    def __init__(self):
        self.output = None
        self.pending = True

    def receive_output(self, value):
        self.output = value

    def apply_receipt(self):
        self.pending = False

    def leave(self):
        if self.pending:
            raise RuntimeError("Execution operation still pending")
        return "library"
