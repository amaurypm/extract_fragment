#!/usr/bin/env python3
## Extract Rosetta fragments from PDB, using pymol as a library.
##
## You need to have pymol insttaled and be able to import it.
## It requires a rosetta fragment file with the corresponding PDB codes, chain names
## and residue ids (residue names are used also, for consistency check).
## It works for only ONE fragment per PDB file. If have more than one (that is weird)
## it will run, but the oupput won't be the desired for the affected fragments.
##

## Amaury Pupo Merino
## amaury.pupo@gmail.com
##
## This script is released under GPL v3.
##

## Importing modules
import argparse
import sys
from pymol import cmd
import os
import tempfile
from Bio import SeqIO

# Functions
def get_frag_info(filename):
    pdb_dict = {}
    fragment_dict = {}
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                fields = line.split()
                if len(fields) == 11:
                    pdb_id = fields[0].strip()
                    chain_id = fields[1].strip()
                    try:
                        resi = int(fields[2])
                    except:
                        sys.stderr.write("WARNING: In line {} from file {} the value {} is not a proper residue id.\nIgnoring the whole line.\n".format(line, filename, fields[2]))
                        continue
                    resn = fields[3].strip()

                    if pdb_id not in pdb_dict:
                        pdb_dict[pdb_id] = {}
                        pdb_dict[pdb_id]['chain_id'] = chain_id
                        pdb_dict[pdb_id]['resi1'] = pdb_dict[pdb_id]['resi2'] = resi
                        pdb_dict[pdb_id]['seq'] = resn
                    else:
                        if chain_id != pdb_dict[pdb_id]['chain_id']:
                            sys.stderr.write("WARNING: More than one chain indicated for pdb {}: {} and {}\n.Ignoring line {}\n".format(pdb_id, pdb_dict[pdb_id]['chain_id'], chain_id, line))
                            continue
                        if resi < pdb_dict[pdb_id]['resi1']:
                            pdb_dict[pdb_id]['resi1'] = resi

                        elif resi > pdb_dict[pdb_id]['resi2']:
                            pdb_dict[pdb_id]['resi2'] = resi

                        pdb_dict[pdb_id]['seq'] += resn

    for n,pdb_id in enumerate(pdb_dict):
        frag_name = filename + ".frag{:02d}".format(n+1)
        fragment_dict[frag_name] = (pdb_id, pdb_dict[pdb_id])

    return fragment_dict

def write_pdb(frag_name, frag_val):
    cmd.reinitialize()
    out_filename = frag_name + ".pdb"
    pdb_id = frag_val[0]
    chain_id = frag_val[1]['chain_id']
    resi1 = frag_val[1]['resi1']
    resi2 = frag_val[1]['resi2']
    seq = frag_val[1]['seq']

    cmd.fetch(pdb_id, 'all_prot', async_=0, path = "/tmp", type="pdb")
    cmd.select("fragment", "chain {} and resi {:d}-{:d}".format(chain_id, resi1, resi2))

    #Checking sequences:
    with tempfile.TemporaryFile('w+') as tmp_file:
        tmp_file.write(pymol.cmd.get_fastastr("fragment"))
        tmp_file.seek(0)
        for seq_record in SeqIO.parse(tmp_file, "fasta"):
            if seq_record.seq:
                if seq_record.seq != seq:
                    sys.stderr.write("WARNING: Sequence from PDB ({}) does not correspond to the fragment sequence ({})\nIgnoring this fragment ({} {} from {:d} to {:d})\n".format(seq_record.seq, seq, pdb_id, chain_id, resi1, resi2))
                    return


    cmd.save(out_filename, "fragment")

## Main
def main():
    """Main function.
    """
    parser=argparse.ArgumentParser(description="Extract Rosetta fragments from PDB, using pymol as a library.")
    parser.add_argument('fragment_file', nargs='+', help='Fragment file from Rosetta. The filename is usually in the form seq_name.N.nmers, where seq_name is the name of your sequences, N the number of selected fragments and n the length of the fragments/')
    parser.add_argument('-v', '--version', action='version', version='0.1.0', help="Show program's version number and exit.")

    args=parser.parse_args()

    fragment_dict = {}

    for filename in args.fragment_file:
        fragment_dict = get_frag_info(filename)

        if fragment_dict:
            for frag_name, frag_val in fragment_dict.items():
                write_pdb(frag_name, frag_val)
            

## Running the script
if __name__ == "__main__":
    main()

