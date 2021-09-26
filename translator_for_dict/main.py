from googletrans import Translator

import requests


def main():
	translator = Translator()
	file = open("kap19.txt", "r")
	lines = file.readlines()
	verbs_condidates = []
	for i, line in enumerate(lines):
		(fp, sp) = line.split("] ")
		sp = sp.strip()
		w_translation = (str(translator.translate(sp, src="de", dest="en").text)).replace("the ", "").replace("The ", "").replace("that ", "")
		if not ("die" in sp or "der" in sp or "das" in sp):
			verbs_condidates.append([fp+  "] ", sp, " => " + w_translation])
		print(fp + "] " + sp + " => " + w_translation)

	print()
	print()
	print()
	link = "https://www.verbformen.de/konjugation/?w=" 
	for v in verbs_condidates:
		print(v[0]+v[1]+v[2])
		if "(" in v[1]:
			v[1] = ((v[1].split("("))[0]).strip()
		result = requests.get(link + v[1]).text.split("\n")
		for i, line in enumerate(result):
			if "<b>Präteritum</b>:" in line:
				ans = result[i+1].split(", wir")
				for a in ans[0].split(", "):
					print(a)
				break

		Partizip2 = ""
		for i, line in enumerate(result):
			if "<b>Partizip II</b>:" in line:
				Partizip2 = result[i+1]
				break
		
		flag = True
		for i, line in enumerate(result):
			if "<b>Perfekt</b>:" in line and flag:
				flag = False
				if "bin" in result[i+1]:
					print(Partizip2 + " (sein)")
				else:
					print(Partizip2 + " (haben)")
				# break
		print()

def main2():
	verbs_condidates = ["[16/0] angeln => fishing", "[16/0] malen => to paint", "[16/1.1] reiten => horse riding", "[16/1.3a] insgesamt => a total of", "[16/1.3a] sicher => for sure", "[16/1.3a] verbessern => improve", "[16/1.4] aktiv => active", "[16/2.1.a] aktuell => current", "[16/2.1.a] ausschlafen => sleep in", "[16/2.1.a] elektronisch => electronic", "[16/2.1.a] fortsetzen (sich) => continue (to)", "[16/2.1a] hektisch => hectic", "[16/2.1a] knapp => just", "[16/2.1a] regelmäßig => regularly", "[16/2.1a] sozial => social", "[16/2.1a] sparen => save up", "[16/2.1a] stressig => stressful", "[16/2.1a] teilnehmen an (etwas) => to take part in something)", "[16/2.1a] (sich) unterhalten => (talk", "[16/2.2] gern: am liebsten => like: favorite", "[16/2.5a] (sich) abtrocknen => (Be) dry", "[16/2.5a] (sich) eincremen => (to put lotion on", "[16/2.5a] (sich) rasieren => (shave", "[16/2.5a] (sich) schminken => (make up", "[16/2.5a] (sich) umziehen => (get changed", "[16/2.5a] zuerst => first", "[16/2.7] surfen => surfing", "[16/2.7] ungesund => unhealthy", "[16/3.1] betreiben => operate", "[16/3.1] renovieren => renovate", "[16/3.2] beobachten => observe", "[16/3.2] sich um etwas / jemanden kümmern => take care of something / someone", "[16/3.2] niemand => no one", "[16/3.2] verrückt => insane", "[16/3.3b] wenige => few", "[16/4.1b] echt => real", "[16/4.1b] erzählen => tell", "[16/4.1b] furchtbar => awful", "[16/4.1b] peinlich => embarrassing", "[16/4.1b] wieso => how so", "[16/4.2] aufgeregt => excited", "[16/4.2] aufregen (sich über etwas) => upset (about something)", "[16/4.2] erfreut => pleased", "[16/4.2] gelangweilt => bored"]

	link = "https://www.verbformen.de/konjugation/?w=" 
	for v in verbs_condidates:
		print(v)
		infinitive = v.split("] ")[1].split(" => ")[0].strip()
		# print(link + infinitive)
		result = requests.get(link + infinitive).text.split("\n")
		# print(result)
		# break
		for i, line in enumerate(result):
			if "<b>Präteritum</b>:" in line:
				ans = result[i+1].split(", wir")
				for a in ans[0].split(", "):
					print(a)
				break

		Partizip2 = ""
		for i, line in enumerate(result):
			if "<b>Partizip II</b>:" in line:
				Partizip2 = result[i+1]
				break
		
		flag = True
		for i, line in enumerate(result):
			if "<b>Perfekt</b>:" in line and flag:
				flag = False
				if "bin" in result[i+1]:
					print(Partizip2 + " (sein)")
				else:
					print(Partizip2 + " (haben)")
				# break
		print()

if __name__ == '__main__':
	main()

	# main2()