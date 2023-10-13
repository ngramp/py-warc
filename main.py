
directory = ""

warcFile = getNextWarcFile(directory)
webpage = getWebpage(warcFile)
filtered_text = getFilteredText(webpage)
entities = getEntities(filtered_text)

topics = getTopics(filtered_text)

