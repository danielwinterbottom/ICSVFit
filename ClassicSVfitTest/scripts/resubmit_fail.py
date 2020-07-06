import os
import subprocess
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--dir", dest = "dir",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--ops", dest= "ops", default='--siteblacklist=T3_KR_KNU,T2_TR_METU,T3_FR_IPNL,T2_US_Wisconsin', 
                  help="extra options to be specified when resubmitting jobs")

(options,args) = parser.parse_args()

ops = options.ops
crabdir = options.dir

def list_paths(path):
    directories = []
    for item in os.listdir(path):
      if os.path.isdir(os.path.join(path, item)):
        directories.append(item)
    return directories

def get_failed_ids(status):
  x = status.split('\n')
  y = []
  for i in x:
    if 'Warning' in i: continue
    if 'exit code' in i: continue
    if 'Jobs status:' in i: continue
    if len(i.split())>0: y.append(i.split()[0])
  return y

def chunks(l, n):
  n = max(1, n)
  y = []
  for i in range(0, len(l), n):
    j = l[i:i+n]
    y.append(j)
  return y

dirs = list_paths(crabdir)

for d in dirs:
  print '-------------------------'
  print 'resubmitting for:', d
  status = subprocess.check_output('crab status %s/%s --long | grep failed' % (crabdir,d), shell=True)
  x= get_failed_ids(status)

  if len(x)<=0: continue

  #y = chunks(x,100)
  y = chunks(x,1)

  for j in y:
    ids=','.join(j)
    cmd = 'crab resubmit -d %(crabdir)s/%(d)s --jobids=%(ids)s %(ops)s' % vars()
    os.system(cmd)


