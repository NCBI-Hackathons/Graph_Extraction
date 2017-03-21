#! /usr/bin/python

import pprint
import urllib
import Bio

# file readers

def read_seq_lengths(filename):
	length_dict = {}
	f = open(filename, "r")
	for line in iter(f):
		d = line.split()
		name = d[0]
		length = int(d[1])
		length_dict[name] = length
		#print name , length, len(length_dict)
	f.close()
	return length_dict


class Placement(object):
	def __init__(self):
		self.alt_name = ''
		self.alt_orient = ''
		self.alt_asm = ''
		self.parent_name = ''
		self.parent_asm = ''
		self.parent_start = 0
		self.parent_stop = 0
		self.alt_tails = [0,0]
	def __repr__(self):
        	from pprint import pformat
        	return pformat(vars(self))

	def sort_key(self):
		return self.parent_start

def read_grc_placements(filename):
	placements = []
	f = open(filename, "r")
	for line in iter(f):
		if line[0] == '#':
			continue
		d = line.split("\t")
		if d[1] != 'Primary Assembly':
			continue
		p = Placement()
		p.alt_name = d[3]
		p.alt_asm = d[0]
		p.alt_orient = d[8]
		p.parent_name = d[6]
		p.parent_asm = d[1]
		p.parent_start = int(d[11])
		p.parent_stop = int(d[12])
		p.alt_tails[0] = int(d[13])
		p.alt_tails[1] = int(d[14])
		
		if p.alt_orient == 'b':
			p.alt_orient = '+'
		if p.alt_orient == '-':
			t = p.alt_tails[0]
			p.alt_tails[0] = p.alt_tails[1]
			p.alt_tails[1] = t

		placements.append(p)
		#print p.alt_name , p.parent_name, p.parent_start, p.parent_stop
	f.close()
	return placements

class Region(object):
	cols = [
		'region_name',
		'chromosome',
		'chr_start',
		'chr_stop',
		'scaffold_role',
		'scaffold_GB_acc',
		'scaffold_RS_acc',
		'assembly_unit'
	];
	def __init__(self):
		self.region_name = ''
		self.chromosome = ''
		self.chr_start = 0
		self.chr_stop = 0
		self.scaffold_role = ''
		self.scaffold_GB_acc = ''
		self.scaffold_RS_acc = ''
		self.assembly_unit = ''
	def __repr__(self):
        	from pprint import pformat
        	return pformat(vars(self))
	def sort_key(self):
		return self.region_name

def read_grc_regions(filename):
	regions = []
	f = open(filename, "r")
	num_cols = len(Region.cols)
	for line in iter(f):
		if line[0] == '#':
			continue
		d = line.split("\t")
		r = Region()
		for i in range(0, num_cols):
		    setattr(r, Region.cols[i], d[i])
		regions.append(r)
		#print p.alt_name , p.parent_name, p.parent_start, p.parent_stop
	f.close()
	return regions

def get_parents(placements):
	parents = set()
	for p in placements:
		parents.add(p.parent_name)
	return list(parents)

# real work
mfa_gap_counter = 1
class MFA(object):
	def __init__(self):
		self.rows = []
		header = MFA_Row()
		header.letter = 'H'
		header.version = '1.0'
		self.rows.append(header)
	def add_comment(self, comment):
		row = MFA_Row()
		row.letter = '#'
		row.comment = comment
		self.rows.append(row)
	def make_gap(self):
		global mfa_gap_counter
		gap_row = MFA_Row()
		gap_row.letter = 'S'
		gap_row.sequence_name = 'synthetic_gap__' + str(mfa_gap_counter)
		gap_row.sequence_iupac = 'NNNNNNNNNN'
		gap_row.sequence_length = 10
		self.rows.append(gap_row)
		mfa_gap_counter += 1
		return gap_row.sequence_name
	
class MFA_Row(object):
	def __init__(self):
		self.letter = ''
		self.sequence_name = ''
		self.sequence_start = 0
		self.sequence_stop = 0
		self.sequence_iupac = '*' # unset
		self.sequence_length = 0	
	
		self.link_from_name= '*' # unset
		self.link_to_name = '*' # unset
		self.link_from_strand = '+'
		self.link_to_strand = '+'
		self.link_cigar = '0M'	
	
		self.version = ''
		self.comment = ''
		
	def to_string(self):
		if self.letter == 'S':
			return self.letter + '\t' + self.sequence_name + '\t' + self.sequence_iupac + '\t' + 'LN:i:' + str(self.sequence_length)
		elif self.letter == 'L':
			return self.letter+'\t'+self.link_from_name+'\t'+self.link_from_strand+'\t'+self.link_to_name+'\t'+self.link_to_strand+'\t'+self.link_cigar	
		elif self.letter == 'H':
			return self.letter + '\t' + 'VN:Z:' + self.version
		elif self.letter == '#':
			return self.letter + self.comment
		else:
			return "mfa_row::to_string error: no letter"	




def make_mfa_from_placements(placements, lengths, fasta_sequences):
	mfa = MFA()
	parent_name = placements[0].parent_name
	parent_seg_starts = [1]
        last_parent_stop = 0
	sort_placements = sorted(placements, key=Placement.sort_key)

	mfa.add_comment(parent_name)
	
	gap_counter = 1
	tail_count = 0	
	for placement in sort_placements:
		tail_count += placement.alt_tails[0]
		tail_count += placement.alt_tails[1]

	# extract the parent segment starts 
	for placement in sort_placements:
		parent_seg_starts.append(placement.parent_start)
		parent_seg_starts.append(placement.parent_stop+1)
		last_parent_stop = max(last_parent_stop, placement.parent_stop)
		#print placement.parent_start
	parent_seg_starts.append(last_parent_stop+1)
	parent_seg_starts.append(lengths[parent_name]+1)
	parent_seg_starts = list(set(parent_seg_starts))
	parent_seg_starts.sort()

	# make alt segment rows
	for placement in sort_placements:
		row = MFA_Row()
		row.letter = 'S'
		row.sequence_name = placement.alt_name
		row.sequence_start = 0
		row.sequence_stop = lengths[placement.alt_name] - 1
		row.sequence_length = lengths[placement.alt_name]
                row.sequence_iupac = fasta_sequences[parent_name].seq[row.sequence_start:row.sequence_stop]
		# TODO
		mfa.rows.append(row)
	
	# make parent segment rows
	parent_name_map = {}
	parent_names = []
	i = 0
	for start in parent_seg_starts:
		if i+1 == len(parent_seg_starts):
			break
		stop = parent_seg_starts[i+1] - 1
		row = MFA_Row()
		row.letter = 'S'
		row.sequence_name = parent_name + '__' + str(i+1) + '__'+str(start)+'_'+str(stop)
		row.sequence_start = start
		row.sequence_stop = stop
		row.sequence_length = (stop-start)+1
		mfa.rows.append(row)
                row.sequence_iupac = fasta_sequences[parent_name].seq[row.sequence_start:row.sequence_stop]
		# TODO
		parent_name_map[start] = row.sequence_name
		parent_name_map[stop] = row.sequence_name
		parent_names.append(row.sequence_name)
		i += 1

	#pprint.pprint(parent_name_map)
	#pprint.pprint(parent_names)

	# make parent-to-parent link rows
	i = 0
	for first in parent_names:
		if i+1 == len(parent_names):
			break
		second = parent_names[i+1]
		row = MFA_Row()
		row.letter = 'L'
		row.link_from_name = first
		row.link_to_name = second
		mfa.rows.append(row)
		i += 1
	
	# make alt-to-parent link rows
	for placement in sort_placements:
		#pprint.pprint(placement)

		if placement.alt_tails[0] == 0:
			alt_in = MFA_Row()
			alt_in.letter = 'L'
			alt_in.link_from_name = parent_name_map[placement.parent_start-1]
			alt_in.link_from_strand = '+'
			alt_in.link_to_name = placement.alt_name
			alt_in.link_to_strand = placement.alt_orient
			mfa.rows.append(alt_in)
		elif placement.alt_tails[0] > 0:
			gap_name = mfa.make_gap()
			gap_in = MFA_Row()
			alt_in = MFA_Row()
			gap_in.letter = 'L'
			gap_in.link_from_name = parent_name_map[placement.parent_start-1]
			gap_in.link_to_name = gap_name
			alt_in.letter = 'L'
			alt_in.link_from_name = gap_name
			alt_in.link_to_name = placement.alt_name
			alt_in.link_to_strand = placement.alt_orient
			mfa.rows.append(gap_in)
			mfa.rows.append(alt_in)
		#end

		if placement.alt_tails[1] == 0:	
			alt_out = MFA_Row()
			alt_out.letter = 'L'
			alt_out.link_from_name = placement.alt_name
			alt_out.link_from_strand = placement.alt_orient
			alt_out.link_to_name = parent_name_map[placement.parent_stop+1]
			alt_out.link_to_strand = '+'	
			mfa.rows.append(alt_out)
		elif placement.alt_tails[1] > 0:
			gap_name = mfa.make_gap()
			alt_out = MFA_Row()
			gap_out = MFA_Row()
			alt_out.letter = 'L'
			alt_out.link_from_name = placement.alt_name
			alt_out.link_from_strand = placement.alt_orient
			alt_out.link_to_name = gap_name
			gap_out.letter = 'L'
			gap_out.link_from_name = gap_name
			gap_out.link_to_name = parent_name_map[placement.parent_stop+1]
			mfa.rows.append(alt_out)
			mfa.rows.append(gap_out)
		#end
	return mfa


# output 
def output_mfa(output_mfas):
	#print "H\tVN:Z:1.0"
	for mfa in output_mfas:
		for row in mfa.rows:
			print row.to_string()
	return 0

# main

baseurl = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.36_GRCh38.p10/'
alt_scaff_pl_url = baseurl + 'GCF_000001405.36_GRCh38.p10_assembly_structure/all_alt_scaffold_placement.txt'
assm_regions_url = baseurl + 'GCF_000001405.36_GRCh38.p10_assembly_regions.txt'
alt_scaff = urllib.urlretrieve(alt_scaff_pl_url)
regions = urllib.urlretrieve(assm_regions_url)

lengths = read_seq_lengths('all_seq_len')
placements = read_grc_placements(alt_scaff[0])
regions = read_grc_regions(regions[0])
parents = get_parents(placements)

#print len(lengths) , len(placements) , len(parents)

fasta_file_name = '/home/ubuntu/grc_data/GCF_000001405.36_GRCh38.p10_genomic.fna'
fasta_sequences = {}
from Bio import SeqIO
for seq_record in SeqIO.parse(fasta_file_name, "fasta"):
	fasta_sequences[seq_record.id] = seq_record	
	#print(seq_record.id)
   	#print(repr(seq_record.seq))
   	#print(len(seq_record))

# calculate MFA segments, links, paths, for a given parent
result_mfa = [];
for parent in parents:
	# do stuff
	#if parent != 'NC_000024.10':
	#	continue
	curr_placements = []
	for placement in placements:
		if placement.parent_name == parent:
			curr_placements.append(placement)
	mfa = make_mfa_from_placements(curr_placements, lengths, fasta_sequences)
	result_mfa.append(mfa)
	#print parent, len(curr_placements)

output_mfa(result_mfa)

#end

