import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from string import ascii_uppercase

class FSM:
    """Finite State Machine"""
    def __init__(self, sequence):
        self.sequence = self._validate(sequence)
        self.graph = nx.MultiDiGraph()

        self.num_states = len(self.sequence)

        self.graph_options = {
        'font_color': 'white',
        'width': 2,
        'label': f"FSM for {self.sequence}"
        }

    def _validate(self, sequence):
        if not (set(sequence) == set("01") or set(sequence) == set("0") or set(sequence) == set("1")):
            raise Exception(f"Parse error: Invalid binary sequence `{sequence}`")
        else:
            return sequence

    def build_fsm(self):
        raise NotImplementedError("`build_fsm` not implemented")

    def render_fsm(self):
        pos = nx.nx_agraph.graphviz_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'seq')

        nx.draw(self.graph,
                pos,
                arrows=True,
                with_labels=True,
                **self.graph_options)

        A = to_agraph(self.graph)
        A.draw(path="graph.svg", format="svg", prog="dot")

    def get_state_name(self, num, alphabet=ascii_uppercase):
        """Number to state name
        Base 26 encoding
        """
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        
        while num:
            num, rem = divmod(num, base)
            print(num, rem)
            arr.append(alphabet[rem])
        arr.reverse()

        return ''.join(arr)

    def get_state_matching_pattern(self, pattern):
        """Given a `pattern`, find a state that expects it"""
        for i in range(len(pattern)):
            pattern_to_match = pattern[i:]

            print(f"Matching pattern: {pattern_to_match}")
        
            for state in range(self.num_states-1, -1, -1):
                expected_pattern = self.sequence[:state]

                if expected_pattern == pattern_to_match:
                    print(f"Found match, next state: {self.get_state_name(state)}")
                    return self.get_state_name(state)

        return None


class Moore(FSM):
    """Moore Machine"""
    def __init__(self, sequence):
        super().__init__(sequence)

        # Final state is extra
        self.num_states = len(self.sequence) + 1

        # Build the fsm
        self.build_fsm()


    def build_fsm(self):
        # Add nodes
        for state in range(self.num_states):
            node = self.get_state_name(state)
            self.graph.add_node(node)

        # Add edges
        for state in range(self.num_states):
            # Sequence till now
            prev_seq = self.sequence[:state]
            # Positive
            positive = self.sequence[state-1]
            # Negative
            negative = "0" if self.sequence[state-1] == "1" else "1"

            print(f"prev_seq: {prev_seq}, positive: {positive}, negative: {negative}")

            src = self.get_state_name(state)
            dst = None

            # Positive edge
            dst = self.get_state_matching_pattern(prev_seq + positive)
            if dst is None: dst = self.get_state_name(0)
            self.graph.add_edge(src, dst, label=positive)

            # Negative edge
            dst = self.get_state_matching_pattern(prev_seq + negative)
            if dst is None: dst = self.get_state_name(0)
            self.graph.add_edge(src, dst, label=negative)


if __name__ == "__main__":
    seq = input("Enter binary input sequnce to detect : ")
    
    myFSM = Moore(seq)
    myFSM.render_fsm()



