import streamlit as st
from PIL import Image
import io

# Page setup - Wide layout (Desktop jaisa feel ke liye)
st.set_page_config(page_title="Image Compressor Pro", layout="wide")

st.title("🖼️ Image Compressor Pro")

# Sidebar - Controls (Desktop ke Left Panel ki tarah)
with st.sidebar:
    st.header("⚙️ Settings")
    quality = st.slider("Quality", min_value=1, max_value=100, value=80)
    
    st.markdown("---")
    st.subheader("Batch Options")
    fast_mode = st.toggle("Fast mode")
    
    st.markdown("---")
    st.caption("Appearance: Dark Mode (Default)")

# Main Area Layout (Top Drag/Drop, Bottom Side-by-side comparison)
uploaded_file = st.file_uploader("Drag & Drop an image here", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Original Image
    img = Image.open(uploaded_file)
    original_bytes = uploaded_file.getvalue()
    orig_size_kb = len(original_bytes) / 1024

    # Compress Image
    buffer = io.BytesIO()
    # Convert RGBA to RGB for JPEG format
    if img.mode in ("RGBA", "P"):
        img_conv = img.convert("RGB")
    else:
        img_conv = img
    
    img_conv.save(buffer, format="JPEG", quality=quality)
    compressed_bytes = buffer.getvalue()
    comp_size_kb = len(compressed_bytes) / 1024

    st.markdown("---")

    # Side-by-Side Comparison (Desktop UI ki tarah)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original")
        st.image(img, use_container_width=True)
        st.info(f"**Size:** {orig_size_kb:.2f} KB")

    with col2:
        st.subheader("Compressed")
        st.image(buffer.getvalue(), use_container_width=True)
        st.success(f"**Size:** {comp_size_kb:.2f} KB")
        
        # Download Button
        st.download_button(
            label="💾 Download Compressed Image",
            data=compressed_bytes,
            file_name=f"compressed_{uploaded_file.name}",
            mime="image/jpeg"
        )
else:
    st.info("Load an image to get started.")
