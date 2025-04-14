class LabelOrder:
    def __init__(self, name, label, neighbors_labels, nodes, preceds):
        self._name = name
        self._label = label
        self._neighbors_labels = neighbors_labels
        self._nodes = nodes
        self._preceds=preceds
        
    def __str__(self):
       
        
        return (
                f"{self._name}: "
                f"{self._label}.{{{', '.join(map(str, self._neighbors_labels))}}}"
                f" nodes: {{{', '.join(map(str, self._nodes))}}}"
                f"  preceds: {{{', '.join(map(str, self._preceds))}}}"
                )

    def add_node(self, value):
        self._nodes.append(value)