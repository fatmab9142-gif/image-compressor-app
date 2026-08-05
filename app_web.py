import io
import streamlit as st
from PIL import Image

st.title("Image Compressor Pro")

# File Uploader
uploaded_file = st.file_uploader("Image upload karein", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Image Load Karein
    img = Image.open(uploaded_file)
    
    # RGBA / Palette mode ko RGB me convert karein (PNG / Transparency Fix)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    st.image(img, caption="Original Image", use_container_width=True)

    # Compression Level Slider
    quality = st.slider("Quality (Compress Level)", 10, 90, 70)

    if st.button("Compress Image"):
        # Image Compress Logic
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=int(quality), optimize=True)
        buffer.seek(0)
        
        # File Size Calculation (KB me)
        original_bytes = uploaded_file.getvalue()
        compressed_bytes = buffer.getvalue()
        
        original_size = len(original_bytes) / 1024
        compressed_size = len(compressed_bytes) / 1024
        
        # Success Message
        st.success(f"Compressed Successfully! Size: {original_size:.1f} KB ➔ {compressed_size:.1f} KB")
        st.image(compressed_bytes, caption="Compressed Image", use_container_width=True)

        # Download Button
        st.download_button(
            label="Download Compressed Image",
            data=buffer.getvalue(),
            file_name=f"compressed_{uploaded_file.name}",
            mime="image/jpeg"
        )