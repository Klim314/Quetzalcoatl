#!/usr/bin/env python 3

from modules import sent_tokenize as st

tst = "colonic colonization of clostridium spp. is associated with accumulation of tregs, which inhibits development of inflammatory lesions. to investigate whether infection with the clostridium leptum sp. can specifically induce tregs and/or tdcs bone marrow-derived dendritic cells were cultured in the presence or absence of c. leptum then co-cultured with cd4(+)cd25(-) t cells or not"
print(st.preprocess(tst))