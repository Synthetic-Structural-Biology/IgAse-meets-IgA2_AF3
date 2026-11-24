# IgAse-IgA2 AlphaFold3 Modelling

This repository contains analysis scripts supporting the publication: _A “knob-in-hole” gate in the antibody CH1 domain underlies subclass-independent IgA hinge cleavage by the commensal metallopeptidase IgAse_, adding some additional metrics and plots to the original paper.
Initially, the metrics reported in the paper were: `pTM`, per chain and total `ipTM` and `ipSAE`, `TM score`, `Ligand RMSD` and `atom-atom distances`.
Here, we extend the work by adding `pDockQ2`, `DockQ` and `pyDock total energy` and correlating a few of all metrics.

## Software Requirements

| Script | Software requirements |
| --- | --- |
| [parallel_DockQ.py](./parallel_DockQ.py) | DockQ |
| [pydock_energies.ipynb](./pydock_energies.ipynb) | NumPy, Matplotlib, gemmi, DockQ, pyDock3 |
| [scores-ICVV.ipynb](./scores-ICVV.ipynb) | NumPy, Matplotlib, ipSAE, USalign |
| [superimposition-ICVV.ipynb](./superimposition-ICVV.ipynb) | NumPy, Matplotlib, SciPy, ProDy |

## Repository Structure

```text
├── README.md
├── parallel_DockQ.py
├── scores-ICVV.ipynb
├── superimposition-ICVV.ipynb
├── pydock_energies.ipynb
├── AF3S_with_DockQ_z_scores.csv
└── plots/
```

## Reference

If you use any scripts from this repository in your research, or the original results of the paper, please cite the original publication:

```bibtex
@article{larrota2026pnas,
    title = {A “knob-in-hole” gate in the antibody CH1 domain underlies subclass-independent IgA hinge cleavage by the commensal metallopeptidase IgAse},
    author = {Ramírez-Larrota, Juan Sebastián  and Arasa Estivill, Guillem and 
    López-Martín, Mario and Effantin, Gregory and Gragera, Marcos and Sánchez Sorzano, Carlos Óscar and 
    Marcos, Enrique and Eckhard, Ulrich and Gomis-Rüth, Francesc Xavier},
    journal = {Proceedings of the National Academy of Sciences},
    doi = {10.1073/pnas.2626241123},
    year = {2026}
}
```

Original scripts and data can be found in the [original Zenodo repository](https://zenodo.org/records/22232524).

## Acknowledgements

This extended work was done by [Guillem Arasa](https://github.com/guillemares), supported by a Conexión BCB grant during a short mobility program in collaboration with the Model3DBio group at ICVV-CSIC, led by Dr. Juan Fernández-Recio.
