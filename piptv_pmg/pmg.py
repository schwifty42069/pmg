import os
import sys
import getopt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class M3UWriter(object):
    def __init__(self, write_dir):
        # Test to see if requests can be sent to CDN nodes
        self.cdn_nodes = ['peer1.savitar.tv', 'peer2.savitar.tv', 'peer3.savitar.tv',
                          'peer4.savitar.tv', 'live.savitar.tv']

        self.channel_codes = ['ABCE', 'A&E', 'AMC', 'APL', 'BBCA', 'BET', 'BOOM', 'BRVO', 'CNE', 'CBSE', 'CMT', 'CNBC',
                              'CNN', 'COM', 'DEST', 'DSC', 'DISE', 'DISJR', 'DXD', 'DIY', 'E!', 'ESPN', 'ESPN2', 'FOOD',
                              'FBN', 'FOXE', 'FNC', 'FS1', 'FS2', 'FREEFM', 'FX', 'FXM', 'FXX', 'GOLF', 'GSN', 'HALL',
                              'HMM', 'HBO', 'HGTV', 'HIST', 'HLN', 'ID', 'LIFE', 'LIFEMOV', 'MLBN', 'MTHD', 'MSNBC',
                              'MTV', 'NGW', 'NGC', 'NBA', 'NBCSN', 'NBCE', 'NFLHD', 'NIKE', 'NKTN', 'OWN', 'OXGN', 'PAR',
                              'PBSE', 'POP', 'SCI', 'SHO', 'STARZ', 'SUND', 'SYFY', 'TBS', 'TCM', 'TELE', 'TNNS', 'CWE',
                              'WEATH', 'TLC', 'TNT', 'TRAV', 'TruTV', 'TVLD', 'UNVSO', 'USA', 'VH1', 'WE']

        self.cdn_channel_codes = ['ABC', 'AE', 'AMC', 'Animal', 'BBCAmerica', 'BET', 'Boomerang', 'Bravo', 'CN', 'CBS',
                                  'CMT', 'CNBC', 'CNN', 'Comedy', 'DA', 'Discovery', 'Disney', 'DisneyJr', 'DisneyXD',
                                  'DIY', '']

        self.links = ['http://ustvgo.tv/abc-live-streaming-free/', 'http://ustvgo.tv/ae-networks-live-streaming-free/',
                      'http://ustvgo.tv/amc-live/', 'http://ustvgo.tv/animal-planet-live/',
                      'http://ustvgo.tv/bbc-america-live/', 'http://ustvgo.tv/bet/', 'http://ustvgo.tv/boomerang/',
                      'http://ustvgo.tv/bravo-channel-live-free', 'http://ustvgo.tv/cartoon-network-live-streaming-free',
                      'http://ustvgo.tv/cbs-live-streaming-free/', 'http://ustvgo.tv/cmt/',
                      'http://ustvgo.tv/cnbc-live-streaming-free/', 'http://ustvgo.tv/cnn-live-streaming-free/',
                      'http://ustvgo.tv/comedy-central-live-free/', 'http://ustvgo.tv/destination-america/',
                      'http://ustvgo.tv/discovery-channel-live/', 'http://ustvgo.tv/disney-channel-live-streaming-free/',
                      'http://ustvgo.tv/disneyjr/', 'http://ustvgo.tv/disneyxd/', 'http://ustvgo.tv/diy/',
                      'http://ustvgo.tv/e/', 'http://ustvgo.tv/espn-live/', 'http://ustvgo.tv/espn2/',
                      'http://ustvgo.tv/food-network-live-free/', 'http://ustvgo.tv/fox-business-live-streaming-free/',
                      'http://ustvgo.tv/fox-hd-live-streaming/', 'http://ustvgo.tv/fox-news-live-streaming-free/',
                      'http://ustvgo.tv/fox-sports-1/', 'http://ustvgo.tv/fox-sports-2/',
                      'http://ustvgo.tv/freeform-channel-live-free/', 'http://ustvgo.tv/fx-channel-live/',
                      'http://ustvgo.tv/fxm/', 'http://ustvgo.tv/fxx/', 'http://ustvgo.tv/golf-channel-live-free/',
                      'http://ustvgo.tv/gsn/', 'http://ustvgo.tv/hallmark-channel-live-streaming-free/',
                      'http://ustvgo.tv/hallmark-movies-mysteries-live-streaming-free/', 'http://ustvgo.tv/hbo/',
                      'http://ustvgo.tv/hgtv-live-streaming-free/', 'http://ustvgo.tv/history-channel-live/',
                      'http://ustvgo.tv/hln/', 'http://ustvgo.tv/investigation-discovery-live-streaming-free/',
                      'http://ustvgo.tv/lifetime-channel-live/', 'http://ustvgo.tv/lifetime-movies/',
                      'http://ustvgo.tv/mlb-network/', 'http://ustvgo.tv/motortrend/',
                      'http://ustvgo.tv/msnbc-live-streaming-free/', 'http://ustvgo.tv/mtv/',
                      'http://ustvgo.tv/nat-geo-wild-live/', 'http://ustvgo.tv/national-geographic-live/',
                      'http://ustvgo.tv/nba-tv/', 'http://ustvgo.tv/nbc-sports/', 'http://ustvgo.tv/nbc/',
                      'http://ustvgo.tv/nfl-network-live-free/', 'http://ustvgo.tv/nickelodeon-live-streaming-free/',
                      'http://ustvgo.tv/nicktoons/', 'http://ustvgo.tv/own/', 'http://ustvgo.tv/oxygen/',
                      'http://ustvgo.tv/paramount-network/', 'http://ustvgo.tv/pbs-live/', 'http://ustvgo.tv/pop/',
                      'http://ustvgo.tv/science/', 'http://ustvgo.tv/showtime/', 'http://ustvgo.tv/starz-channel-live/',
                      'http://ustvgo.tv/sundance-tv/', 'http://ustvgo.tv/syfy-channel-live/',
                      'http://ustvgo.tv/tbs-channel-live-free/', 'http://ustvgo.tv/tcm/', 'http://ustvgo.tv/telemundo/',
                      'http://ustvgo.tv/tennis-channel-live-free/', 'http://ustvgo.tv/the-cw-live-streaming-free/',
                      'http://ustvgo.tv/the-weather-channel-live-streaming-free/', 'http://ustvgo.tv/tlc-live-free/',
                      'http://ustvgo.tv/tnt/', 'http://ustvgo.tv/travel-channel-live-free/', 'http://ustvgo.tv/trutv/',
                      'http://ustvgo.tv/tv-land-live-free/', 'http://ustvgo.tv/univision/',
                      'http://ustvgo.tv/usa-network-live/', 'http://ustvgo.tv/vh1/', 'http://ustvgo.tv/we-tv/']

        self.write_dir = write_dir
        self.profile = webdriver.FirefoxProfile()
        self.profile.add_extension("../resource/har_export_trigger-0.6.1.xpi")
        self.options = FirefoxOptions()
        # self.options.add_argument("-headless")
        self.options.add_argument("-devtools")
        self.driver = webdriver.Firefox(self.profile, firefox_options=self.options)
        self.renew_token_node = 'http://ustvgo.tv/nfl-network-live-free'
        self.wms_auth_token = {}
        self.scraped_links = []

        self.export_har_js = \
            """return HAR.triggerExport().then(harLog => {
                   for (r of harLog.entries) {
                       if (r.request.url.includes("m3u8")) { 
                           return r.request;
                       }
                   }
               });"""

    @staticmethod
    def assemble_hotlink(node, channel, token):
        return "http://{}/{}/myStream/playlist.m3u8?wmsAuthSign={}".format(node, channel, token)

    def retrieve_new_token(self):
        """ # The old logic
        scraper = cfscrape.create_scraper()
        for link in self.links:
            req = requests.get(link)
            if req.status_code == 503:
                bsoup = Soup(scraper.get(link).content, 'html.parser')
            else:
                bsoup = Soup(req.text, 'html.parser')
            for s in bsoup.findAll("script"):
                if "player.setup" in str(s):
                    self.scraped_links.append(s.next_element.split(" file: ")[1].split(',')[0].strip("\'"))
                    """
        self.driver.get(self.renew_token_node)
        # use this to update wmsAuth token, build out calls to cdn root nodes for m3u
        req = self.driver.execute_script(self.export_har_js)
        self.wms_auth_token.update({req['queryString'][0]['name']: req['queryString'][0]['value']})

    def initialize_m3u_file(self):
        if os.path.exists(self.write_dir):
            os.remove(self.write_dir)
            with open(self.write_dir, "w") as writer:
                writer.write('')
                writer.close()
        else:
            with open(self.write_dir, "w") as writer:
                writer.write('')
                writer.close()

    def write_m3u_chunk(self, channel_code, url):
        with open(self.write_dir, "a") as writer:
            writer.write("#EXTM3U\n")
            writer.write("#EXTINF: -1,{}\n".format(channel_code))
            writer.write("{}\n\n".format(url))
            writer.close()

    def feed_chunk_writer(self):
        for code, link in zip(self.channel_codes, self.scraped_links):
            self.write_m3u_chunk(code, link)


def main(argv):
    write_dir = ''
    try:
        opts, args = getopt.getopt(argv, "h:o:", ["output="])
    except getopt.GetoptError:
        print('pmg.py -o <outputfile>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('pmg.py -o <outputfile>')
            sys.exit()
        elif opt in ("-o", "--output"):
            write_dir = arg
    if write_dir == '':
        print('pmg.py -o <outputfile>')
        sys.exit()
    mw = M3UWriter(write_dir)
    mw.retrieve_new_token()
    mw.initialize_m3u_file()
    mw.feed_chunk_writer()


if __name__ in "__main__":
    main(sys.argv[1:])







