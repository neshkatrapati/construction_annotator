def split_sentence(sentence):
	s = sentence.plain_form.split(' ')
	return [(index, w) for index, w in enumerate(s)]