import argparse
import glob
import json
import os
from mirdata.validate import md5
import logging

try:
    import adtof.config
except ImportError:
    logging.error("In order to use adtof you must have adtof installed. " "Please reinstall mirdata using `pip install 'mirdata[adtof]'")
    raise ImportError

DATASET_INDEX_PATH = "./mirdata/datasets/indexes/adtof_index_1.0.json"


def make_dataset_index(dataset_data_path):
    # annotation_dir = os.path.join(dataset_data_path, "annotations", "raw_midi")
    # annotation_files = glob.glob(os.path.join(annotation_dir, "*.midi"))
    # track_ids = sorted([os.path.basename(f).split(".")[0] for f in annotation_files])
    annotation_files = adtof.config.getFilesInFolder(dataset_data_path, adtof.config.RAW_MIDI)
    track_ids = sorted([adtof.config.getFileBasename(f) for f in annotation_files])

    # top-key level metadata
    # TODO add metadata while reading original files
    # metadata_checksum = md5(os.path.join(dataset_data_path, "id_mapping.txt"))
    index_metadata = {"metadata": {"id_mapping": ("id_mapping.txt", None)}}

    # top-key level tracks
    index_tracks = {}
    for track_id in track_ids:
        audioName = os.path.join(adtof.config.AUDIO, "{}.ogg".format(track_id))
        annotationName = os.path.join(adtof.config.RAW_MIDI, "{}.midi".format(track_id))
        audio_checksum = md5(os.path.join(dataset_data_path, audioName))
        annotation_checksum = md5(os.path.join(dataset_data_path, annotationName))

        index_tracks[track_id] = {
            "audio": (audioName, audio_checksum),
            "annotation": (annotationName, annotation_checksum),
        }

    # top-key level version
    dataset_index = {"version": None}

    # combine all in dataset index
    dataset_index.update(index_metadata)
    dataset_index.update({"tracks": index_tracks})

    with open(DATASET_INDEX_PATH, "w") as fhandle:
        json.dump(dataset_index, fhandle, indent=2)


def main(args):
    make_dataset_index(args.dataset_data_path)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Make dataset index file.")
    PARSER.add_argument("dataset_data_path", type=str, help="Path to dataset data folder.")

    main(PARSER.parse_args())
