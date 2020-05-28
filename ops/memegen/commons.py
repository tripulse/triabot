from typing import Union, IO
from abc    import ABC, ABCMeta, abstractmethod

class GeneratorError(Exception):
    """While doing initialization or processing the generator
    had failed todo its job properly, this can cause if the
    internal API it is using had failed to do it's job."""
    pass

class Generator(ABC, metaclass=ABCMeta):
    """A generator is a class which does internal processing
    or doesn't do anything to return a URL-like object which
    refers to an image. Some properties of it are:
    
    - Perform HTTP requests (eg. with `urllib`).
    - Use external dependencies (eg. `praw`).
    """

    @abstractmethod
    def __call__(self) -> (Union[IO, str], dict):
        """Upon calling it returns a URL reffering to an image
        file and some extradata of the extractor as a dictionary."""
        pass