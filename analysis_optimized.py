from pathlib import Path

import h5py
import numpy as np


def load_data_hdf5(path):
    segments = []
    counts = []
    centers = []
    for hdf5_path in sorted(path.glob("*.hdf5"), key=lambda p: int(p.stem)):
        with h5py.File(hdf5_path, "r") as f:
            segments.append(f["segments"][:])
            counts.append(f["counts"][:])
            centers.append(f["centers"][:])
    return segments, counts, centers


def combine_stats_numpy(chunked_segments, chunked_counts, chunked_centers):
    all_segments = np.concatenate(
        [i.astype(np.uint32) for i in chunked_segments if len(i) > 0]
    )
    all_counts = np.concatenate(
        [i.astype(np.uint32) for i in chunked_counts if len(i) > 0]
    )
    all_centers = np.concatenate(
        [i.astype(np.float32) for i in chunked_centers if len(i) > 0]
    )

    # sort all arrays by all_segments
    sort_idx = np.argsort(all_segments)
    all_segments = all_segments[sort_idx]
    all_counts = all_counts[sort_idx]
    all_centers = all_centers[sort_idx]

    # group by segments (g_idx is where the groups start)
    g_segments, g_idx = np.unique(all_segments, return_index=True)
    g_counts = np.split(all_counts, g_idx[1:])
    g_centers = np.split(all_centers, g_idx[1:])

    # empty arrays for results
    segments = np.ndarray(len(g_segments), dtype=all_segments.dtype)
    counts = np.ndarray(len(g_segments), dtype=all_counts.dtype)
    centers = np.ndarray((len(g_segments), 2), dtype=all_centers.dtype)

    # combine stats for each segment
    for i, (segment, segment_counts, segment_centers) in enumerate(
        zip(g_segments, g_counts, g_centers)
    ):
        count_sum = segment_counts.sum()
        center = (segment_centers * segment_counts[:, np.newaxis]).sum(
            axis=0
        ) / count_sum
        segments[i] = segment
        counts[i] = count_sum
        centers[i] = center
    return segments, counts, centers


if __name__ == "__main__":
    chunked_stats = load_data_hdf5(Path("data"))
    combined_stats = combine_stats_numpy(*chunked_stats)
    print(f"Got {len(combined_stats[0])} stats.")
