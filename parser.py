from bs4 import BeautifulSoup
import requests
import re
import json

TWITTER_COEFFICIENT = 1
FACEBOOK_COEFFICIENT = 1


class Media:
    def __init__(self, name):
        self.name = name
        self.facebook = 0
        self.twitter = 0
        self.url = ""
        self.rate = 0
        self.img = ""


def get_rates():
    base_url = "https://blog.feedspot.com/bitcoin_blogs/"
    html_text = requests.get(base_url).text

    soup = BeautifulSoup(html_text, 'html.parser')

    container = soup.find("div", {"id": "fsb"})

    h3_list = []
    for item in container.select("h3"):
        h3_list.append(Media(item.select("a")[0].text))

    i = 0
    for item in container.select("p"):
        try:

            h3_list[i].url = item.find("a", {"class": "ext"}).text
            h3_list[i].img = "https:" + item.select("img")[0]["data-lazy-src"]
            # h3_list[i].img = item.select("img")[0].find(attrs={"name": "stainfo"})
            # print(item.select("img")[0]["data-lazy-src"])
            try:
                facebook = int(re.search("Facebook fans ([0-9,\,]+)\.", item.text).group(1).replace(',', ''))
            except AttributeError:
                facebook = 0
            try:
                twitter = int(re.search("Twitter followers ([0-9,\,]+)\.", item.text).group(1).replace(',', ''))
            except AttributeError:
                twitter = 0
            h3_list[i].facebook = facebook
            h3_list[i].twitter = twitter
            h3_list[i].rate = facebook * FACEBOOK_COEFFICIENT + twitter * TWITTER_COEFFICIENT
            i += 1
        except AttributeError as err:
            print(err)

    h3_list = sorted(h3_list, key=lambda x: x.rate, reverse=True)
    toJSON = []
    for item in h3_list:
        # print(item.name, item.facebook, item.twitter, item.rate)
        toJSON.append(
            {'name': item.name, 'facebook': item.facebook, 'twitter': item.twitter, 'url': item.url, 'rate': item.rate,
             'img': item.img})
    JSON = json.dumps(toJSON, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': '))
    print(JSON)
    with open('data.json', 'w') as outfile:
        outfile.write(JSON)

    # for item in soup.select('table')[1].select('tr'):
    #     cols = item.select('td')
    #     if len(cols) > 5:
    #         name = cols[1].text.strip()
    #         rate = cols[5].text.strip()
    #         name = re.sub(r" \([\w]*\)", "", name)
    #         logo = base_url + item.select('img')[0]['src']
    #
    #         grades = {
    #             "Positive+": 100,
    #             "Positive": 90,
    #             "Stable+": 80,
    #             "Stable": 70,
    #             "Risky+": 60,
    #             "Risky": 50,
    #             "Risky-": 40,
    #             "Negative": 30,
    #             "Negative-": 20,
    #             "Default": 10,
    #         }
    #         raised = None
    #         raised_element = cols[6].select('span.blac-blue-collected')
    #         if raised_element:
    #             raised = raised_element[0].text.strip()
    #
    #         goal = None
    #         goal_element = cols[7].select('span.blac-blue-collected')
    #         if goal_element:
    #             goal = goal_element[0].text.strip()
    #         ico_page_link = item["data-href"]
    #         ico_page = requests.get(ico_page_link).text
    #         ico_soup = BeautifulSoup(ico_page, "html.parser")
    #         link = ico_soup.find(
    #             'span', text=" Website").parent.get('href')
    #         if name not in ratings:
    #             ratings[name] = Ico(name)
    #         ratings[name].add_rate(
    #             link, logo, goal, raised, address == "ico/preico", Rate("ICO Rating", rate, grades[rate]))


get_rates()
