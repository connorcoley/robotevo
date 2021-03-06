# Copyright (C) 2014-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2014-2019

__author__ = 'qPCR4vir'

"""
Maintain here a list of all available customer protocols
# todo separate this into a new registre_protocols.py and registre_in_GUI.py
"""

from protocols.demos.demo_two_mixes.demo_two_mixes import DemoTwoMixes
from protocols.evo100_f.RNAextractionMN_Mag_Vet.RNAextractionMN_Mag_Vet import RNAextr_MN_Vet_Kit
from protocols.evo100_f.Prefill_plates_VEW1_ElutionBuffer_VEW2.Prefill_plates_VEW1_ElutionBuffer_VEW2 import Prefill_plates_VEW1_ElutionBuffer_VEW2
from protocols.evo100_f.Prefill_plates_LysisBuffer.Prefill_plates_LysisBuffer import Prefill_plates_LysisBuffer
from protocols.evo100_f.PreKingFisher_RNAextNucleoMag_EtOH80p.PreKingFisher_RNAextNucleoMag_EtOH80p import PreKingFisher_RNAextNucleoMag_EtOH80p
from protocols.evo100_f.Prefill_plates_LysisBuffer.Prefill_plates_LysisBuffer_and_ProtKpreMix import Prefill_plates_LysisBuffer_and_ProtKpreMix
from EvoScriPy.protocol_steps                         import Pipeline
from protocols.demos.hello_world.hello_world import HelloWorld

available         = []
available_classes = {}

available.append( DemoTwoMixes                     ())
available.append( Prefill_plates_VEW1_ElutionBuffer_VEW2      ())
available.append( Prefill_plates_LysisBuffer                  ())
available.append( Prefill_plates_LysisBuffer_and_ProtKpreMix  ())
available.append( PreKingFisher_RNAextNucleoMag_EtOH80p       ())
available.append( RNAextr_MN_Vet_Kit                          ())
available.append( HelloWorld                                  ())


def registreExecutable(executable):
    """
    An alternative to direct registration in available
    :param executable:
    """
    available.append(executable)
    available_classes[executable.name] = executable.__class__


pipeline_PreKingFisher = Pipeline ( protocols=  [Prefill_plates_VEW1_ElutionBuffer_VEW2 (run_name = "Prefill"),
                                                 PreKingFisher_RNAextNucleoMag_EtOH80p  (run_name = "Lysis"   ) ],
                                    run_name='PreKingFisher')

registreExecutable(pipeline_PreKingFisher)
available.append(Pipeline())






