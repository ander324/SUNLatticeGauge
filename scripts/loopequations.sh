#!/bin/bash

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHSpp_0_1 LHSpm_0_1 LHSmp_0_1 LHSmm_0_1 LHSpp_0_2 LHSpm_0_2 LHSmp_0_2 LHSmm_0_2 LHSpp_0_3 LHSpm_0_3 LHSmp_0_3 LHSmm_0_3 LHSpp_1_2 LHSpm_1_2 LHSmp_1_2 LHSmm_1_2 LHSpp_1_3 LHSpm_1_3 LHSmp_1_3 LHSmm_1_3 LHSpp_2_3 LHSpm_2_3 LHSmp_2_3 LHSmm_2_3 RHS | grep "pp" > pp


~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHSpp_0_1 LHSpm_0_1 LHSmp_0_1 LHSmm_0_1 LHSpp_0_2 LHSpm_0_2 LHSmp_0_2 LHSmm_0_2 LHSpp_0_3 LHSpm_0_3 LHSmp_0_3 LHSmm_0_3 LHSpp_1_2 LHSpm_1_2 LHSmp_1_2 LHSmm_1_2 LHSpp_1_3 LHSpm_1_3 LHSmp_1_3 LHSmm_1_3 LHSpp_2_3 LHSpm_2_3 LHSmp_2_3 LHSmm_2_3 RHS | grep "pm" > pm

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHSpp_0_1 LHSpm_0_1 LHSmp_0_1 LHSmm_0_1 LHSpp_0_2 LHSpm_0_2 LHSmp_0_2 LHSmm_0_2 LHSpp_0_3 LHSpm_0_3 LHSmp_0_3 LHSmm_0_3 LHSpp_1_2 LHSpm_1_2 LHSmp_1_2 LHSmm_1_2 LHSpp_1_3 LHSpm_1_3 LHSmp_1_3 LHSmm_1_3 LHSpp_2_3 LHSpm_2_3 LHSmp_2_3 LHSmm_2_3 RHS | grep "mp" > mp

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHSpp_0_1 LHSpm_0_1 LHSmp_0_1 LHSmm_0_1 LHSpp_0_2 LHSpm_0_2 LHSmp_0_2 LHSmm_0_2 LHSpp_0_3 LHSpm_0_3 LHSmp_0_3 LHSmm_0_3 LHSpp_1_2 LHSpm_1_2 LHSmp_1_2 LHSmm_1_2 LHSpp_1_3 LHSpm_1_3 LHSmp_1_3 LHSmm_1_3 LHSpp_2_3 LHSpm_2_3 LHSmp_2_3 LHSmm_2_3 RHS | grep "mm" > mm

~/susy_catterall/peter_susy_scripts/loopcalcs.sh RHS > rhs


grep real pp > pp.real
grep real pm > pm.real
grep real mp > mp.real
grep real mm > mm.real

grep imag pp > pp.imag
grep imag pm > pm.imag
grep imag mp > mp.imag
grep imag mm > mm.imag


awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pp.real > lhssum.real
awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pm.real >> lhssum.real
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mp.real >> lhssum.real
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mm.real >> lhssum.real

awk 'BEGIN{x=0;}{x+=$1;}END{print "LHS.real = " x}' lhssum.real

awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pp.imag > lhssum.imag
awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pm.imag >> lhssum.imag
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mp.imag >> lhssum.imag
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mm.imag >> lhssum.imag

awk 'BEGIN{x=0;}{x+=$1;}END{print "LHS.imag = " x}' lhssum.imag

more rhs

