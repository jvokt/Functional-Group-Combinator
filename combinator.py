#!/usr/bin/env python

import openbabel, pybel, glob, os, subprocess

def setupLigands(group):
  dict = {}
  for file in glob.glob('ligand-groups/' + group + '/*.smi'):
    filename = os.path.splitext(os.path.basename(file))[0]
    if filename == 'H': dict[filename] = ''
    else: 
      f = open(file)
      filecontent = f.read().split()[0]
      dict[filename] = filecontent
  return dict

def insert(original, new, pos):
  return original[:pos] + new + original[pos:]

def getSMILE(base, p1, ligand1, p2, ligand2):
  p1 = int(p1)
  p2 = int(p2) 
  if p1 >= p2: return base
  ligandA = '(' + ligandDict[ligand1] + ')'
  ligandB = '(' + ligandDict[ligand2] + ')'
  sm = base
  result = base
  if p1 <= 1: sm = insert(base, ligandA, 2)
  elif p1 == 2: sm = insert(base, ligandA, 3)
  else: sm = insert(base, ligandA, 15)
  if p2 >= 6: result = insert(sm, ligandB, len(sm))
  elif p2 == 5: result = insert(sm, ligandB, len(sm)-2)
  else: result = insert(sm, ligandB, len(sm)-14)
  return result

def createXYZ(smile,molecule,dir):
  if smile != '':
    mol = pybel.readstring('smi',smile)
    mol.make3D()
    if not os.path.exists(dir):
      os.makedirs(dir)
    mol.write('xyz', dir + '/' + molecule + '.xyz',True)
  else:
    #print os.getcwd()
    f = open('jobs/6-31g/wpbeh/minimize/-1/no/1/' + molecule + '/scr/optim.xyz')
    lines = f.read().split('\n')
    xyzline = 0
    for i in range(0,len(lines)):
      if 'TeraChem' in lines[i]:
        xyzline = i - 1
    if not os.path.exists(dir):
      os.makedirs(dir)
    f = open(dir + '/' + molecule + '.xyz','w')
    #print dir + ' ' + xyzline
    for line in lines[xyzline:]:
        f.write(line + '\n')
    f.close()

def createInputFile(molecule,dir):
  input = dir.split('/')
  f = open(dir + '/' + molecule + '.in', 'w')
  f.write('chkfile\t' + molecule + '.chk\n')
  f.write('coordinates\t' + molecule + '.xyz\n')
  f.write('basis\t' + input[2] + '\n')
  f.write('method\t' + input[3] + '\n')
  f.write('run\t' + input[4] + '\n')
  f.write('charge\t' + input[5] + '\n')
  f.write('nbo\t' + input[6] + '\n')
  f.write('spinmult\t' + input[7] + '\n')
  f.write('min_coordinates\tcartesian\n')
  f.write('min_method\tbfgs\n')
  f.write('min_init_hess\tidentity\n')
  f.write('convthre\t1.0e-6\n')
  f.write('min_print\tverbose\n')
  f.write('timings\tyes\n')
  f.write('gpus\t1\n')
  f.write('end')
  f.close()

def runBash(cmd):
    subprocess.call(cmd, executable="bash", shell=True)

def runJob(molecule, dir):
  mol = molecule.replace('catechol-1-','').replace('-5','')
  f = open(dir + '/sub-' + molecule, 'w')
  f.write('#$ -S /bin/bash\n')
  f.write('#$ -N ' + mol + '\n')
  f.write('#$ -l h_rt=05:00:00\n')
  f.write('#$ -l gpus=1\n')
  f.write('#$ -l h_rss=8G\n')
  f.write('#$ -cwd\n')
  f.write('#$ -q *\n')
  f.write('#$ -pe smp 1\n')
  f.write('export OMP_NUM_THREADS=1\n')
  f.write('cd $SGE_O_WORKDIR\n')
  f.write('cp -pr $SGE_O_WORKDIR/*.xyz $SGE_O_TEMPDIR\n')
  f.write('cp -pr $SGE_O_WORKDIR/*.in $SGE_O_TEMPDIR\n')
  f.write('cd $SGE_O_TEMPDIR\n')
  f.write('$TeraChem/int ' + molecule + '.in > $SGE_O_WORKDIR/' + molecule + '.out\n')
  f.write('cp -pr $SGE_O_TEMPDIR/scr/ $SGE_O_WORKDIR/')
  f.close()
  os.chdir(dir)
  os.system('qsub sub-' + molecule + ' > data.dat')
  os.system('date +%H:%M" "%D > date.dat')
  jobid = open('data.dat').read().split()[2]
  try: 
    date = open('date.dat').read().split('\n')[0]
  except IOError:
    date = '????'
  os.chdir('/home/jvokt/ligand-combinator/')  
  jobs.write(jobid + ' ' + date + ' ' + dir + '\n')

#deprecated
def runJobs():
  dir = 'jobs/6-31g/wpbeh/minimize/'
  molecules = [ name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]
  for molecule in molecules:
    runJob(molecule, dir + molecule)
  #for root, dirs, files in os.walk(dir)
   # runJob()

inputfile = open('combinator.in').read().split('\n')
basename = inputfile[0].split()[1]
base = open('bases/' + basename + '.smi').read().split()[0]
p1 = inputfile[1].split()[1]
p2 = inputfile[2].split()[1]
ligandGroup = inputfile[3].split()[1] 
ligandDict = setupLigands(ligandGroup)
ligands = ligandDict.keys()
method = inputfile[4].split()[1]
basis = inputfile[5].split()[1]
runtype = inputfile[6].split()[1]
autorun = inputfile[7].split()[1]
charge = inputfile[8].split()[1]
nbo = inputfile[9].split()[1]
spinmult = inputfile[10].split()[1]
basedir = inputfile[11].split()[1]

#molecules = {}
jobs = open('jobs.dat','w')
#importantLigs = ['Cl']
for ligand1 in ligands:
  for ligand2 in ligands:
    #if ligand1 in importantLigs or ligand2 in importantLigs:
      #print ligand1 + ', ' + ligand2
      molecule = basename + '-' + p1 + '-' + ligand1 + '-' + p2 + '-' + ligand2
      #dir = 'jobs/' + basedir + '/' + basis + '/' + method + '/' + \
      #  runtype + '/' + charge + '/' + nbo + '/' + spinmult + '/' + molecule
      dir = 'xyzs/neutral/'
      smile = getSMILE(base, p1, ligand1, p2, ligand2)
      createXYZ(smile,molecule,dir)
      #createInputFile(molecule,dir)
      #if int(autorun) == 1: runJob(molecule, dir)

if int(autorun) == 0: runJobs()
jobs.close()
