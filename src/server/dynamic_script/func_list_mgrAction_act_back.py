def main(page_type):
	if page_type is None or len(page_type) == 0:
		return "#"
	elif page_type == 'LIST':
		return 'list/?page=MGR_LIST_COL'
	return ""