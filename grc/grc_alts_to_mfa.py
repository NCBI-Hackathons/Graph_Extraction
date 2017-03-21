#! /usr/bin/python

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

	def sort_key(self):
		return self.parent_start

def read_grc_placements(filename):
	placements = []
	f = open(filename, "r")
	for line in iter(f):
		if line[0] == '#':
			continue
		d = line.split("\t")
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
		placements.append(p)
		#print p.alt_name , p.parent_name, p.parent_start, p.parent_stop
	f.close()
	return placements

def get_parents(placements):
	parents = set()
	for p in placements:
		parents.add(p.parent_name)
	return list(parents)

# real work
class MFA(object):
	def __init__(self):
		self.rows = []
		header = MFA_Row()
		header.letter = 'H'
		header.version = '1.0'
		self.rows.append(header)

class MFA_Row(object):
	def __init__(self):
		self.letter = ''
		self.sequence_name = ''
		self.sequence_start = 0
		self.sequence_stop = 0
		self.sequence_iupac = 'unsetunsetunset'
		
		self.link_from_name= 'unset'
		self.link_to_name = 'unset'
		self.link_from_strand = '+'
		self.link_to_strand = '+'
		self.link_cigar = '0M'	
	
		self.version = ''
	
	def to_string(self):
		if self.letter == 'S':
			return self.letter + '\t' + self.sequence_name + '\t' + self.sequence_iupac
		elif self.letter == 'L':
			return self.letter+'\t'+self.link_from_name+'\t'+self.link_from_strand+'\t'+self.link_to_name+'\t'+self.link_to_strand+'\t'+self.link_cigar	
		elif self.letter == 'H':
			return self.letter + '\t' + 'VN:Z:' + self.version
		else:
			return "mfa_row::to_string error: no letter"	
	
def make_mfa_from_placements(placements, lengths):
	mfa = MFA()
	parent_name = placements[0].parent_name
	parent_seg_starts = [1]
        last_parent_stop = 0
	sort_placements = sorted(placements, key=Placement.sort_key)

	# extract the parent segment starts 
	for placement in sort_placements:
		parent_seg_starts.append(placement.parent_start)
		last_parent_stop = max(last_parent_stop, placement.parent_stop)
		#print placement.parent_start
	parent_seg_starts.append(last_parent_stop+1)
	parent_seg_starts.append(lengths[parent_name]+1)

	# make alt segment rows
	for placement in sort_placements:
		row = MFA_Row()
		row.letter = 'S'
		row.sequence_name = placement.alt_name
		row.sequence_start = 0
		row.sequence_stop = lengths[placement.alt_name]
		mfa.rows.append(row)
	
	# make parent segment rows
	parent_name_map = {}
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
		mfa.rows.append(row)
		
		parent_name_map[start] = row.sequence_name
		parent_name_map[stop] = row.sequence_name
		i += 1

	# make alt-to-parent link rows
	for placement in sort_placements:
		alt_in = MFA_Row()
		alt_in.letter = 'L'
		alt_in.link_from_name = parent_name_map[placement.parent_start-1]
		alt_in.link_from_strand = '+'
		alt_in.link_to_name = placement.alt_name
		alt_in.link_to_strand = placement.alt_orient
		mfa.rows.append(alt_in)
		
		alt_out = MFA_Row()
		alt_out.letter = 'L'
		alt_out.link_from_name = placement.alt_name
		alt_out.link_from_strand = placement.alt_orient
		alt_out.link_to_name = parent_name_map[placement.parent_stop+1]
		alt_out.link_to_strand = '+'	
		mfa.rows.append(alt_out)
	return mfa


# output 
def output_mfa(output_mfas):
	#print "H\tVN:Z:1.0"
	for mfa in output_mfas:
		for row in mfa.rows:
			print row.to_string()
	return 0

# main

lengths = read_seq_lengths('all_seq_len')
placements = read_grc_placements('all_alt_scaffold_placement.txt')
parents = get_parents(placements)

#print len(lengths) , len(placements) , len(parents)

# calculate MFA segments, links, paths, for a given parent
result_mfa = [];
for parent in parents:
	# do stuff
	if parent != 'NC_000024.10':
		continue
	curr_placements = []
	for placement in placements:
		if placement.parent_name == parent:
			curr_placements.append(placement)
	mfa = make_mfa_from_placements(curr_placements, lengths)
	result_mfa.append(mfa)
	#print parent, len(curr_placements)

output_mfa(result_mfa)

#end

