# Copyright (C) 2019-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2019-2019
__author__ = 'Ariel'

# Tutorial

from   EvoScriPy.protocol_steps import *
import EvoScriPy.instructions   as     Itr
import EvoScriPy.Labware        as     Lab
import EvoScriPy.Reagent        as     Rgt
from protocols.Evo200 import Evo200


class Tutorial_HL(Evo200):
    """
    Created n wells with 100 uL of mix1 diluted 1:10. A diluent is provided.
    A reagent "mix1" is diluted (distributed) in n wells 1:10.
    The final volume of each dilution is vf=100 uL.

    There are many ways to achieve that. Here is one:
    - Calculate how much to distribute from mix1 to each Dil_10. v= vf/10 and from diluent vd.
    - Create a reagent mix1 in an Eppendorf Tube 1,5 mL for v uL per "sample".
    - Create a reagent diluent in an cubette 100 mL for vd uL per "sample".
    - Generate check list
    - Create n Dil_10_i reagents ( i from 0 to n-1 )
    - Distribute mix1
    - Distribute diluent

    """

    name = "Tutorial_HL. Dilutions."
    min_s, max_s = 1, 96                    # all dilutions in one 96 well plate

    def def_versions(self):                 # for now just ignore the variants
        self.versions = {'No version': self.V_def               }

    def V_def(self):
        pass

    def __init__(self,
                 GUI                         = None,
                 num_of_samples: int           = 8,
                 worktable_template_filename = None,
                 output_filename             = None,
                 firstTip                    = None,
                 run_name: str               = ""):

        Evo200.__init__(self,
                        GUI                         = GUI,
                        num_of_samples=num_of_samples or Tutorial_HL.max_s,
                        worktable_template_filename = worktable_template_filename or
                                                      '../EvoScripts/wt_templates/tutorial_hl_dilution.ewt',
                        output_filename             = output_filename or '../current/dilutions_HL',
                        firstTip                    = firstTip,
                        run_name                    = run_name)

    def Run(self):
        self.initialize()           # if needed calls Executable.initialize() and set_EvoMode
                                    # which calls GUI.update_parameters() and set_defaults() from Evo200

        self.show_runtime_check_list    = True

        n = self.NumOfSamples
        assert 1 <= n <= Tutorial_HL.max_s , "In this demo we want to set dilutions in a 96 well plate."
        wt = self.worktable

        Itr.comment('Dilute 1:10 mix1 in {:d} wells.'.format(n)).exec()

        # Get Labwares (Cuvette, eppys, etc.) from the work table    -----------------------------------------------
        diluent_cuvette = wt.get_labware(Lab.Trough_100ml, "BufferCub")
        mixes           = wt.get_labware(Lab.Eppendorfrack, "mixes")

        vf = 100                                      # The final volume of every dilution, uL
        v  = vf /10                                   # uL to be distribute from original mix1 to each Dil_10
        vd = vf - v                                   # uL to be distribute from diluent to each Dil_10



        diluent = Rgt.Reagent("Diluent",              # Define the reagents in each labware (Cuvette, eppys, etc.) -
                              diluent_cuvette,
                              volpersample = vd )

        mix1    = Rgt.Reagent("mix1",
                              mixes,
                              volpersample = v)

        self.check_list()                                          # Show the check_list   -------------------------

        Itr.wash_tips(wasteVol=5, FastWash=True).exec()

        plate = wt.get_labware(labw_type="96 Well Microplate", label="plate")

        dilution = Rgt.Reagent("mix1, diluted 1:10",               # Define place for temporal reactions  ----------
                                plate,
                                replicas         = n,
                                minimize_aliquots= False)

        with group("Fill dilutions"):

            Itr.userPrompt("Put the plate for dilutions in " + str(plate.location)).exec()

            with self.tips(tip_type="DiTi 200 ul", reuse=True, drop=False, drop_last=True):
                self.distribute(reagent           = mix1,
                                to_labware_region = dilution.select_all())

            with self.tips(tip_type="DiTi 1000ul", reuse=True, drop=False, drop_last=True):
                self.distribute(reagent           = diluent,
                                to_labware_region = dilution.select_all())

            self.drop_tips()

        self.done()


if __name__ == "__main__":
    p = Tutorial_HL(num_of_samples= 42,
                    run_name        = "_42s")

    p.use_version('No version')
    p.Run()
