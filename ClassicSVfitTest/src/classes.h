#include <vector>
#include <map>
#include <utility>
#include <string>
#include "ICSVFit/ClassicSVfitTest/interface/Candidate.hh"
#include "ICSVFit/ClassicSVfitTest/interface/Met.hh"

namespace { struct dictionary {
  ic::Candidate dummy1;
  std::vector<ic::Candidate> dummy2;
  ic::Met dummy3;
  ic::Met::BasicMet dummy4;
  std::map<std::size_t, ic::Met::BasicMet> dummy5;
  std::vector<ic::Met> dummy6;
  std::map<unsigned long, std::string> dummy7;
};
}

