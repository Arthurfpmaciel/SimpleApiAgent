class Metrics:
    def __init__(self, latency=0, input_tokens=0, output_tokens=0):
        self.latency = latency
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
    def to_dict(self):
        return {
            "latency":self.latency,
            "input_tokens":self.input_tokens,
            "output_tokens":self.output_tokens
            }