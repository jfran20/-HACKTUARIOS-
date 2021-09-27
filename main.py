from tika import parser 

raw = parser.from_file('PDF/BIMBO 2021-2.pdf')
print(raw['content'])