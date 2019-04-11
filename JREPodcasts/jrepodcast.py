import requests
import urllib
from bs4 import BeautifulSoup, re, os
import vlc


class JREPodcastAPI(object):
    domain = 'http://podcasts.joerogan.net'
    mp3_url = 'http://traffic.libsyn.com/joeroganexp/'
        

    def searchFor(self, query=None, **kwargs):
        """Searches for a podcast
        Parameters:
        :query: - string to search ex.(episode, title)
        Returns:
            Results based on query parameters from most recent to oldest"""

        session = requests.Session()

        if kwargs.get('recent'):
            response = session.get(self.domain)
            return self._podcastParser(response.content).values()
        elif query is None:
            return(None)

        referer = '%s/?search=%s' % (self.domain, urllib.parse.quote(query))
        session.headers.update({'Referer': referer})

        form_data = {'search-terms': query, 'action': 'search_podcasts'}

        response = session.post(
            domain + '/wp-admin/admin-ajax.php',
            data=form_data,
            allow_redirects=True
        )

        html_content = response.json().get('response')

        podcasts = self._podcastParser(html_content)

        return(podcasts)

    def download(self, path, episode=None, url=None):
        assert os.path.isdir(path)

        if episode is not None:
            episode = str(episode)
            assert episode.isnumeric()

        elif url is not None:
            assert self.mp3_url in url

            episode = os.path.basename(url).replace('.mp3', '').strip('mashowp')

        podcast = self.searchFor(query=episode).get(0)

        saveasfile = os.path.join(
            path, '%s_%s_%s.mp3' % (
                episode,
                podcast['title'],
                podcast['date']
            )
        )

        r = requests.get(podcast['mp3_url'], stream=True)

        with open(saveasfile, 'wb') as dl:
            for chunk in r.iter_content(chunk_size=255):
                if chunk:
                    dl.write(chunk)
        print(f"Episode {episode} with {podcast['title']}, finished downloading!")
        return

    def streamAudio(self, url):

        stream = vlc.MediaPlayer(url)
        return(stream)

    def recent(self):
        return self.searchFor(recent=True)

    def _podcastParser(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        episodes = soup.find_all('div', attrs={'class': re.compile('episode ')})

        _podcasts_query = dict()

        for x, episode in enumerate(episodes):
            episode_num = episode.find('span', attrs={'class': 'episode-num'}).get_text().strip('#')
            podcast_date = episode.find('h3').get_text()
            desc = episode.find('div', attrs={'class': 'podcast-content'}).get_text()

            title = episode.find('div', attrs={'class': 'podcast-details'})
            title = title.find('h3').get_text()

            podcast_mp3 = '%s%s.mp3' % (
                self.mp3_url,
                'mmashow' + episode_num if 'mma' in title.lower() else 'p' + episode_num
            )

            dllinks = episode.find('ul', attrs={'class': 'download-links'})
            vimeo_link = dllinks.find('a')['href']

            _podcasts_query[x] = {
                'episode': episode_num,
                'title': title,
                'date': podcast_date,
                'desc': desc.encode(),
                'mp3_url': podcast_mp3,
                'vimeo_url': vimeo_link
            }
        return(_podcasts_query)