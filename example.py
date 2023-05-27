from utils import get_chunks, get_segmentation, get_stats, plot

if __name__ == "__main__":
    segmentation = get_segmentation()
    plot(segmentation)
    chunked_segmentation = list(get_chunks(segmentation, chunks=3))
    plot(chunked_segmentation)
    chunked_stats = get_stats(chunked_segmentation)
    plot(chunked_segmentation, chunked_stats[:-1])
    stats = get_stats(segmentation)
    plot(segmentation, stats[:-1])
