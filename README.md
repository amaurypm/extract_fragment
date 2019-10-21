# extract_fragment
Extract Rosetta fragments from PDB, using pymol as a library.

## Goal
I created this script to be able to follow flexible peptide docking using [FlexPepDock](https://www.rosettacommons.org/docs/latest/application_documentation/docking/flex-pep-dock). I was interested in the case where the binding site is unknown, so I had to use the PIPER-FlexPepDock protocol.

When you follow the instructions for the PIPER-FlexPepDock protocol, after the fragment generation with `make_fragments.pl` they simply said:

> These assigned fragments are extracted from the Protein Data Bank (including the side-chains).

but no script is provided to do that, and that is the reason of this script.

## Expected input format
File(s) named something like seqname.N.nmers, where seqname is the name of your sequence, N the number of selected fragments and n the length of the fragments.
With a content similar to:
> position:            1 neighbors:          100

> 3lf2 A   259 G L   79.841   23.568  174.143  -21.920   52.450  -55.690

> 3lf2 A   260 G L   90.324   29.544 -178.881  -22.640   55.040  -58.370

> 3lf2 A   261 L L  -84.370  -18.629 -179.931  -21.980   52.820  -61.390

> 3lf2 A   262 S L  -68.835  113.560 -179.728  -25.200   53.920  -63.090

> 3lf2 A   263 R L  -80.025  -11.761 -177.097  -24.250   56.330  -65.870

> 3lf2 A   264 H L  -81.399  140.015 -178.424  -27.920   57.150  -66.420

> 3lf2 A   265 A L  -78.782    0.000    0.000  -29.340   60.340  -64.930

> ...

## Output
PDB files containing the fragments. If the sequence from the PDB does not corerspond with the sequence specified in the fragment file a warning will be printed and not PDB will be saved (it happens, a lot, almost for half the fragments. I don't know why)

