import os
import shutil
import sys
import getopt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import random
import platform
import time


class M3UWriter(object):
    def __init__(self, write_dir):
        try:
            import piptv_pmg.pmg
            print("\nFound installed as module!\n")
            self.is_installed_as_module = True
        except ModuleNotFoundError:
            self.is_installed_as_module = False
        # Test to see if requests can be sent to CDN nodes
        self.cdn_nodes = ['peer1.savitar.tv', 'peer2.savitar.tv', 'peer3.savitar.tv', 'live.savitar.tv']

        self.channel_codes = ['ABCE', 'A&E', 'AMC', 'APL', 'BBCA', 'BET', 'BOOM', 'BRVO', 'CNE', 'CBSE', 'CMT', 'CNBC',
                              'CNN', 'COM', 'DEST', 'DSC', 'DISE', 'DISJR', 'DXD', 'DIY', 'E!', 'ESPN', 'ESPN2', 'FOOD',
                              'FBN', 'FOXE', 'FNC', 'FS1', 'FS2', 'FREEFM', 'FX', 'FXM', 'FXX', 'GOLF', 'GSN', 'HALL',
                              'HMM', 'HBO', 'HGTV', 'HIST', 'HLN', 'ID', 'LIFE', 'LIFEMOV', 'MLBN', 'MTHD', 'MSNBC',
                              'MTV', 'NGW', 'NGC', 'NBA', 'NBCSN', 'NBCE', 'NFLHD', 'NIKE', 'NKTN', 'OWN', 'OXGN',
                              'PAR', 'PBSE', 'POP', 'SCI', 'SHO', 'STARZ', 'SUND', 'SYFY', 'TBS', 'TCM', 'TELE', 'TNNS',
                              'CWE', 'WEATH', 'TLC', 'TNT', 'TRAV', 'TruTV', 'TVLD', 'UNVSO', 'USA', 'VH1', 'WE']

        self.cdn_channel_codes = ['ABC', 'AE', 'AMC', 'Animal', 'BBCAmerica', 'BET', 'Boomerang', 'Bravo', 'CN', 'CBS',
                                  'CMT', 'CNBC', 'CNN', 'Comedy', 'DA', 'Discovery', 'Disney', 'DisneyJr', 'DisneyXD',
                                  'DIY', 'E', 'ESPN', 'ESPN2', 'FoodNetwork', 'FoxBusiness', 'FOX', 'FoxNews', 'FS1',
                                  'FS2', 'Freeform', 'FX', 'FXMovie', 'FXX', 'GOLF', 'GSN', 'Hallmark', 'HMM', 'HBO',
                                  'HGTV', 'History', 'HLN', 'ID', 'Lifetime', 'LifetimeM', 'MLB', 'MotorTrend', 'MSNBC',
                                  'MTV', 'NatGEOWild', 'NatGEO', 'NBA', 'NBCSN', 'NBC', 'NFL', 'Nickelodeon',
                                  'Nicktoons', 'OWN', 'Oxygen', 'Paramount', 'PBS', 'POP', 'Science', 'Showtime',
                                  'StarZ', 'SundanceTV', 'SYFY', 'TBS', 'TCM', 'Telemundo', 'Tennis', 'CWE',
                                  'https://weather-lh.akamaihd.net/i/twc_1@92006/master.m3u8', 'TLC', 'TNT', 'Travel',
                                  'TruTV', 'TVLand', 'Univision', 'USANetwork', 'VH1', 'WETV']

        self.write_dir = write_dir
        self.profile = webdriver.FirefoxProfile()
        self.options = FirefoxOptions()
        # Need to configure a VM for macOS testing
        if platform.system() == "Windows" and self.is_installed_as_module:
            print("\nDetected windows...\n \nTrying to set environment variable for geckodriver\n")
            self.resource_dir = str(os.path.abspath(piptv_pmg.pmg.__file__)).split("pmg.py")[0] + "\\resource\\"
            self.set_environment_variable(self.resource_dir + "\\geckodriver_win64")
        elif platform.system() == "Windows" and not self.is_installed_as_module:
            self.resource_dir = os.getcwd().split("piptv_pmg")[0] + "\\resource\\"
            self.set_environment_variable(self.resource_dir + "\\geckodriver_win64")
        elif platform.system() == "Linux" and self.is_installed_as_module:
            self.resource_dir = str(os.path.abspath(piptv_pmg.pmg.__file__)).split("pmg.py")[0] + "/resource/"
            if not os.path.exists("/usr/bin/geckodriver"):
                shutil.copyfile(self.resource_dir + 'geckodriver_linux64/geckodriver', '/usr/bin/geckodriver')
        elif platform.system() == "Linux" and not self.is_installed_as_module:
            self.resource_dir = os.getcwd().split("piptv_pmg")[0] + "/resource/"
            if not os.path.exists("/usr/bin/geckodriver"):
                shutil.copyfile(self.resource_dir + 'geckodriver_linux64/geckodriver', '/usr/bin/geckodriver')
        self.options.add_argument("-headless")
        self.options.add_argument("-devtools")
        if platform.system() == "Windows":
            self.driver = webdriver.Firefox(self.profile, options=self.options)
            self.driver.install_addon(self.resource_dir + "har_export_trigger-0.6.1.xpi",
                                      temporary=True)
        elif platform.system() == "Linux":
            print("\nDetected Linux...\n")
            self.profile.add_extension(self.resource_dir + "har_export_trigger-0.6.1.xpi")
            self.driver = webdriver.Firefox(self.profile, options=self.options)

        self.renew_token_node = 'http://ustvgo.tv/nfl-network-live-free'
        self.wms_auth_token = {}
        self.generated_links = []

        self.export_har_js = \
            """return HAR.triggerExport().then(harLog => {
                   for (r of harLog.entries) {
                       if (r.request.url.includes("m3u8")) { 
                           return r.request;
                       }
                   }
               });"""

    @staticmethod
    def set_environment_variable(gecko_path):
        os.environ['PATH'] = os.environ['PATH'] + ";" + gecko_path

    def assemble_hotlink(self, node, channel):
        self.generated_links.append("http://{}/{}/myStream/playlist.m3u8?wmsAuthSign={}".format(
            node, channel, self.wms_auth_token['wmsAuthSign']))

    def generate_links(self):
        print("\nGenerating links...\n")
        for channel in self.cdn_channel_codes:
            if "weather" in channel:
                self.generated_links.append(channel)
            else:
                x = random.randrange(4)
                self.assemble_hotlink(self.cdn_nodes[x], channel)

    def retrieve_new_token(self):
        self.driver.get(self.renew_token_node)
        time.sleep(5)
        req = self.driver.execute_script(self.export_har_js)
        self.wms_auth_token.update({req['queryString'][0]['name']: req['queryString'][0]['value']})
        print("\nRetrieved token:\n\n{}\n".format(self.wms_auth_token['wmsAuthSign']))
        self.driver.quit()

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
        print("\nWriting M3U...\n")
        for code, link in zip(self.channel_codes, self.generated_links):
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
    mw.generate_links()
    mw.initialize_m3u_file()
    mw.feed_chunk_writer()


if __name__ in "__main__":
    main(sys.argv[1:])
