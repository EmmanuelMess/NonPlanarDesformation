from abc import ABCMeta


class DeformerState(metaclass=ABCMeta):  # pylint: disable=too-few-public-methods
    """
    Generic state for passing data from deformers to undeformers
    """
