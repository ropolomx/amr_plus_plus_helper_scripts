from Bio import SeqIO

megabio_accessions = open('megabio_accessions.txt').read().splitlines()

megabio_nt = [rec for rec in SeqIO.parse('megabio_database_cds.fasta', 'fasta')]

matches = []

for m in megabio_accessions:
    for n in megabio_nt:
        for m in n.id:
            matches.append(n)


