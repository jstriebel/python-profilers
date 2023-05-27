import json
from pathlib import Path


def load_data(path):
    segments = []
    counts = []
    centers = []
    for json_path in sorted(path.glob("*.json"), key=lambda p: int(p.stem)):
        with open(json_path) as f:
            data = json.load(f)
            segments.append(data["segments"])
            counts.append(data["counts"])
            centers.append(data["centers"])
    return segments, counts, centers


def combine_stats(chunked_segments, chunked_counts, chunked_centers):
    counts_per_segment = {}
    centers_per_segement = {}
    for segments_i, counts_i, centers_i in zip(
        chunked_segments, chunked_counts, chunked_centers
    ):
        for segment, count, center in zip(segments_i, counts_i, centers_i):
            counts_per_segment.setdefault(segment, []).append(count)
            centers_per_segement.setdefault(segment, []).append(center)

    result_segments = []
    result_counts = []
    result_centers = []
    for segment in counts_per_segment.keys():
        center_x = 0
        center_y = 0
        count_sum = 0
        for count, center in zip(
            counts_per_segment[segment], centers_per_segement[segment]
        ):
            center_x += center[0] * count
            center_y += center[1] * count
            count_sum += count

        result_segments.append(segment)
        result_counts.append(count_sum)
        result_centers.append((center_x / count_sum, center_y / count_sum))
    return result_segments, result_counts, result_centers


if __name__ == "__main__":
    chunked_stats = load_data(Path("data"))
    combined_stats = combine_stats(*chunked_stats)
    print(f"Got {len(combined_stats[0])} stats.")
