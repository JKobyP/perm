all:
	./src/perm.py -p hippie_current.txt -k -f uniprot-human.tab -d -o diseases/

kinase:
	./src/perm.py -p hippie_current.txt -k -f uniprot-human.tab

disease:
	./src/perm.py -p hippie_current.txt -d -o diseases/
