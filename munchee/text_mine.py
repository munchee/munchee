from nltk import word_tokenize, FreqDist, Text
from nltk.stem import SnowballStemmer
import wikipedia
from math import sqrt


exclude_words = "would there their about which because person people could other after these given while, \
monday tuesday wednesday thursday friday saturday sunday january february march april may june \
july august september october november december moved include around between announce provide include \
first second third fourth fifth sixth seventh eigth ninth tenth one two three four five six seven eight \
nine ten"
ewl = word_tokenize(exclude_words)


def get_most_occured(text, common_num=25):
	word_list = word_tokenize(text.lower())
	filtered_list = [w for w in word_list if (len(w)>4 and w not in ewl)]

	common_num = min(common_num, len(filtered_list))

	return FreqDist(Text(filtered_list)).most_common(common_num)

def get_match_percentage(companytxt, fd_user_ls, company_common_num=50):
	wl_companytxt = word_tokenize(companytxt.lower())
	company_common_num = min(company_common_num, len(wl_companytxt))

	snowball_stemmer = SnowballStemmer("english")
	stemmed_fl_companytxt = [snowball_stemmer.stem(w) for w in wl_companytxt if (len(w)>4 and w not in ewl)]
	fd_company = FreqDist(Text(stemmed_fl_companytxt)).most_common(company_common_num+2)[2:]

	print(fd_company)
	print(fd_user_ls)

	rankings = []
	for i in range(len(fd_company)):
		word = fd_company[i][0]
		if word in fd_user_ls:
			rankings.append(company_common_num-i-1)
	max_score = sum(range(company_common_num)[company_common_num-len(fd_user_ls):])

	if max_score == 0:
		return 0

	return sqrt((sum(rankings)/max_score)*100)*10

def stemmed_top_user_words(usertxt, num=10):
	wl_usertxt = word_tokenize(usertxt.lower())
	num = min(num, len(wl_usertxt))

	snowball_stemmer = SnowballStemmer("english")
	stemmed_fl_usertxt = [snowball_stemmer.stem(w) for w in wl_usertxt if (len(w)>4 and w not in ewl)]
	fd_user_ls = [w[0] for w in FreqDist(Text(stemmed_fl_usertxt)).most_common(num)]

	return fd_user_ls

if __name__ == "__main__":
	wikipage = wikipedia.page("Facebook, company, inc.")
	text_wk = wikipage.content
	personal = "technology, job, software, internship, "
	text_ps = personal

	user_words = stemmed_top_user_words(text_ps, num=10)
	print(get_match_percentage(text_wk,user_words))