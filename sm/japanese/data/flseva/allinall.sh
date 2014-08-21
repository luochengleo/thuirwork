./DIN-splitqrels imine.Iprob imine.Dqrels imine
cat ./iminerunlist | ./TRECsplitruns ./imine.Iprob.tid
cat ./iminerunlist | ./D-NTCIR-eval imine.Iprob.tid imine 5 100
mkdir jpflseva
mv *.Dnev ./jpflseva
