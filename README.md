# JREPodcast
The Joe Rogan Experience Podcasts API

Sample Usage:

``` {.sourceCode .python}
#Downloads most recent podcasts

from JREPodcasts import jrepodcast

podcasts = jrepodcast.API()

for podcast in podcasts.recent():
  podcasts.download(path=path, episode=podcast['episode'])
