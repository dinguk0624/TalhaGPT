# modules/image_gen.py
import os

import torch
from diffusers import AutoPipelineForText2Image

pipe = None
device = None


def init_image_pipeline():
    """Lazy-load SDXL Turbo with automatic CUDA / CPU selection."""
    global pipe, device
    if pipe is not None:
        return

    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16
        variant = "fp16"
        print("[Görsel Modülü]: CUDA bulundu → SDXL Turbo GPU (fp16) üzerine yükleniyor...")
    else:
        device = "cpu"
        dtype = torch.float32
        variant = None
        print("[Görsel Modülü]: CUDA bulunamadı → CPU kullanılacak (çok yavaş olabilir).")

    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=dtype,
        variant=variant,
    )
    pipe.to(device)


def generate_image(prompt: str) -> str:
    """Generate a 512x512 image from the given prompt and save it."""
    if not prompt or not str(prompt).strip():
        return "[Görsel Hatası]: Prompt boş olamaz."

    try:
        init_image_pipeline()
        print(f"[Görsel Modülü]: '{prompt}' için görsel çiziliyor ({device})...")

        # SDXL Turbo: 1-2 step fast generation
        image = pipe(
            prompt=prompt,
            num_inference_steps=2,
            guidance_scale=0.0,
        ).images[0]

        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)

        existing = len([f for f in os.listdir(output_dir) if f.endswith(".png")])
        filename = f"{output_dir}/resim_{existing + 1}.png"
        image.save(filename)

        abs_path = os.path.abspath(filename)
        return f"[Başarılı]: Görsel üretildi → {abs_path}"
    except Exception as e:
        return f"[Görsel Hatası]: {e}"
