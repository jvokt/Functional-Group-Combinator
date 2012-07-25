#!/usr/bin/env python

import os, math, subprocess

#dir = 'jobs/6-31g/wpbeh/minimize/'
dir = 'jobs/neutral/6-31gs/uwpbeh/energy/'
neutral = 'jobs/neutral/6-31gs/uwpbeh/minimize/0/full/1/'
negative = 'jobs/neutral/6-31gs/uwpbeh/energy/-1/full/2/'
positive = 'jobs/neutral/6-31gs/uwpbeh/energy/1/full/2/'
#catechol_charge_file = file(dir + 'catechol-1-H-5-H/scr/charge_mull.xls').read().split("\n")
#catechol_charge = []
#for i in range(0,8):
#  catechol_charge.append(catechol_charge_file[i].split()[2])
#length = {'CN':2, 'CH3SO2': 4, 'F': 1, 'H': 0, 'COCH3': 3, 'CHO': 2, 'C4H8COOH': 7, 'Br': 1, 'CH2OH': 4, 'COOH': 3, 'CF3': 4, 'NO2': 3}
if not os.path.exists(dir + 'calculations/'):
  os.makedirs(dir + 'calculations/')

molecules = [ name for name in os.listdir(neutral) if os.path.isdir(os.path.join(neutral, name))]
#print len(molecules)
for molecule in molecules:
  #print molecule
  #mol = molecule.replace('catechol-1-','').split('-5-')
  #lig1 = mol[0]
  #lig2 = mol[1]
  f = open(dir + 'calculations/' + molecule + '-calc','w')
  neutral_energy_file = file(neutral + molecule + '/' + molecule + '.out').read().split("\n")
  for line in neutral_energy_file:
    if 'FINAL ENERGY' in line:
      neutral_energy = line.split()[2]
  negative_energy_file = file(negative + molecule + '/' + molecule + '.out').read().split("\n")
  for line in negative_energy_file:
    if 'FINAL ENERGY' in line:
      negative_energy = line.split()[2]
  positive_energy_file = file(positive + molecule + '/' + molecule + '.out').read().split("\n")
  for line in positive_energy_file:
    if 'FINAL ENERGY' in line:
      positive_energy = line.split()[2]
  IP = float(positive_energy) - float(neutral_energy)
  EA = float(neutral_energy) - float(negative_energy)
  if EA < 0: print 'negative EA:' + molecule
  hardness = float(positive_energy) - float(negative_energy)
  f.write('Negative energy: ' + str(negative_energy) + "\n")
  f.write('Neutral energy: ' + str(neutral_energy) + "\n")
  f.write('Positive energy: ' + str(positive_energy) + "\n")
  f.write('IP: ' + str(IP) + "\n")
  f.write('EA: ' + str(EA) + "\n")
  f.write('Hardness: ' + str(hardness) + "\n")
  f.close()
