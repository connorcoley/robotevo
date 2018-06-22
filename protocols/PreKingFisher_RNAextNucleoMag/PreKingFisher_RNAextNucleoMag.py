# Copyright (C) 2018-2018, Ariel Vina Rodriguez ( Ariel.VinaRodriguez@fli.de , arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2018-2018

from EvoScriPy.protocol_steps import *
import EvoScriPy.Instructions as Itr
import EvoScriPy.Labware as Lab

__author__ = 'Ariel'


class PreKingFisher_RNAextNucleoMag(Protocol):
    """Implementation of the protocol for RNA extraction using the NucleoMag® VET kit from MACHEREY-NAGEL.
    """

    name = "PreKingFisher for RNA extraction with the NucleoMag MN_Vet kit"
    versions = {'none'    : not_implemented}

    class Parameter (Protocol.Parameter):

        def __init__(self, GUI = None):

            self.NumOfSamples = 96
            Protocol.Parameter.__init__(self, GUI=GUI,
                                        worktable_template_filename = '../EvoScripts/wt_templates/preFisher_RNAext.ewt',
                                        output_filename='../current/preFisher_RNAext'
                                        )

    def __init__(self, parameters =  None):

        self.NumOfSamples = parameters.NumOfSamples
        Protocol.__init__(self,
                          4,
                          parameters or PreKingFisher_RNAextNucleoMag.Parameter())

    def set_defaults(self):
        print('set_defaults in preFisher_RNAext')
        print('Init init_RNAextraction preFisher ')

        Rtv.NumOfSamples = self.NumOfSamples  # ??

        wt = self.worktable

        # todo decide where to put the default labware: in robot or worktable object or the global Lab

        self.WashCleanerS   = wt.getLabware(Lab.CleanerSWS,    "")
        self.WashWaste      = wt.getLabware(Lab.WasteWS,       "")
        self.WashCleanerL   = wt.getLabware(Lab.CleanerLWS,    "")
        self.DiTiWaste      = wt.getLabware(Lab.DiTi_Waste,    "")

        # self.BioWaste = wt.getLabware(Lab.Trough_100ml, "6-Waste")
        Lab.def_WashWaste   = self.WashWaste
        Lab.def_WashCleaner = self.WashCleanerS
        Lab.def_DiTiWaste   = self.DiTiWaste
        Lab.def_DiTi        = Lab.DiTi_1000ul   # todo revise


    def Run(self):
        self.initialize()                       #  set_defaults ??
        NumOfSamples = self.NumOfSamples
        wt           = self.worktable

        Itr.comment('Extracting RNA from {:s} samples with the MN-Vet kit'.format(str(NumOfSamples))).exec()


        #  Get Labwares (Cuvette, eppys, etc.) from the work table

        ElutBuf     = wt.getLabware(Lab.Trough_100ml,   "1-VEL-ElutionBuffer"   )
        LysBuf      = wt.getLabware(Lab.Trough_100ml,   "2-Vl Lysis Buffer"     )
        BindBuf     = wt.getLabware(Lab.Trough_100ml,   "3-VEB Binding Buffer"  )

        DiTi1000_1  = wt.getLabware(Lab.DiTi_1000ul,    "1000-1")
        DiTi1000_2  = wt.getLabware(Lab.DiTi_1000ul,    "1000-2")
        DiTi1000_3  = wt.getLabware(Lab.DiTi_1000ul,    "1000-3")

        Reactives   = wt.getLabware(Lab.GreinRack16_2mL,"Reactives" )
        Plate_lysis = wt.getLabware(Lab.MP96deepwell,   "Plate_VEW1"    )  # Plate 12 x 8 ?
        Plate_VEW1  = wt.getLabware(Lab.MP96deepwell,   "Plate_VEW1"    )  # Plate 12 x 8 ?
        Plate_VEW2  = wt.getLabware(Lab.MP96deepwell,   "Plate_VEW2"    )  # Plate 12 x 8 ?
        Plate_EtOH  = wt.getLabware(Lab.MP96deepwell,   "Plate_EtOH"    )  # Plate 12 x 8 ?
        Plate_Eluat = wt.getLabware(Lab.MP96deepwell,   "Plate_EtOH"    )  # Plate 12 x 8 ? MP96well !!
        Samples     = wt.getLabware(Lab.EppRack6x16_2mL,"Proben"        )  # 6x16 = 12 x 8 ?


        #  Set the initial position of the tips

        Itr.set_DITI_Counter2(DiTi1000_1, posInRack=self.parameters.firstTip).exec()

        # Set volumen / sample

        SampleVolume        = 200.0
        LysisBufferVolume   = 180.0       # VL1
        IC2Volume           =   5.0       # ? 4
        BindingBufferVolume = 600.0
        B_BeadsVolume       =  20.0
        VEW1Volume          = 600.0
        VEW2Volume          = 600.0
        EtOH80pVolume       = 600.0
        ProtKVolume         =  20.0
        cRNAVolume          =   4.0
        IC_MS2Volume        =  20.0
        ElutionBufferVolume = 100.0


        # Liquid classes used for pippetting. Others liquidClass names are defined in "protocol_steps.py"

        SampleLiqClass = "Serum Asp"  # = TissueHomLiqClass   # SerumLiqClass="Serum Asp preMix3"


        all_samples = range(Rtv.NumOfSamples)
        maxTips     = min  (Rbt.nTips, Rtv.NumOfSamples)
        maxMask     = Rbt.tipsMask[maxTips]


        # Define the reactives in each labware (Cuvette, eppys, etc.)

        LysisBuffer     = Rtv.Reactive("VL - Lysis Buffer "              ,
                                       LysBuf,    volpersample=LysisBufferVolume ,defLiqClass=B_liquidClass)
        IC2             = Rtv.Reactive("IC2 - synthetic RNA "              ,
                                       Reactives, pos=11, volpersample=  IC2Volume ,defLiqClass=W_liquidClass)
        VEB             = Rtv.Reactive("VEB - Binding Buffer "           ,
                                       BindBuf,   volpersample=BindingBufferVolume ,defLiqClass=B_liquidClass)
        B_Beads         = Rtv.Reactive("B - Beads " , Reactives, initial_vol=1200,
                                         pos=1, volpersample= B_BeadsVolume , replicas=2, defLiqClass=Beads_LC_2)

        VEW1            = Rtv.Reactive("VEW1 - Wash Buffer "              ,
                                         wt.getLabware(Lab.Trough_100ml,  "4-VEW1 Wash Buffe"),
                                         volpersample=VEW1Volume    , defLiqClass=B_liquidClass)
        VEW2            = Rtv.Reactive("VEW2 - WashBuffer "               ,
                                         wt.getLabware(Lab.Trough_100ml,  "5-VEW2-WashBuffer" ),
                                         volpersample=VEW2Volume    , defLiqClass=B_liquidClass)
        EtOH80p         = Rtv.Reactive("Ethanol 80% "                     ,
                                         wt.getLabware(Lab.Trough_100ml,  "7-EtOH80p"     ),
                                         volpersample=EtOH80pVolume , defLiqClass=B_liquidClass)
        ElutionBuffer   = Rtv.Reactive("Elution Buffer "                  ,
                                       ElutBuf,     volpersample=ElutionBufferVolume , defLiqClass="Eluat")

        ProtK           = Rtv.Reactive("Proteinase K "                    ,
                                       Reactives, pos=16, volpersample= ProtKVolume , defLiqClass=Small_vol_disp)
        cRNA            = Rtv.Reactive("Carrier RNA "                     ,
                                       Reactives, pos=15, volpersample=  cRNAVolume , defLiqClass=Small_vol_disp)
        IC_MS2          = Rtv.Reactive("IC MS2 phage culture ",
                                       Reactives, pos=14, volpersample= IC_MS2Volume , defLiqClass=Small_vol_disp)
        pK_cRNA_MS2     = Rtv.preMix  ("ProtK+cRNA+IC-MS2 mix "        ,
                                       Reactives, pos=12,   components=[ ProtK, cRNA, IC2 ]
                                         ,defLiqClass=W_liquidClass, replicas=2)
        Waste           = Rtv.Reactive("Waste "  , self.WashWaste )

        # Show the CheckList GUI to the user for posible small changes

        self.CheckList()

        Itr.wash_tips(wasteVol=30, FastWash=True).exec()

        # Define samples and the place for temporal reactions
        for s in all_samples:
            Rtv.Reactive("probe_{:02d}".format(s + 1), Samples, single_use=SampleVolume,
                         pos=s + 1, defLiqClass=SampleLiqClass, excess=0)
            Rtv.Reactive("lysis_{:02d}".format(s + 1), Plate_lysis, initial_vol=0.0, pos=s + 1,
                         excess=0)  # todo revise order !!!

            #Rtv.Reactive("VEW1_{:02d}".format(s + 1), Plate_VEW1, initial_vol=0.0, pos=s + 1,
            #             excess=0)  # todo revise order !!!
            Rtv.Reactive("VEW2_{:02d}".format(s + 1), Plate_VEW2, initial_vol=0.0, pos=s + 1,
                         excess=0)  # todo revise order !!!


        with group("Prefill plates with VEW1, VEW2, EtOH and Elution buffer"):

            Itr.userPrompt("Put the plates for VEW1, VEW2 and EtOH in that order")

            with tips(reuse=True, drop=False):
                spread(reactive=VEW1, to_labware_region=Plate_VEW1.selectOnly(all_samples))

            with tips(reuse=True, drop=False):
                spread(reactive=VEW2, to_labware_region=Plate_VEW2.selectOnly(all_samples))

            with tips(reuse=True, drop=False):
                spread(reactive=EtOH80p, to_labware_region=Plate_EtOH.selectOnly(all_samples))

            Itr.userPrompt("Put the plates for the lysis in pos 1 and the for Eluat in pos 3")

            with tips(reuse=True, drop=False):
                spread(reactive=ElutionBuffer, to_labware_region=Plate_Eluat.selectOnly(all_samples))


        with group("Sample Lysis"):
            with tips(tipsMask=maxMask, reuse=True, drop=True):
                pK_cRNA_MS2.make()
                spread  (  reactive=pK_cRNA_MS2,   to_labware_region= Plate_lysis.selectOnly(all_samples))
                spread  (  reactive=LysisBuffer,   to_labware_region= Plate_lysis.selectOnly(all_samples))
            with tips(reuse=False, drop=True):
                transfer(  from_labware_region= Samples,
                           to_labware_region=   Plate_lysis,
                           volume=              SampleVolume,
                           using_liquid_class=  (SampleLiqClass,"Serum Disp postMix3"),
                           optimizeFrom         =False,     # optimizeTo= True,           # todo Really ??
                           NumSamples=          NumOfSamples)
            Itr.wash_tips(wasteVol=4, FastWash=True).exec()
            # with tips(reuse=False, drop=True):        # better reuse=True, drop=False, with normal Liquid Class ??
            #     spread  (  reactive=LysisBuffer,
            #                to_labware_region= Plate_lysis.selectOnly(all_samples),
            #                using_liquid_class=(None,"Serum Disp postMix3"))

            with incubation(minutes=15):
                Itr.userPrompt("Please Schutteln the plates for lysis in pos 1")

        with group("Beads binding"):
            with tips(tipsMask=maxMask, reuse=True, drop=False):
                for p in [40, 50, 60, 65]:
                   mix_reactive(B_Beads, LiqClass=Beads_LC_1, cycles=1, maxTips=maxTips, v_perc=p)

            with tips(reuse=True, drop=True):
                spread( reactive=B_Beads,      to_labware_region=Plate_lysis.selectOnly(all_samples))
                spread( reactive=VEB,          to_labware_region=Plate_lysis.selectOnly(all_samples))

            # with tips(reuse=False, drop=True):   # better reuse=True, drop=False, with normal Liquid Class ??
            #     spread  (  reactive=VEB,
            #                to_labware_region= Plate_lysis.selectOnly(all_samples),
            #                using_liquid_class=(None,"Serum Disp postMix3"))
            with incubation(minutes=5):
                Itr.userPrompt("Please Schutteln the plates for lysis in pos 1")

        self.Script.done()
