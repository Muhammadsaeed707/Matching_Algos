import random
import sys
import argparse

class Packet:
    def __init__(self, input_port, output_port, arrival_tick):
        self.input_port  = input_port
        self.output_port = output_port
        self.arrival_tick= arrival_tick

class FifoSimulator:
    def __init__(self, num_ports, arrival_prob, seed, simulation_ticks=20000):
        random.seed(seed)
        self.num_ports = num_ports
        self.arrival_prob = arrival_prob
        self.simulation_ticks = simulation_ticks

        # variables to compute average delay of packets transmitted out of output ports
        self.delay_count = 0
        self.delay_sum   = 0.0

        # One input queue for each input port
        # Initialized to empty queue for each input port
        self.input_queues = []
        for input_port in range(num_ports):
            self.input_queues += [[]]

    def run_simulator(self):
        # Main simulator loop: Loop over ticks
        for tick in range(self.simulation_ticks):
            # Tick every input port
            for input_port in range(self.num_ports):
                # Is there a packet here?
                if (random.random() < self.arrival_prob):
                  # If so, pick output port uniformly at random
                  output_port = random.randint(0, self.num_ports - 1)
                  self.input_queues[input_port] += [Packet(input_port, output_port, tick)]

            self.fifo(tick)

            # Average delay printing
            if (tick % 100 == 0):
                print ("Average delay after ", tick, " ticks = ", self.delay_sum / self.delay_count, " ticks")
            print()

    def fifo(self, tick):
        # TODO: Implement FIFO algorithm:
        # First, look at all the head packets, i.e., packets at the head of each of the input_queues
        # Second, If multiple inputs have head packets destined to the same output port,
        # pick an input port at random, and deq from that. Repeat for each output port.

        # More detailed instructions for FIFO algorithm:
        # First, populate a dictionary d that maps an output port to the list of all packets destined to that output.

        # Set dictionary as dict
        dict = {}
        # Iterate through input queues with for loops
        for input_queue in self.input_queues:
            # Check is length is greater than 0
            if len(input_queue) > 0:
                # Check if value is in dictionary or not 
                if input_queue[0].output_port not in dict:
                    # Create list for key value 
                    dict[input_queue[0].output_port] = []
                # Add value to said key
                dict[input_queue[0].output_port].append(input_queue[0])

        # Second, for each output port o, pick one of the packets in the list d[o] at random
        # To pick one packet out of a list at random, you can use the random.choice function.
        # Note: To complete the matching for an input port i that was picked and hence matched to an output port,
        # dequeue from that input port's queue (input_queues[i])

        # Iterate through output ports in dictionary
        for output_port in dict:
            # Set value to remove to variable remove 
            remove = random.choice(dict[output_port])
            # Set variable packet to relevant value 
            packet = dict[output_port].pop(dict[output_port].index(remove))
            # Pop variable remove out 
            self.input_queues[packet.input_port].pop(0)
            # Iterate 
            self.delay_sum += (tick-packet.arrival_tick)
            self.delay_count +=1

        # Remember to update the average delay based on the packets that were just dequeued.
        # Otherwise, your average delay will be 0/0 because no samples would have been accumulated.


if __name__ == "__main__":
    # Usage for command line arguments
    parser = argparse.ArgumentParser(
        description="Assignment 4."
    )
    parser.add_argument(
        "-p",
        "--num_ports",
        type=int,
        help="The number of ports on the router"
    )
    parser.add_argument(
        "-a",
        "--arrival_prob",
        type=float,
        help="The probability that a packet arrives"
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="The seed for the random number generator"
    )
    args = parser.parse_args()
    simulator = FifoSimulator(args.num_ports, args.arrival_prob, args.seed)
    simulator.run_simulator()
