# modules/image_gen.py
import os
import torch
from diffusers import AutoPipelineForText2Image

pipe = None

def init_image_pipeline():
    global pipe
    if pipe is None:
        print("[Görsel Modülü]: SDXL Turbo modeli RTX 4060 GPU üzerine yükleniyor...")
        # SDXL Turbo: 8GB VRAM için çok hızlı ve yüksek kaliteli resim üretir
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", 
            torch_dtype=torch.float16, 
            variant="fp16"
        )
        pipe.to("cuda")

def generate_image(prompt: str) -> str:
    """Verilen İngilizce istemle (prompt) 512x512 görsel üretir ve kaydeder."""
    try:
        init_image_pipeline()
        print(f"[Görsel Modülü]: '{prompt}' için görsel çiziliyor...")
        
        # 1-2 adımda ışık hızında üretim (SDXL Turbo özelliği)
        image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
        
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/resim_{len(os.listdir(output_dir)) + 1}.png"
        image.save(filename)
        
        return f"[Başarılı]: Görsel başarıyla üretildi ve '{filename}' yoluna kaydedildi!"
    except Exception as e:
        return f"[Görsel Hatası]: {e}"