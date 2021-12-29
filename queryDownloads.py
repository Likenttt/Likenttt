import regex
import re
import argparse
import os
import requests


# badge_pattern like CIQ_Store_downloads-{}-green
def replace_readme_comments(file_name, badge_pattern, downloads):
    with open(file_name, "r+") as f:
        text = f.read()
        badge_pattern_regex = badge_pattern.format('\\d{1,10}')
        # regrex sub from github readme comments
        text = re.sub(badge_pattern_regex,
                      badge_pattern.format(downloads),
                      text,
                      flags=re.DOTALL,
                      )
        f.seek(0)
        f.write(text)
        f.truncate()


def extract_downloads_from_html(html_text):
    searchObj = regex.search(r'[^><]+(?<=\d+)(?=<\/span>)', html_text)
    assert searchObj, 'Nothing found!!'
    return searchObj[0]


def extract_app_url_from_homepage(html_text):
    searchObj = regex.findall(r'/en-US/apps/[0-9a-z\-]{0,36}', html_text)
    assert searchObj, 'Nothing found!!'
    print('searchObj are:'.format(searchObj))
    s = set()
    for item in searchObj:
        s.add(item)
    return s


def get_developers_app_total_downloads(developer_id):
    developer_home_page_url = 'https://apps.garmin.com/en-US/developer/{}/apps'.format(developer_id)
    html_text = get_html_text_from_url(developer_home_page_url)
    apps_uri_set = extract_app_url_from_homepage(html_text)
    count = 0
    for uri in apps_uri_set:
        if uri is not None:
            ciq_download_intl = get_downloads_from_url('https://apps.garmin.com' + uri)
            ciq_download_china = get_downloads_from_url('https://apps.garmin.cn' + uri)
            if ciq_download_intl and ciq_download_china:
                downloads = int(ciq_download_intl) + int(ciq_download_china)
                count += downloads
    return count


def get_html_text_from_url(url):
    print('requesting {}'.format(url))
    res = requests.get(url)
    html_text = res.content
    print('html text is \n {}'.format(html_text))
    return html_text.decode('utf-8')


def get_downloads_from_url(url):
    html_text = get_html_text_from_url(url)
    return extract_downloads_from_html(html_text)


def main(ciq_id, badge_pattern, readme_file_name):
    ciq_download_intl = get_downloads_from_url('https://apps.garmin.com/zh-CN/apps/' + ciq_id)
    ciq_download_china = get_downloads_from_url('https://apps.garmin.cn/zh-CN/apps/' + ciq_id)
    if ciq_download_intl and ciq_download_china:
        downloads = int(ciq_download_intl) + int(ciq_download_china)
        print('app download is {}'.format(downloads))
        replace_readme_comments(readme_file_name, badge_pattern, downloads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # https://apps.garmin.cn/zh-CN/apps/dc6ceca8-6ec6-49f2-b711-4ebc0d347177
    parser.add_argument("ciq_id", help="ciq_id")
    parser.add_argument("badge_pattern", help="badge_pattern")
    parser.add_argument("readme_file_name", help="readme_file_name")

    options = parser.parse_args()
    main(options.ciq_id, options.badge_pattern, options.readme_file_name)
