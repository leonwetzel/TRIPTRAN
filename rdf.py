class Triple:
    """
    Describes an RDF triple.
    """
    def __init__(self, *args):
        """
        Constructs an RDF triple, using the given values.
        This triple is also known as a delexicalised triple.
        :param subject:
        :param predicate:
        :param object:
        """
        if not args:
            raise ValueError(
                "Cannot construct Triple without argument values! Enter "
                "either a string, or subject, predicate and object values.")

        if len(args) == 3:
            self.subject = args[0]
            self.predicate = args[1]
            self.object = args[2]
        elif isinstance(args[0], str):
            # TODO: extract_triples implementeren
            pass

    def __str__(self):
        """
        Returns the delexicalised triple.
        :return:
        """
        return f"{self.subject} {self.predicate} {self.object}"
