from .commons        import Generator, GeneratorError
from random          import choice

from praw            import Reddit
from praw.exceptions import MissingRequiredAttributeException
from requests        import get
from urllib.parse    import urlparse

class Reddit_partial(Generator):
    """Partial implementation of a generator which seeks through
    a limited amount of subreddits that has content for memes."""

    _DOMAINS = ['i.imgur.com', 'i.redd.it']
    _INTR_SOURCES = '+'.join([
        'memes',
        'dankmemes',
        'me_irl',
        'ProgrammerHumor',
        'PewdiepieSubmissions',
        'linuxmemes',
    ])

    def __init__(self, id: str, secret: str):
        """Initalize a PRAW for grabbing contents of sub-reddits.
        - `id`     — Client ID of reddit app.
        - `secret` — Client Secret of reddit app.
        """
        try:
            self._rctx = Reddit(
                client_id=id, client_secret=secret,
                user_agent=self.__class__.__name__)
        except MissingRequiredAttributeException:
            raise GeneratorError("required attributes were invalid")
    
    def __call__(self):
        """Upon calling selects a random subreddit and selects
        a random post, provides 'title' and 'author' extradata."""

        # choose a random meme image from a random sub-reddit,
        # note: this only picks image URLs and nothing else.        
        img = None
        while img is None or not urlparse(img.url)[1] in self._DOMAINS:
          img = self._rctx.subreddit(self._INTR_SOURCES).random()
        
        return (img.url,
          {'title': img.title, 'author': img.author})
