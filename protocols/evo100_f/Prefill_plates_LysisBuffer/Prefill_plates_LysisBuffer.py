# Copyright (C) 2018-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2018-2019
__author__ = 'Ariel'
# this is now one version in Prefill_plates_LysisBuffer_and_ProtKpreMix

from EvoScriPy.protocol_steps import *
from protocols.evo100_f.evo100_f import Evo100_FLI


class Prefill_plates_LysisBuffer(Evo100_FLI):
    """
    Prefill plates with LysisBuffer for the
    Implementation of the protocol for RNA extraction using the NucleoMag® VET kit from MACHEREY-NAGEL
    with washes in the Fischer Robot.
    """

    name = "Prefill plates with LysisBuffer for KingFisher"
    min_s, max_s = 1, 96

    def def_versions(self):
        self.versions = {'3 plate': self.V_3_plate,
                         '2 plate': self.V_2_plate,
                         '1 plate': self.V_1_plate}

    def V_1_plate(self):        self.num_plates = 1
    def V_2_plate(self):        self.num_plates = 2
    def V_3_plate(self):        self.num_plates = 3

    def __init__(self, GUI=None, run_name=None, output_filename=None):

        this = Path(__file__).parent

        Evo100_FLI.__init__(self,
                            GUI                     = GUI,
                            num_of_samples          = Prefill_plates_LysisBuffer.max_s,
                            worktable_template_filename=this / 'Prefill_plates_LysisBuffer.ewt',
                            output_filename         = output_filename or this / 'scripts' / 'Prefill_LysisBuffer',
                            run_name                = run_name)

    def run(self):
        self.initialize()

        num_of_samples = self.num_of_samples
        wt           = self.worktable

        self.comment('Prefill {:d} plates with LysisBufferReact for {:d} samples.'
                     .format(self.num_plates, num_of_samples))

                                                       # Get Labwares (Cuvette, eppys, etc.) from the work table
        LysBufCuvette = wt.get_labware("2-Vl Lysis Buffer", labware.Trough_100ml)

        DiTi1000_1  = wt.get_labware("1000-1", labware.DiTi_1000ul)
        DiTi1000_2  = wt.get_labware("1000-2", labware.DiTi_1000ul)
        DiTi1000_3  = wt.get_labware("1000-3", labware.DiTi_1000ul)


        self.set_first_tip()                      #  Set the initial position of the tips

        # Set volumen / sample
        LysisBufferVolume   = 100.0       # VL1 or VL

        all_samples = range(num_of_samples)

        # Define the reactives in each labware (Cuvette, eppys, etc.)

        LysisBufferReact = Reagent("VL - Lysis Buffer ",
                                   LysBufCuvette,
                                   volpersample = LysisBufferVolume,
                                   def_liq_class  = 'MN VL',
                                   num_of_samples= self.num_plates * num_of_samples)

        # Show the check_list GUI to the user for possible small changes

        self.check_list()
        self.set_EvoMode()

        instructions.wash_tips(wasteVol=5, FastWash=True).exec()

        LysPlat = [wt.get_labware("Plate lysis-" + str(i + 1), labware.MP96deepwell) for i in range(self.num_plates)]

        par = LysPlat[0].parallelOrder(self.n_tips, all_samples)

        # Define place for intermediate reactions
        for i, LP in enumerate(LysPlat):
            for s in all_samples:
                Reagent("lysis_{:d}-{:02d}".format(i + 1, s + 1),
                            LP,
                            initial_vol =0.0,
                            wells=s + 1,
                            excess      =0)

        with group("Prefill plates with LysisBufferReact"):

            self.user_prompt("Put the plates for LysisBufferReact")

            for LP in LysPlat:
                with self.tips(reuse=True, drop=False):
                    self.distribute(reagent=LysisBufferReact, to_labware_region=LP.selectOnly(all_samples))
                self.drop_tips()

        self.done()


if __name__ == "__main__":

    p = Prefill_plates_LysisBuffer(run_name='1 plate')

    p.use_version('1 plate')
    p.run()
