from queryDownloads import replace_readme_comments,get_downloads_from_url,get_developers_app_total_downloads
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	# https://apps.garmin.cn/zh-CN/apps/dc6ceca8-6ec6-49f2-b711-4ebc0d347177
	parser.add_argument("readme_file_name", help="readme_file_name")
	parser.add_argument("badge_pattern", help="badge_pattern")
	parser.add_argument('developer_id', help="developer id. e.g. cdc2c15c-3ac3-46c6-99ec-a9c0f4a135e0 from https://apps.garmin.com/en-US/developer/cdc2c15c-3ac3-46c6-99ec-a9c0f4a135e0/apps")

	options = parser.parse_args()
	print(options)
	count = get_developers_app_total_downloads(options.developer_id)
	replace_readme_comments(options.readme_file_name,options.badge_pattern,count)