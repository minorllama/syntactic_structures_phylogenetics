def nodegenerate(es):
	degenerate = ['Siciliano_Ragusa', 'Barese', 'Reggio_Emilia', 'Greek_Salento', 'Greek_Cypriot', 'Serbo-Croatian', 'Irish', 'Even_1', 'Even_2', 'Kazakh', 'Kirghiz', 'Archi']
	return [e for e in es if not e in degenerate]

tuplize = lambda x: tuple(nodegenerate(list(sorted(x))))
splitlangs = lambda x: [e.strip()  for e in x.split(",")]

germanic = tuplize(['English', 'Dutch', 'Afrikaans', 'German', 'Danish', 'Icelandic', 'Faroese', 'Norwegian',  'Welsh'])
germanic2 = tuplize(['English', 'Dutch', 'Afrikaans', 'German', 'Danish', 'Icelandic', 'Faroese', 'Norwegian'])

romance = tuplize(['Siciliano_Mussomeli', 'Calabrese_Southern', 'Salentino', 'Calabrese_Northern', 'Campano', 'Teramano', 'Casalasco', 'Parma', 'Italian', 'Spanish', 'French', 'Portuguese', 'Romanian', 'Greek_Calabria_1', 'Greek_Calabria_2', 'Greek'])

ie = tuplize(splitlangs("Irish, Welsh, Marathi, Hindi, Pashto, Greek, Greek_Cypriot, Greek_Calabria_1, Greek_Calabria_2,Greek_Salento, Bulgarian, Serbo-Croatian, Slovenian, Polish, Russian, Faroese, Norwegian, Danish,Icelandic, German, Dutch, English, Afrikaans, French, Casalasco, Reggio_Emilia, Parma, Spanish,Portuguese, Romanian, Siciliano_Ragusa, Siciliano_Mussomeli, Salentino, Calabrese_Southern, Italian, Barese, Campano, Teramano, Calabrese_Northern"))

slavic = tuplize(splitlangs("Bulgarian, Serbo-Croatian, Slovenian, Polish, Russian"))

ia = tuplize(splitlangs("Hindi, Marathi, Pashto, Tamil, Telugu"))

ua = tuplize(splitlangs("Kazakh, Kirghiz, Turkish, Yakut, Uzbek, Evenki, Even_1, Even_2, Buryat, Mari_1, Mari_2, Udmurt_1, Udmurt_2, Hungarian, Khanty_1, Khanty_2, Estonian, Finnish"))


def langs():
	return {"germanic2" : germanic2, "germanic":germanic,   "romance" : romance, "indo-european": ie, "indo-aryan":ia, "slavic" : slavic,  "uralic-altaic": ua}
def outgroup(): 
	return {"germanic2":"Icelandic" , "germanic":"Welsh", "romance": "Greek", "indo-european":"Marathi", "indo-aryan":"Tamil", "slavic":"Russian", "uralic-altaic":"Evenki"}
