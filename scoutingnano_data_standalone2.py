# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 -s NANO:@Scout --process NANO --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --era Run3_2024 --conditions 150X_mcRun3_2024_realistic_v2 --python_file scoutingnano_mc_standalone2.py -n 100 --fileout scouting_nano_MC.root --filein file:0034afa6-0d8d-4409-8154-afda2a1d7d4b.root
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_2024_cff import Run3_2024
from Configuration.ProcessModifiers.unifiedparticleTransformerAK4SonicTriton_cff import unifiedparticleTransformerAK4SonicTriton

#process = cms.Process('NANO',Run3_2024,unifiedparticleTransformerAK4SonicTriton)
process = cms.Process('NANO',Run3_2024)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.custom_run3scouting_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

#process.MessageLogger.cerr.threshold = 'ERROR'

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2024D/ScoutingPFRun3/HLTSCOUT/v1/000/380/945/00000/20069f13-2547-4f76-bdcb-298284079342.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('scouting_nano_data.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_v8', '')

# SONIC/Triton: point the client at the tritonserver instance started via singularity
# (see RecoBTag/CombinedScouting/data/models/README.md for the model repository it serves).
#process.load('HeterogeneousCore.SonicTriton.TritonService_cff')
#process.TritonService.verbose = True
#process.TritonService.servers.append(
#    cms.PSet(
#        name = cms.untracked.string("default"),
#        address = cms.untracked.string("localhost"),
#        port = cms.untracked.uint32(8001),
#    )
#)
# these categories are LogInfo/LogWarning by default and get dropped by MessageLogger's
# default per-category limit unless explicitly given one here -- without this, TritonService's
# server-discovery messages (and any MissingModel/connection failures) are silently swallowed.
for _cat in ['TritonDiscovery', 'TritonService', 'TritonFailure', 'PreferredServer', 'MissingModel',
             'TritonClient', 'UnifiedParticleTransformerAK4SonicJetTagsScoutingV2Producer']:
    setattr(process.MessageLogger.cerr, _cat, cms.untracked.PSet(limit = cms.untracked.int32(10000000)))


process.scoutingFatJetFilterCands = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("scoutingFatPFJetRecluster"),
    minNumber = cms.uint32(1),
    # jets already have pt > 170 from clustering, so no extra pt cut needed
)

process.fatJetFilter_step = cms.Path(
    process.scoutingNanoSequence + process.scoutingFatJetFilterCands
)

process.dstJetHTFilter = cms.EDFilter("TriggerResultsFilter",
    # The TriggerResults product written by the HLT process
    triggerConditions = cms.vstring(
            'DST_PFScouting_JetHT_v*',
            'DST_PFScouting_SingleMuon_v*',
    ),
    hltResults    = cms.InputTag('TriggerResults', '', 'HLT'),
    l1tResults    = cms.InputTag(''),          # not using L1 here
    throw         = cms.bool(False),           # don't crash if path not in menu
    l1tIgnoreMaskAndPrescale = cms.bool(False),
    daqPartitions = cms.uint32(1),
)

process.eventFilter_step = cms.Path(
    process.dstJetHTFilter
    + process.scoutingNanoSequence
    + process.scoutingFatJetFilterCands
)

process.NANOAODoutput.SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('eventFilter_step')
)


# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.scoutingNanoSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)

process.schedule = cms.Schedule(
    process.eventFilter_step,        
    #process.fatJetFilter_step,
    process.endjob_step,
    process.NANOAODoutput_step,
)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.custom_run3scouting_cff
from PhysicsTools.NanoAOD.custom_run3scouting_cff import customiseScoutingNano 

#call to customisation function customiseScoutingNano imported from PhysicsTools.NanoAOD.custom_run3scouting_cff
process = customiseScoutingNano(process)

from PhysicsTools.PatFromScouting.scoutingToMiniAODDerivedCollections_cff import customiseScoutingNanoDerived
process = customiseScoutingNanoDerived(process, "NANO")
# End of customisation functions


# Customisation from command line

#process.source.delayReadingEventProducts = cms.untracked.bool(False)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

