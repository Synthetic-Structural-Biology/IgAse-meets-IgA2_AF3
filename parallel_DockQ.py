import os
import re
import json
import glob
import subprocess
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

af_models = [
    "/DATA/Projects/03-IgAse_IgA2_Modelling/AF3_server/outs/IgAse_IgA2_wt_multiple_seeds_1",
    "/DATA/Projects/03-IgAse_IgA2_Modelling/AF3_server/outs/IgAse_IgA2_wt_multiple_seeds_2",
    "/DATA/Projects/03-IgAse_IgA2_Modelling/AF3_server/outs/IgAse_IgA2_wt_multiple_seeds_3",
    "/DATA/Projects/03-IgAse_IgA2_Modelling/AF3_server/outs/IgAse_IgA2_wt_multiple_seeds_4"
    ]
cif_files = [cif for i in af_models for cif in glob.glob(os.path.join(i, "**/*.cif"), recursive=False)]

# print(f"Found {len(cif_files)} mmCIF files for analysis.")

# --------------------------------------------------
# 1. Run DockQ
# --------------------------------------------------

def run_DockQ(
    model_pdb,
    reference_pdb,
    dockq_model="short",
    mapping=None,
):

    command = [
        "DockQ",
        model_pdb,
        reference_pdb,
        f"--{dockq_model}",
        "--n_cpu=2",
    ]

    if mapping is not None:
        command.append(f"--mapping={mapping}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"DockQ failed: {model_pdb} vs {reference_pdb}\n"
            f"{result.stderr}"
        )

    return parse_dockq_output(result.stdout)


# --------------------------------------------------
# 2. Parse DockQ output
# --------------------------------------------------

def parse_dockq_output(output):

    results = {}

    number = r"([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)"

    # Total DockQ
    total_match = re.search(
        rf"Total DockQ .*?:\s*{number}",
        output
    )

    if not total_match:
        raise ValueError("Could not find Total DockQ.")

    results["DockQ"] = float(total_match.group(1))

    # Per-interface metrics
    patterns = {
        "DockQ": rf"\bDockQ\s+{number}",
        "fnat": rf"\bfnat\s+{number}",
        "LRMSD": rf"\bLRMSD\s+{number}",
        "iRMSD": rf"\biRMSD\s+{number}",
    }

    for line in output.splitlines():

        if not re.match(r"\s*DockQ\s+", line):
            continue

        mapping_match = re.search(
            r"\bmapping\s+(\S+)",
            line
        )

        if not mapping_match:
            continue

        interface = mapping_match.group(1).split(":")[0]

        for metric, pattern in patterns.items():

            match = re.search(pattern, line)

            if match:
                results[f"{metric}_{interface}"] = float(
                    match.group(1)
                )

    return results


# --------------------------------------------------
# 3. Calculate one comparison
# --------------------------------------------------

def calculate_pair(task):

    model, reference = task

    try:

        metrics = run_DockQ(
            model_pdb=model,
            reference_pdb=reference,
            dockq_model="short"
        )

        return {
            "model": os.path.basename(model),
            "reference": os.path.basename(reference),
            "metrics": metrics,
            "status": "success"
        }

    except Exception as e:

        return {
            "model": os.path.basename(model),
            "reference": os.path.basename(reference),
            "status": "error",
            "error": str(e)
        }


# --------------------------------------------------
# 4. Generate pairwise comparisons
# --------------------------------------------------

def generate_pairs(files, directed=True):

    n = len(files)

    for i in range(n):

        for j in range(n):

            if i == j:
                continue

            # If directed=False, calculate only one direction
            if not directed and j <= i:
                continue

            yield files[i], files[j]


# --------------------------------------------------
# 5. Parallel execution and JSONL storage
# --------------------------------------------------

def run_parallel_dockq(
    cif_files,
    output_file="dockq_results.jsonl",
    max_workers=8,
    batch_size=100,
    directed=True,
):

    pairs = generate_pairs(cif_files, directed=directed)

    total = (
        len(cif_files) * (len(cif_files) - 1)
        if directed
        else len(cif_files) * (len(cif_files) - 1) // 2
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        with open(output_file, "a", buffering=1) as json_file:

            with tqdm(total=total, desc="DockQ calculations") as pbar:

                while True:

                    batch = list(islice(pairs, batch_size))

                    if not batch:
                        break

                    futures = [
                        executor.submit(calculate_pair, pair)
                        for pair in batch
                    ]

                    for future in as_completed(futures):

                        result = future.result()

                        # Only the main thread writes to the file
                        json_file.write(
                            json.dumps(result) + "\n"
                        )

                        pbar.update(1)

                    # Ensure completed results are flushed to disk
                    json_file.flush()

    print(f"Results saved to: {output_file}")


run_parallel_dockq(
    cif_files=cif_files,
    output_file="dockq_results.jsonl",
    max_workers=8,
    batch_size=100,
    directed=True
)