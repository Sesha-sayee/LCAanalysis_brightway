# LCAanalysis_brightway

## Energy consumption sample calculation:
The energy consumption process for HTL at 300 C with MSW feed composition is detailed below:

Calculating heat capacity of feedstocks:

heat capacity of carbohydrate =  \frac((∑ (25 &#8594 HTL temp.) 1.31 + 4.27*0.001*temp. ))(/((HTL temp.-25)))  
        
heat capacity of starch =  (∑_25^(HTL temp.)▒〖1.26 + 5.24*0.001*temp.〗)/((HTL temp.-25))
       
Amino acid composition of protein is considered to be same as soy protein. The table below shows the amino acid composition and heat capacity for each amino acid:

Comp.	ala	arg	asn	asp	cys	gln	glu	gly	his	ile
(%)	4.3	7.6	0	11.5	1.2	0	19	4.2	2.6	4.8
Cp (cal/kmol)	27.13	55.8	38.3	37.09	38.8	44.02	41.84	23.71	51.48	45
Comp.	leu	lys	met	phe	pro	ser	thr	trp	tyr	val
(%)	8.1	6.2	1.4	5.2	5.1	5.2	3.7	1.4	3.7	5
Cp (cal/kmol)	48.03	48.94	69.32	48.52	36.13	32.4	35.2	56.92	51.73	40.34

heat capacity of protein =  (∑▒〖〖C_p〗_(amino acid) (in KJ/KgK) ×amino acid composition (wt.%)〗)/100

For lipids, we calculated the average of heat capacities from 6 different lipids. 
        *List Cp grapeseed oil = 2.081 KJ/kgK
        *List Cp almond oil = 2.103 KJ/kgK
        *List Cp vegetable oil = 2.081 KJ/kgK
        *List Cp olive oil = 2.116 KJ/kgK
        *List Cp cocoa butter = 2.143 KJ/kgK
        *List Cp coconut oil = 2.111 KJ/kgK

Average Cp lipid = 2.106; #KJ/kgK

The heat capacity of lignin, PP, PS, PC, PET are constants and equal to 2.2, 1.92, 1.5, 1.25, 1.25 KJ/kgK respectively. 

heat capacity of feedstock =  (∑▒〖〖C_p〗_component  ×component composition (wt.%)〗)/100=1.86 KJ/kgK

The heat capacity of water is calculated using pressure as a function of temperature given by the equation:

Pressure=  e^(34.494 - 4924.99/(temp.+237.1)))⁄〖(temp.+105)〗^1.57 
       
Figure below shows the heating curve for this equation. The heat capacity of water is calculated as follows: 

heat capacity of water =  (∑_25^(HTL temp.)▒〖C_p (temp.,pressure(temp.))〗)/((HTL temp.-25))=4.54 KJ/kgK, where Cp(temp., pressure) and pressure(temp.) are functions like f(x,y) and f(x). 

The heat capacity of feedstock is mass averaged based on feedstock loading.

heat capacity of slurry =  (〖C_p〗_water×(wt.% water in slurry)+ 〖C_p〗_feedstock×(wt.% feedstock in slurry))/100=3.83 KJ/kgK

The heat needed to melt the plastic is also accounted. The heat of fusion for PP, PS, PC, PET are 165, 105.26, 134, 66.94 KJ/kg respectively

From the PNNL studies, the heat integration factor is 0.9. 

HTL step energy consumption=(1-heat integration factor)×feedstock flow rate ×{heat capacity of slurry×(HTL temp.-25)×((100+feedstock loading)/(feedstock loading))+ ∑_plastic▒〖plastic (wt.%)×heat of fusion〗}×1/(reactor heating effeciency)
