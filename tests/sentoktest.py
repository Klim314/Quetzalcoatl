from data import sent_tokenize as st


a = ('effect of supplements with lactic acid bacteria and oligofructose on the intestinal microflora during administration of cefpodoxime proxetil.',\
 'thirty healthy volunteers in three groups participated in a study of the effect on the intestinal microflora of oral supplementation with\
  bifidobacterium longum, lactobacillus acidophilus and oligofructose, an indigestible oligosaccharide, during oral administration of cefpodoxime\
   proxetil bd for 7 days. those in group a also received an oral supplement with c.1011 cfu of b. longum bb 536 and l. acidophilus ncfb 1748 and 15 g\
    oligofructose daily, those in group b received a supplement with oligofructose only and those in group c received placebo, for 21 days. in all\
     three groups there was a marked decrease in aerobic microorganisms, involving mainly a rapid and almost complete disappearance of escherichia coli\
      (p: < 0.05) during antimicrobial administration and, thereafter, an overgrowth of enterococci (p: < 0.05). the number of intestinal yeasts also \
      increased significantly (p: < 0.05) in groups a and b over the same period. there was a dramatic decrease in anaerobic microorganisms on day 4\
       of administration, mainly caused by loss of bifidobacteria (p: < 0.05) in all groups. the number of lactobacilli also decreased but was\
        significantly higher in group a than in group c at the end of cefpodoxime proxetil administration. clostridium difficile was found in \
        only one person from group a, but six persons each in groups b and c. of the bifidobacterial strains isolated from the faecal samples\
         in group a, one was similar to the strain of b. longum administered, but most volunteers were colonized by several different strains of b. longum during the investigation period. the administered strain of l. acidophilus was recovered from six patients in group a.')
st.preprocess(a[1])