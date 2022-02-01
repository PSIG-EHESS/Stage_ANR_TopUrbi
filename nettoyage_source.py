import re, sys, os
#Import des modules à utiliser : 're' pour les expressions régulières et 'sys' pour la communication avec le terminal

#faire des dico pour tracer les index, les pages 
index_title = []
page_nb = []
entry_dic = []

for root, dirs, files in os.walk(sys.argv[1]):
	for filename in files:
		file_in = open (sys.argv[1] + filename, mode='r', encoding='utf-8')
		file_out = open (sys.argv[2].strip() + "/Norm" + filename, mode='w', encoding='utf-8')
		context_line = False
		str1 = []
		context =  []
		#identifier une entrée du dictionnaire
		entry_match = re.compile(r" [A-Z]+(\s|\.|,|:)+[A-Z][a-z]+")
		index_match = re.compile(' [A-Z]{2} \n') 
		for line in file_in:
			if line.startswith("##") or line == " \n":
				context_line = True
				#imprimer page précedente
				print("P:"+' '.join(str1).replace("  ", " ").replace("- ", ""))
				file_out.write(' '.join(str1).replace("  ", " ").replace("- ", "").replace(" ,", ","))
				file_out.write("\n")
				str1 = []
				if line.startswith("##"):
					print("PAGE:"+line)
					file_out.write("PAGE:"+line)
					file_out.write("\n")
					page_nb.append(line)
			else:
				#print("texte")
				context_line = False
				if index_match.match(line):
					print("INDEX:"+line)
					file_out.write("INDEX:"+line)
					file_out.write("\n")
					index_title.append(line)
				
			if not context_line:
				#print("joint")
				str1.append(line.lstrip().rstrip("\n").lstrip("\ufeff").strip("|"))
		
		print("pages:")
		print(page_nb)
		
		print("index:")
		print(index_title)
		
		file_in.close()
		file_out.close()
