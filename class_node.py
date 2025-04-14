class Node:
    def __init__(self, name, label, neighbors_labels, domain, ispattern):
        self._name = name
        self._label = label
        self._neighbors_labels = neighbors_labels
        self._domain = domain
        self._ispattern = ispattern

    def __str__(self):
        if self._label is not None:  # Explicitly check for None
            alpha = "\u03B1"
            result = f"{alpha}({self._name}): "
            if len(self._neighbors_labels) > 0:
                result += f"{self._label}.{{{', '.join(map(str, self._neighbors_labels))}}} "
            else:
                result += f"{self._label} "
        else:
            result = f"{self._name}: "
        
        if self._ispattern:
            result += f", dom(x_{self._name})= & {{{', '.join(map(str, self._domain))}}}"
        
        return result
