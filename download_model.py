import os
import nemo.collections.asr as nemo_asr

# Create the 'models' directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load the pretrained model from Hugging Face
print("📥 Downloading model from Hugging Face...")
asr_model = nemo_asr.models.EncDecHybridRNNTCTCBPEModel.from_pretrained(
    model_name="nvidia/stt_en_fastconformer_hybrid_large_pc"
)

# Save the model as a .nemo file in the 'models' folder
output_path = "models/stt_en_fastconformer_hybrid_large_pc.nemo"
asr_model.save_to(output_path)
print(f"✅ Model saved to: {output_path}")
