# JREPodcast
The Joe Rogan Experience Podcasts API

Sample Usage:

``` {.sourceCode .python}
#Downloads most recent podcasts

>>> from JREPodcasts import jrepodcast

>>> podcasts = jrepodcast.API()

#Get Recent Updates (Podcasts from front page)
>>> podcasts.recent()

dict_values([{'episode': '1278', 'title': 'Kevin Hart', 'date': '04.06.19', 'desc': b'#1278. Kevin Hart is a\xc2\xa0comedian, actor and producer. His new stand up special is now streaming on Netflix.', 'mp3_url': 'http://traffic.libsyn.com/joeroganexp/p1278.mp3'},


#Search for a podcast
>>> podcasts.search("James Hetfield")

{0: {'episode': '887', 'title': 'James Hetfield', 'date': '12.16.16', 'desc': b'#887.\xc2\xa0James Hetfield is a musician, singer and songwriter known for being the co-founder, lead vocalist, rhythm guitarist and main songwriter for the American heavy metal band Metallica.\n', 'mp3_url': 'http://traffic.libsyn.com/joeroganexp/p887.mp3'}}

#Download a podcast by episode id or url (only as mp3 at the moment)
>>> podcasts.download(path='C:/temp', episode=887)

Episode 887 with James Hetfield, finished downloading!
