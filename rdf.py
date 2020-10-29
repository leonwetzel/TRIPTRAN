class Triple:
    """
    Describes an RDF triple.
    """
    def __init__(self, *args):
        """
        Constructs an RDF triple, using the given values.
        This triple is also known as a delexicalised triple.
        """
        if not args:
            raise ValueError(
                "Cannot construct Triple without argument values! Enter "
                "either a string, or subject, predicate and object values.")

        if len(args) == 3:
            self.subject = args[0]
            self.predicate = args[1]
            self.object = args[2]
            self.lexical_examples = []
        elif isinstance(args[0], str):
            # input originates from XML file
            self.subject, self.predicate, self.object = args[0].split('|')
            self.lexical_examples = []

    def add_lexical_example(self, example):
        """
        Adds a lexical example to an RDF triple.
        The example reflects the subject, predicate
        and object values in a lexical way.
        :param example:
        :return:
        """
        self.lexical_examples.append(example)

    def remove_lexical_example(self, example):
        """
        Removes a lexical example from an
        RDF triple.
        :param example:
        :return:
        """
        self.lexical_examples.remove(example)

    def __str__(self):
        """
        Returns the delexicalised triple.
        :return:
        """
        return f"{self.subject} {self.predicate} {self.object}"

    def __repr__(self):
        """
        Returns the delexicalised triple.
        :return:
        """
        return f"{self.subject} {self.predicate} {self.object}"
