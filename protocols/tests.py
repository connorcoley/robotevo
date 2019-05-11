# Copyright (C) 2014-2019, Ariel Vina Rodriguez ( arielvina@yahoo.es )
#  distributed under the GNU General Public License, see <http://www.gnu.org/licenses/>.
#
# author Ariel Vina-Rodriguez (qPCR4vir)
# 2014-2019
__author__ = 'qPCR4vir'


test_dir = '../current/tests/'


from protocols.Prefill_plates_VEW1_ElutionBuffer_VEW2 import Prefill_plates_VEW1_ElutionBuffer_VEW2 as Prt

p = Prt (NumOfSamples    = 96,
         output_filename = test_dir + 'Prefill_plates_VEW1_ElutionBuffer_VEW2',
         run_name        = "_test_96s")
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


p = Prt (NumOfSamples    = 6,
         output_filename = test_dir + 'Prefill_plates_VEW1_ElutionBuffer_VEW2',
         run_name        = "_test_6s")
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()



from protocols.PreKingFisher_RNAextNucleoMag_EtOH80p  import PreKingFisher_RNAextNucleoMag_EtOH80p as Prt

p = Prt (NumOfSamples    = 96,
         output_filename = test_dir + 'PreKingFisher_RNAextNucleoMag_EtOH80p',
         run_name        = "_test_96s_VL-pKmix prefill")
p.use_version('VL-pKmix prefill')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


p = Prt (NumOfSamples    = 6,
         output_filename = test_dir + 'PreKingFisher_RNAextNucleoMag_EtOH80p',
         run_name        = "_test_6s_VL-pKmix prefill")
p.use_version('VL-pKmix prefill')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


from protocols.RNAextractionMN_Mag_Vet import RNAextr_MN_Vet_Kit as Prt

p = Prt (NumOfSamples    = 48,
         output_filename = test_dir + 'RNAext_MNVet_TeMag',
         run_name        = "_test_48s_VL-pKmix prefill")
p.use_version('VL-pKmix prefill')
p.go_first_pos('A01')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


p = Prt (NumOfSamples    = 6,
         output_filename = test_dir + 'RNAext_MNVet_TeMag',
         run_name        = "_test_6s_VL-pKmix prefill")
p.use_version('VL-pKmix prefill')
p.go_first_pos('A01')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


p = Prt (NumOfSamples    = 48,
         output_filename = test_dir + 'RNAext_MNVet_TeMag',
         run_name        = "_test_48s_VL-pKmix Inactivated")
p.use_version('VL-pKmix Inactivated')
p.go_first_pos('A01')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


p = Prt (NumOfSamples    = 6,
         output_filename = test_dir + 'RNAext_MNVet_TeMag',
         run_name        = "_test_6s_VL-pKmix Inactivated")
p.use_version('VL-pKmix Inactivated')
p.go_first_pos('A01')
print("\n\n************ " + p.output_filename + " **************\n")
p.Run()


#from protocols.Prefill_plate_in_Evo200                import Prefill_plate_in_Evo200
#from protocols.RNAextractionMN_Mag_Vet                import RNAextr_MN_Vet_Kit
#from protocols.Prefill_plates_LysisBuffer             import Prefill_plates_LysisBuffer

#from protocols.Prefill_plates_LysisBuffer_and_ProtKpreMix  import Prefill_plates_LysisBuffer_and_ProtKpreMix
#from EvoScriPy.protocol_steps                         import Pipeline
#from protocols.PCR                                    import PCRexperiment
