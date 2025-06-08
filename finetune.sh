#!/bin/bash

# -----------------------------
# Variables
# -----------------------------
BRANCH="v1.23.0"
NEMO_DIR="./NeMo"
DATA_DIR=$(pwd)
export DATA_DIR=$DATA_DIR

# -----------------------------
# Clone NVIDIA NeMo
# -----------------------------
echo "📥 Cloning NVIDIA NeMo ($BRANCH)..."
git clone -b $BRANCH https://github.com/NVIDIA/NeMo $NEMO_DIR

# -----------------------------
# Run Fine-Tuning Script
# -----------------------------
echo "🚀 Starting fine-tuning..."
NEMO_MODEL_PATH="./models/stt_en_fastconformer_hybrid_large_pc.nemo"

python $NEMO_DIR/examples/asr/speech_to_text_finetune.py \
    --config-path="../asr/conf/fastconformer/hybrid_transducer_ctc/" \
    --config-name=fastconformer_hybrid_transducer_ctc_bpe \
    +init_from_nemo_model="$NEMO_MODEL_PATH" \
    ++model.train_ds.manifest_filepath="$DATA_DIR/an4_converted/train_manifest.json" \
    ++model.validation_ds.manifest_filepath="$DATA_DIR/an4_converted/test_manifest.json" \
    ++model.optim.sched.d_model=1024 \
    ++trainer.devices=1 \
    ++trainer.max_epochs=1 \
    ++trainer.precision=bf16 \
    ++model.optim.name="adamw" \
    ++model.optim.lr=0.1 \
    ++model.optim.weight_decay=0.001 \
    ++model.optim.sched.warmup_steps=100 \
    ++exp_manager.version=test \
    ++exp_manager.use_datetime_version=False \
    ++exp_manager.exp_dir="$DATA_DIR/checkpoints"

echo "✅ Fine-tuning complete."
