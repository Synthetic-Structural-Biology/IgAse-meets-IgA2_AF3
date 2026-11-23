# IgAse-IgA2 AlphaFold3 Modelling

This repository contains analysis scripts supporting the publication: _A “knob-in-hole” gate in the antibody CH1 domain underlies subclass-independent IgA hinge cleavage by the commensal metallopeptidase IgAse_, adding some additional metrics and plots to the original paper.

## Software Requirements

| Script | Software |
| --- | --- |
| [parallel_DockQ.py](./parallel_DockQ.py) | DockQ |
| [pydock_energies.ipynb](./pydock_energies.ipynb) | NumPy, Matplotlib, DockQ, pyDock3 |
| [scores-ICVV.ipynb](./scores-ICVV.ipynb) | NumPy, Matplotlib, ipSAE, USalign |
| [superimposition-ICVV.ipynb](./superimposition-ICVV.ipynb) | NumPy, Matplotlib, SciPy, ProDy |

## Repository Structure

```text
├── README.md
├── parallel_DockQ.py
├── scores-ICVV.ipynb
├── superimposition-ICVV.ipynb
├── AF3S_with_DockQ_z_scores.csv
├── plots/
```

## Reference

If you use any scripts from this repository in your research, or the original results of the paper, please cite the original publication:

```bibtex
@article{larrota2026pnas,
    title = {A “knob-in-hole” gate in the antibody CH1 domain underlies subclass-independent IgA hinge cleavage by the commensal metallopeptidase IgAse},
    author = {Ramírez-Larrota, Juan Sebastián  and Arasa Estivill, Guillem and López-Martín, Mario and Effantin, Gregory and Gragera, Marcos and Sánchez Sorzano, Carlos Óscar and Marcos, Enrique and Eckhard, Ulrich and Gomis-Rüth, Francesc Xavier},
    journal = {Proceedings of the National Academy of Sciences},
    doi = {10.1073/pnas.2626241123},
    year = {2026},
}
```

## Acknowledgements

This extended work was supported by a Conexión BCB mobility grant in collaboration with the Model3DBio group at ICVV-CSIC, led by Dr. Juan Fernández-Recio.
