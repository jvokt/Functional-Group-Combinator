#!/usr/bin/env python

import os, math, subprocess

#dir = 'jobs/6-31g/wpbeh/minimize/'
#dir = 'jobs/anion/6-31g/wpbeh/minimize/-1/no/1/'
dir = 'jobs/methylated/6-31gs/wpbeh/minimize/0/no/1/'
#dir = 'jobs/methylated/6-31gs/wpbeh/energy/0/no/1/'
#dir = open('jobs.dat').read().split()[3].split('catechol')[0]
catechol_charge_file = file(dir + 'catecholOmethyl-1-H-5-H/scr/charge_mull.xls').read().split("\n")
catechol_charge = []
for i in range(0,8):
  catechol_charge.append(catechol_charge_file[i].split()[2])
length = {'CN':2, 'CH3SO2': 4, 'F': 1, 'Cl': 1, 'H': 0, 'COCH3': 3, 'CHO': 2, 'C4H8COOH': 7, 'Br': 1, 'CH2OH': 4, 'COOH': 3, 'CF3': 4, 'NO2': 3}
if not os.path.exists(dir + 'charge-diffs/'):
  os.makedirs(dir + 'charge-diffs/')

molecules = [ name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)) and name != 'charge-diffs']
print len(molecules)
for molecule in molecules:
  mol = molecule.replace('catecholOmethyl-1-','').split('-5-')
  lig1 = mol[0]
  lig2 = mol[1]
  print molecule + ': ' + '(' + lig1 + ',' + lig2 + ')'
  f = open(dir + 'charge-diffs/' + molecule + '-charge-diff','w')
  try:
    mol_charge_file = file(dir + molecule + '/scr/charge_mull.xls').read().split("\n")
  except IOError:
    print 'scr charge file not found'
    mol_charge_file = file(dir + 'catecholOmethyl-1-H-5-H/scr/charge_mull.xls').read().split("\n")
    lig1 = 'H'
    lig2 = 'H'
  index = [0, length[lig1] + 1]
  for i in range(2,7):
    index.append(index[i-1] + 1)
  index.append(index[6] + 1 + length[lig2])
  mol_charge = []
  for i in range(0,8):
    x = index[i]
    mol_charge.append(mol_charge_file[x].split()[2])
  atoms = ['C1','C2','C3','O3','C4','O4','C5','C6']
  for i in range(0,8):
    diff = float(mol_charge[i]) - float(catechol_charge[i])
    f.write(atoms[i] + " " + str(diff) + "\n")
  f.close()
