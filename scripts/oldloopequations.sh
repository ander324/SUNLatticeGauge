#!/bin/bash

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHS++_0_1 LHS+-_0_1 LHS-+_0_1 LHS--_0_1 LHS++_0_2 LHS+-_0_2 LHS-+_0_2 LHS--_0_2 LHS++_0_3 LHS+-_0_3 LHS-+_0_3 LHS--_0_3 LHS++_1_2 LHS+-_1_2 LHS-+_1_2 LHS--_1_2 LHS++_1_3 LHS+-_1_3 LHS-+_1_3 LHS--_1_3 LHS++_2_3 LHS+-_2_3 LHS-+_2_3 LHS--_2_3 RHS | grep "++" > pp


~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHS++_0_1 LHS+-_0_1 LHS-+_0_1 LHS--_0_1 LHS++_0_2 LHS+-_0_2 LHS-+_0_2 LHS--_0_2 LHS++_0_3 LHS+-_0_3 LHS-+_0_3 LHS--_0_3 LHS++_1_2 LHS+-_1_2 LHS-+_1_2 LHS--_1_2 LHS++_1_3 LHS+-_1_3 LHS-+_1_3 LHS--_1_3 LHS++_2_3 LHS+-_2_3 LHS-+_2_3 LHS--_2_3 RHS | grep "+\-" > pm

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHS++_0_1 LHS+-_0_1 LHS-+_0_1 LHS--_0_1 LHS++_0_2 LHS+-_0_2 LHS-+_0_2 LHS--_0_2 LHS++_0_3 LHS+-_0_3 LHS-+_0_3 LHS--_0_3 LHS++_1_2 LHS+-_1_2 LHS-+_1_2 LHS--_1_2 LHS++_1_3 LHS+-_1_3 LHS-+_1_3 LHS--_1_3 LHS++_2_3 LHS+-_2_3 LHS-+_2_3 LHS--_2_3 RHS | grep "\-+" > mp

~/susy_catterall/peter_susy_scripts/loopcalcs.sh LHS++_0_1 LHS+-_0_1 LHS-+_0_1 LHS--_0_1 LHS++_0_2 LHS+-_0_2 LHS-+_0_2 LHS--_0_2 LHS++_0_3 LHS+-_0_3 LHS-+_0_3 LHS--_0_3 LHS++_1_2 LHS+-_1_2 LHS-+_1_2 LHS--_1_2 LHS++_1_3 LHS+-_1_3 LHS-+_1_3 LHS--_1_3 LHS++_2_3 LHS+-_2_3 LHS-+_2_3 LHS--_2_3 RHS | grep "\-\-" > mm

~/susy_catterall/peter_susy_scripts/loopcalcs.sh RHS > rhs


grep real pp > pp.real
grep real pm > pm.real
grep real mp > mp.real
grep real mm > mm.real

grep imag pp > pp.imag
grep imag pm > pm.imag
grep imag mp > mp.imag
grep imag mm > mm.imag


awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pp.real > lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pm.real >> lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mp.real >> lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mm.real >> lhssum

awk 'BEGIN{x=0;}{x+=$1;}END{print "lhs.real " x}' lhssum

awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pp.imag > lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print -x*5.5/(2.0*9.0)}' pm.imag >> lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mp.imag >> lhssum
awk 'BEGIN{x=0;}{x+=$3;}END{print x*5.5/(2.0*9.0)}' mm.imag >> lhssum

awk 'BEGIN{x=0;}{x+=$1;}END{print "lhs.imag " x}' lhssum



more rhs

