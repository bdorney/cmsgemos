#ifndef gem_readout_GEMDataParker_h
#define gem_readout_GEMDataParker_h

//#include "gem/readout/GEMDataParker.h"
//#include "gem/readout/GEMslotContents.h"
#include "gem/readout/GEMDataAMCformat.h"

#include "xdata/String.h"
#include <string>

#include "gem/utils/GEMLogging.h"

namespace gem {
  namespace hw {
    namespace glib {
      class HwGLIB;
    }   
  }
  namespace readout {
    struct GEMDataAMCformat;
  }
  namespace readout {
    class GEMDataParker
    {
    public:
      GEMDataParker        (gem::hw::glib::HwGLIB& glibDevice, 
                            std::string const& outFileName, 
                            std::string const& errFileName, 
                            std::string const& outputType
                           );
      ~GEMDataParker       () {};

      int* dumpData        ( uint8_t const& mask );
      void dumpDataToDisk  ( uint8_t const& link );
      int  getGLIBData     ( uint8_t const& link );

      void GEMfillHeaders  ( uint16_t const& BC,
                             gem::readout::GEMDataAMCformat::GEMData& gem,
                             gem::readout::GEMDataAMCformat::GEBData& geb 
                           );
      bool VFATfillData    ( int const& islot,
                             gem::readout::GEMDataAMCformat::GEBData& geb
                           );
      void GEMfillTrailers ( gem::readout::GEMDataAMCformat::GEMData& gem,
                             gem::readout::GEMDataAMCformat::GEBData& geb
                           );
      void writeGEMevent   ( gem::readout::GEMDataAMCformat::GEMData& gem,
                             gem::readout::GEMDataAMCformat::GEBData& geb,
                             gem::readout::GEMDataAMCformat::VFATData& vfat
                           );
    private:

      log4cplus::Logger gemLogger_;
      gem::hw::glib::HwGLIB* glibDevice_;
      std::string outFileName_;
      std::string errFileName_;
      std::string outputType_;

      /*
       * Counter all in one
       *   [0] VFAT's Blocks Counter
       *   [1] Events Counter
       *   [2] VFATs counter per last event
       */
      int counter_[3];

      // VFAT's Blocks Counter     
      int vfat_;

      // Events Counter     
      int event_;
         
      // VFATs counter per event
      int sumVFAT_;

    };
  }
}
#endif
