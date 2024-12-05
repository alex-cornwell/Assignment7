import numpy as np
import networkx as nx

class FriendNetwork:
    def __init__(self):
        self.graph = nx.Graph()  # Using NetworkX for graph representation

    def add_friend(self, friend_id):
        self.graph.add_node(friend_id)

    def add_connection(self, friend1, friend2):
        self.graph.add_edge(friend1, friend2)

    def send_message(self, sender, receiver, message, lossiness):
        if not nx.has_path(self.graph, sender, receiver):
            print("No path available for communication.")
            return None

        original_length = len(message)
        compressed_message = self.lossy_compress(message, lossiness)
        metadata = {
            "original_length": original_length,
            "lossiness": lossiness,
        }
        return {
            "sender": sender,
            "receiver": receiver,
            "metadata": metadata,
            "message_body": compressed_message,
        }

    @staticmethod
    def lossy_compress(message, lossiness):
        # Convert message to numerical values (ASCII representation)
        signal = np.array([ord(char) for char in message])
        # Apply FFT
        fft_result = np.fft.fft(signal)
        # Zero out a portion of the FFT coefficients
        cutoff = int(len(fft_result) * (1 - lossiness))
        fft_result[cutoff:] = 0
        # Apply inverse FFT
        compressed_signal = np.fft.ifft(fft_result).real
        # Convert back to characters
        compressed_message = ''.join(
            chr(int(round(char))) for char in compressed_signal
            if 0 <= round(char) < 128  # Ensure valid ASCII range
        )
        return compressed_message


# Example Usage
network = FriendNetwork()
network.add_friend("Alice")
network.add_friend("Bob")
network.add_friend("Charlie")
network.add_connection("Alice", "Bob")
network.add_connection("Bob", "Charlie")

message = "Hello, this is a test message."
lossiness = 0.5  # Keep 50% of the FFT coefficients

# Send a lossy compressed message
result = network.send_message("Alice", "Charlie", message, lossiness)
if result:
    print("Message sent:")
    print(result)

