import os
from WMCore.Configuration import Configuration


config = Configuration()

config.section_('General')
config.General.requestName = ''
# if (args.workArea != ''):
#   config.General.workArea = args.workArea

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = os.environ['CMSSW_BASE']+'/src/ICSVFit/ClassicSVfitTest/scripts/do_nothing_cfg.py'
config.JobType.scriptExe = ''
config.JobType.inputFiles = [os.environ['CMSSW_BASE']+'/src/ICSVFit/ClassicSVfitTest/scripts/FrameworkJobReport.xml', os.environ['CMSSW_BASE']+'/bin/'+os.environ['SCRAM_ARCH']+'/ClassicSVFitTest']
config.JobType.outputFiles = ['svfit_output_tar.root']
# config.JobType.maxMemoryMB = args.maxMemory

config.section_('Data')
config.Data.outputPrimaryDataset = 'SVFit'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 1
config.Data.publication = False
config.Data.outputDatasetTag = ''

config.section_('User')

config.section_('Site')
#config.Site.blacklist = ['T3_IT_Bologna']
config.Site.blacklist   = ['T3_KR_KNU','T2_TR_METU','T3_FR_IPNL']
config.Site.storageSite = 'T2_UK_London_IC'
