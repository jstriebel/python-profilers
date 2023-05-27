from pathlib import Path

from utils import get_chunks, get_segmentation, get_stats, plot, save_chunked_stats

if __name__ == "__main__":
    segmentation = get_segmentation(size=1000, segments=200, radius=0.05)
    # plot(segmentation)
    chunked_segmentation = list(get_chunks(segmentation, chunks=100))
    chunked_stats = get_stats(chunked_segmentation, repeat=500)

    data_path = Path("data")
    data_path.mkdir(exist_ok=True)
    save_chunked_stats(chunked_stats, data_path)
