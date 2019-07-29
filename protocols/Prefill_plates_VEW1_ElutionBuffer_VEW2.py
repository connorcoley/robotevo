# Copyright (C) 2018-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2018-2019
__author__ = 'Ariel'


from EvoScriPy.protocol_steps import *
import EvoScriPy.Instructions as Itr
import EvoScriPy.Labware as Lab
from protocols.Evo100 import Evo100_FLI
import EvoScriPy.Reagent as Rgt


class Prefill_plates_VEW1_ElutionBuffer_VEW2(Evo100_FLI):
    """
    Prefill plates with VEW1, Elution buffer and VEW2 for the
    Implementation of the protocol for RNA extraction using the NucleoMag® VET kit from MACHEREY-NAGEL
    with washes in the Fischer Robot.
    """

    name = "Prefill plates with VEW1, Elution buffer and VEW2 for KingFisher"
    min_s, max_s = 1, 96

    def def_versions(self):
        self.versions = {'Standard': self.V_Standard  }

    def V_Standard(self):
        pass

    def __init__(self,
                 GUI                            = None,
                 num_of_samples       : int       = None,
                 worktable_template_filename    = None,
                 output_filename                = None,
                 firstTip                       = None,
                 run_name: str                  = ""):

        Evo100_FLI.__init__(self,
                            GUI                     = GUI,
                            num_of_samples=num_of_samples or Prefill_plates_VEW1_ElutionBuffer_VEW2.max_s,
                            worktable_template_filename
                                                    = worktable_template_filename or
                                                      '../EvoScripts/wt_templates/Prefill_VEW1_ElutB_and_VEW2.ewt',
                            output_filename         = output_filename or
                                                      '../current/Prefill_plates_VEW1_ElutionBuffer_VEW2',
                            firstTip                = firstTip,
                            run_name                = run_name)

    def Run(self):
        self.initialize()                       # set_defaults ??

        NumOfSamples = self.NumOfSamples
        wt           = self.worktable

        Itr.comment('Prefill plates with VEW1, Elution buffer and VEW2 for {:s} samples.'
                                                            .format(str(NumOfSamples))).exec()


                                                            # Get Labwares (Cuvette, eppys, etc.) from the work table

        ElutBuf     = wt.get_labware(Lab.Trough_100ml, "1-VEL-ElutionBuffer")

        DiTi1000_1  = wt.get_labware(Lab.DiTi_1000ul, "1000-1")
        DiTi1000_2  = wt.get_labware(Lab.DiTi_1000ul, "1000-2")
        DiTi1000_3  = wt.get_labware(Lab.DiTi_1000ul, "1000-3")

        Plate_VEW1  = wt.get_labware(Lab.MP96deepwell, "Plate VEW1")  # Plate 12 x 8 ?
        Plate_VEW2  = wt.get_labware(Lab.MP96deepwell, "Plate VEW2")  # Plate 12 x 8 ?
        Plate_Eluat = wt.get_labware(Lab.MP96well, "Plate ElutB")  # Plate 12 x 8 ? MP96well !!


                                                            # Set the initial position of the tips

        self.go_first_pos()

                                                            # Set volumen / sample

        VEW1Volume          = 600.0
        VEW2Volume          = 600.0
        ElutionBufferVolume = 100.0

                                                        # Liquid classes used for pippetting.
                                                        # Others liquidClass names are defined in "protocol_steps.py"

        # SampleLiqClass = "Serum Asp"  # = TissueHomLiqClass   # SerumLiqClass="Serum Asp preMix3"


        all_samples = range(NumOfSamples)
        maxTips     = min  (self.n_tips, NumOfSamples)
        maxMask     = robot.tipsMask[maxTips]

                                                        # Define the reactives in each labware (Cuvette, eppys, etc.)

        VEW1            = Rgt.Reagent("VEW1 - Wash Buffer ",
                                      wt.get_labware(Lab.Trough_100ml, "4-VEW1 Wash Buffe"),
                                      volpersample  = VEW1Volume,
                                      defLiqClass   = B_liquidClass)

        VEW2            = Rgt.Reagent("VEW2 - WashBuffer ",
                                      wt.get_labware(Lab.Trough_100ml, "5-VEW2-WashBuffer"),
                                      volpersample  =VEW2Volume,
                                      defLiqClass   =B_liquidClass)

        ElutionBuffer   = Rgt.Reagent("Elution Buffer ",
                                      ElutBuf,
                                      volpersample  =ElutionBufferVolume,
                                      defLiqClass   =B_liquidClass)

                                                        # Show the check_list GUI to the user for posible small changes

        self.check_list()
        self.set_EvoMode()

        Itr.wash_tips(wasteVol=30, FastWash=True).exec()

        par = Plate_VEW1.parallelOrder(self.n_tips, all_samples)

        # Define samples and the place for temporal reactions
        for s in all_samples:
            Rgt.Reagent("VEW1_{:02d}".format(s + 1),
                        Plate_VEW1,
                        initial_vol  = 0.0,
                        wells=par[s] + 1,
                        excess       = 0)  # todo revise order !!!

            Rgt.Reagent("VEW2_{:02d}".format(s + 1),
                        Plate_VEW2,
                        initial_vol = 0.0,
                        wells=par[s] + 1,
                        excess      = 0)

            Rgt.Reagent("Eluat_{:02d}".format(s + 1),
                        Plate_Eluat,
                        initial_vol = 0.0,
                        wells=par[s] + 1,
                        excess      = 0)


        with group("Prefill plates with VEW1, Elution buffer and VEW2"):

            Itr.userPrompt("Put the plates for VEW1, Elution buffer and VEW2 in that order").exec()

            with self.tips(reuse=True, drop=False):
                self.distribute(reagent             = ElutionBuffer,
                                to_labware_region   = Plate_Eluat.selectOnly(all_samples))    # ,optimize=False

            with self.tips(reuse=True, drop=False):
                self.distribute(reagent             =VEW2,
                                to_labware_region   =Plate_VEW2.selectOnly(all_samples))      # , optimize=False

            with self.tips(reuse=True, drop=False):
                self.distribute(reagent             =VEW1,
                                to_labware_region   =Plate_VEW1.selectOnly(all_samples))      # , optimize=False

        self.drop_tips()

        self.done()


if __name__ == "__main__":

    p = Prefill_plates_VEW1_ElutionBuffer_VEW2(num_of_samples= 96,
                                               run_name        = "")

    p.use_version('Standard')
    # p.go_first_pos('A01')
    p.Run()
