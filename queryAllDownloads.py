from queryDownloads import replace_readme_comments
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # https://apps.garmin.cn/zh-CN/apps/dc6ceca8-6ec6-49f2-b711-4ebc0d347177
    parser.add_argument("readme_file_name", help="readme_file_name")
    parser.add_argument("badge_pattern", help="badge_pattern")
    parser.add_argument('--ciq_id_list', nargs='+')

	count = 0
	options = parser.parse_args()
	for _, ciq_id in options.ciq_id_list:
	    if ciq_id is not None:
	        ciq_download_intl = get_downloads_from_url('https://apps.garmin.com/zh-CN/apps/' + ciq_id)
		    ciq_download_china = get_downloads_from_url('https://apps.garmin.cn/zh-CN/apps/' + ciq_id)
		    if ciq_download_intl and ciq_download_china:
		        downloads = int(ciq_download_intl) + int(ciq_download_china)
		        count += ciq_id
	replace_readme_comments(options.readme_file_name,options.badge_pattern,count)