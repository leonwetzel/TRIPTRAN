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
            # input originates from separate values
            self.subject = args[0]
            self.predicate = args[1]
            self.object = args[2]
            self.lexical_examples = []
            self.theme = None
        elif isinstance(args[0], str):
            # input originates from XML file
            self.subject, self.predicate, self.object = args[0].split('|')
            self.lexical_examples = []
            self.theme = None

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

    def set_theme(self, theme):
        """Set the theme for the triple

        Parameters
        ----------
        theme : str
            Theme related to the triple.

        Returns
        -------
        None
        """
        self.theme = theme

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
        return self.__str__()
