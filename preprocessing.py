import json, librosa, os, glob
import subprocess

import os

DATA_DIR = os.getcwd()
print(DATA_DIR)

source_data_dir = f"{DATA_DIR}/an4"
target_data_dir = f"{DATA_DIR}/an4_converted"

def an4_build_manifest(transcripts_path, manifest_path, target_wavs_dir):
    """Build an AN4 manifest from a given transcript file."""
    with open(transcripts_path, 'r') as fin:
        with open(manifest_path, 'w') as fout:
            for line in fin:
                # Lines look like this:
                # <s> transcript </s> (fileID)
                transcript = line[: line.find('(') - 1].lower()
                transcript = transcript.replace('<s>', '').replace('</s>', '')
                transcript = transcript.strip()

                file_id = line[line.find('(') + 1 : -2]  # e.g. "cen4-fash-b"
                audio_path = os.path.join(target_wavs_dir, file_id + '.wav')

                duration = librosa.core.get_duration(filename=audio_path)

                # Write the metadata to the manifest
                metadata = {"audio_filepath": audio_path, "duration": duration, "text": transcript}
                json.dump(metadata, fout)
                fout.write('\n')

"""Process AN4 dataset."""
if not os.path.exists(source_data_dir):
    link = 'http://www.speech.cs.cmu.edu/databases/an4/an4_sphere.tar.gz'
    raise ValueError(
        f"Data not found at `{source_data_dir}`. Please download the AN4 dataset from `{link}` "
        f"and extract it into the folder specified by the `source_data_dir` argument."
    )

# Convert SPH files to WAV files
sph_list = glob.glob(os.path.join(source_data_dir, '**/*.sph'), recursive=True)
target_wavs_dir = os.path.join(target_data_dir, 'wavs')
if not os.path.exists(target_wavs_dir):
    print(f"Creating directories for {target_wavs_dir}.")
    os.makedirs(os.path.join(target_data_dir, 'wavs'))

for sph_path in sph_list:
    wav_path = os.path.join(target_wavs_dir, os.path.splitext(os.path.basename(sph_path))[0] + '.wav')
    cmd = ["sox", sph_path, wav_path]
    subprocess.run(cmd, check=True)

# Build AN4 manifests
train_transcripts = os.path.join(source_data_dir, 'etc/an4_train.transcription')
train_manifest = os.path.join(target_data_dir, 'train_manifest.json')
an4_build_manifest(train_transcripts, train_manifest, target_wavs_dir)

test_transcripts = os.path.join(source_data_dir, 'etc/an4_test.transcription')
test_manifest = os.path.join(target_data_dir, 'test_manifest.json')
an4_build_manifest(test_transcripts, test_manifest, target_wavs_dir)