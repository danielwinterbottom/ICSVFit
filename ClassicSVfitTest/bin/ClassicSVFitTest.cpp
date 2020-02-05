#include <iostream>
#include <string>
#include <stdlib.h>
#include <stdint.h>

#include "TFile.h"
#include "TTree.h"
#include "UserCode/ICHiggsTauTau/interface/Candidate.hh"
#include "UserCode/ICHiggsTauTau/interface/Met.hh"
#include "TauAnalysis/ClassicSVfit/interface/ClassicSVfit.h"
#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"
#include "TauAnalysis/ClassicSVfit/interface/svFitHistogramAdapter.h"
#include "TSystem.h"
#include "PhysicsTools/FWLite/interface/TFileService.h"

std::pair<double,double> SplitString(std::string instring){
    std::vector<std::string> outstrings;
    std::stringstream ss(instring);
    std::string splitstring;
    while(std::getline(ss, splitstring, ',')) outstrings.push_back(splitstring); 
    return std::make_pair(std::stod(outstrings[0]),std::stod(outstrings[1]));
}


using namespace classic_svFit;

int main(int argc, char* argv[]){

  if (argc !=2 && argc != 3 && argc !=4){
    //std::cerr << "Need 1,2 or 3 args: <input> <file_prefix> (--M=<mass_constraint>)" << std::endl;
    std::cerr << "Need 1,2 or 3 args: <input> <file_prefix> (--M=<mass_constraint>)" << std::endl;
    exit(1);
  }

  std::string file_prefix = "";
  double mass_constraint = -1;
  bool constrainM = false;
  int npercall=-1;
  int offset=-1;
  if(argc==3){
    std::string arg = argv[2];
    if(arg.find("--npercall_offset=") != std::string::npos){
     std::pair<double,double> nper_offset = SplitString(arg.erase(0,18));
     npercall = (int) nper_offset.first;
     offset = (int) nper_offset.second;
    } else file_prefix = argv[2];
  }
  if(argc==4){
    file_prefix = argv[2];
    std::string arg = argv[3];
    if(arg.find("--npercall_offset=") != std::string::npos) {
      std::pair<double,double> nper_offset = SplitString(arg.erase(0,18));
      npercall = (int) nper_offset.first;
      offset = (int) nper_offset.second;
    }
  }


  //if(argc==3){
  //  std::string arg = argv[2];
  //  if(arg.find("--M=") != std::string::npos){
  //   constrainM = true;
  //   mass_constraint=std::stod(arg.erase(0,4));
  //  } else file_prefix = argv[2];
  //}
  //if(argc==4){
  //  file_prefix = argv[2];
  //  constrainM = true;
  //  std::string arg = argv[3];
  //  if(arg.find("--M=") != std::string::npos) mass_constraint=std::stod(arg.erase(0,4));
  //}

  std::string input_file = argv[1];
  std::string output_file = input_file;

  if (output_file.find("input.root") != input_file.npos) {
    std::size_t pos = output_file.find("input.root");
    output_file.replace(pos, std::string("input.root").length(), "output.root");
  } else {
    std::cerr << "The input file is not named correctly" << std::endl;
    return 1;
  }
  TFile *input = TFile::Open((file_prefix+input_file).c_str());
  if (!input) {
    std::cerr << "The input file could not be opened" << std::endl;
    return 1;
  }
  TTree *itree = dynamic_cast<TTree *>(input->Get("svfit"));
  if (!itree) {
    std::cerr << "The input tree could not be found" << std::endl;
    return 1;
  }

  unsigned mini=0;
  unsigned maxi=itree->GetEntries();

  if(npercall>-1 && offset>-1){
    mini=npercall*offset;
    maxi=npercall*(offset+1);
    maxi = maxi > itree->GetEntries() ? itree->GetEntries() : maxi;
    std::size_t pos = output_file.find("output.root"); 
    output_file.replace(pos, std::string("output.root").length(), std::to_string(offset)+"_output.root"); 
  }

  if (mini > itree->GetEntries()) return 0;


  ic::Candidate *c1 = NULL;
  ic::Candidate *c2 = NULL;
  ic::Met *met = NULL;
  unsigned event = 0;
  unsigned lumi = 0;
  unsigned run = 0;
  ULong64_t objects_hash = 0;
  unsigned mode = 0;
  int dm1 = -1;
  int dm2 = -1;
  double svfit_mass;
  double svfit_mass_err;
  double svfit_transverse_mass;
  ic::Candidate *svfit_vector = NULL;

  TH1::AddDirectory(kFALSE);

  itree->SetBranchAddress("event", &event);
  itree->SetBranchAddress("lumi", &lumi);
  itree->SetBranchAddress("run", &run);
  itree->SetBranchAddress("objects_hash", &objects_hash);
  itree->SetBranchAddress("lepton1", &c1);
  itree->SetBranchAddress("dm1", &dm1);
  itree->SetBranchAddress("lepton2", &c2);
  itree->SetBranchAddress("dm2", &dm2);
  itree->SetBranchAddress("met", &met);
  itree->SetBranchAddress("decay_mode", &mode);

  TFile *output = new TFile(output_file.c_str(),"RECREATE");
  TTree *otree = new TTree("svfit","svfit");
  otree->Branch("event", &event, "event/i");
  otree->Branch("lumi", &lumi, "lumi/i");
  otree->Branch("run", &run, "run/i");
  otree->Branch("objects_hash", &objects_hash, "objects_hash/l");
  otree->Branch("svfit_mass", &svfit_mass);
  otree->Branch("svfit_mass_err", &svfit_mass_err);
  otree->Branch("svfit_transverse_mass", &svfit_transverse_mass);
  otree->Branch("svfit_vector", &svfit_vector);

  for (unsigned i = mini; i < maxi; ++i) {
    itree->GetEntry(i);
    std::pair<ic::Candidate, std::vector<double>> result;
    
    // define MET
    double measuredMETx =  met->vector().px();
    double measuredMETy = met->vector().py();

    // define MET covariance
    TMatrixD covMET(2, 2);
    covMET(0,0) = met->xx_sig();
    covMET(1,0) = met->yx_sig();
    covMET(0,1) = met->xy_sig();
    covMET(1,1) = met->yy_sig();
    //std::cout << "event = " << event << std::endl;
    //std::cout << "MET inputs: " << std::endl;
    //std::cout << "covMET(0,0) = " << covMET(0,0) << std::endl; 
    //std::cout << "covMET(1,0) = " << covMET(1,0) << std::endl;
    //std::cout << "covMET(0,1) = " << covMET(0,1) << std::endl;
    //std::cout << "covMET(1,1) = " << covMET(1,1) << std::endl;
    //std::cout << "measuredMETx = " << measuredMETx << std::endl;
    //std::cout << "measuredMETy = " << measuredMETy << std::endl;

    double kappa = 5.;

    std::vector<MeasuredTauLepton> measuredTauLeptons;
    if (mode == 0) {
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToMuDecay, c1->pt(), c1->eta(), c1->phi(), 0.10566)); 
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToHadDecay,  c2->pt(), c2->eta(), c2->phi(), c2->M(), dm2));         
      kappa = 4.;
    } else if (mode == 1){
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToElecDecay, c1->pt(), c1->eta(), c1->phi(), 0.000511));
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToMuDecay, c2->pt(), c2->eta(), c2->phi(), 0.10566));
      kappa = 3.;
      //std::cout << "electron input:" << std::endl;
      //std::cout << "pT = " << c1->pt() << " eta = " << c1->eta() << " phi = " << c1->phi() << " mass = " << 0.000511 << std::endl;
      //std::cout << "muon input:" << std::endl;
      //std::cout << "pT = " << c2->pt() << " eta = " << c2->eta() << " phi = " << c2->phi() << " mass = " << 0.105658 << std::endl;
      //std::cout << "kappa = " << kappa << std::endl;
    } else if (mode == 2){
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToElecDecay, c1->pt(), c1->eta(), c1->phi(), 0.000511));
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToHadDecay,  c2->pt(), c2->eta(), c2->phi(), c2->M(), dm2));
      kappa = 4.;
    } else if (mode == 3){
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToHadDecay,  c1->pt(), c1->eta(), c1->phi(), c1->M(), dm1));
      measuredTauLeptons.push_back(MeasuredTauLepton(MeasuredTauLepton::kTauToHadDecay,  c2->pt(), c2->eta(), c2->phi(), c2->M(), dm2));
      kappa = 5.;
    } else{
      std::cout<<"Mode "<<mode<<" not valid"<<std::endl;
      exit(1);
    }

    int verbosity = 0;
    ClassicSVfit svFitAlgo(verbosity);
    svFitAlgo.addLogM_fixed(true, kappa);
    // add constrain on mass if option is specified
    if(constrainM) svFitAlgo.setDiTauMassConstraint(mass_constraint);
    svFitAlgo.integrate(measuredTauLeptons, measuredMETx, measuredMETy, covMET);
    bool isValidSolution = svFitAlgo.isValidSolution();

    if (isValidSolution){
      svfit_mass = static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getMass();
      svfit_mass_err = static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getMassErr();
      svfit_transverse_mass = static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getTransverseMass();
     svfit_vector->set_vector((ROOT::Math::PtEtaPhiEVector)ROOT::Math::PtEtaPhiMVector(static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getPt(), static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getEta(), static_cast<DiTauSystemHistogramAdapter*>(svFitAlgo.getHistogramAdapter())->getPhi(), svfit_mass));
    } else {
      svfit_mass = -1;
      svfit_mass_err = -1;
      svfit_transverse_mass = -1;
    }
    svfit_vector->set_id(objects_hash);
    std::cout << "Mass: " << svfit_mass << "\tVector Mass: " << svfit_vector->M() << "\tVector pT: " << svfit_vector->pt() << std::endl;
    otree->Fill();
  }
  output->Write();
  delete otree;
  output->Close();
  delete output;

  input->Close();
  delete input;
  std::cout << "Finished Processing." << std::endl;
  return 0;
}




