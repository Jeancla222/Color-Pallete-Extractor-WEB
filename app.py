import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import pandas as pd
import base64
from io import BytesIO

st.set_page_config(
    page_title="Color Palette Extractor",
    page_icon=None,
    layout="wide"
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Montserrat:wght@400;500&display=swap" rel="stylesheet">

<style>
*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #000000 !important;
    color: #f0f0f0 !important;
    font-family: 'Montserrat', sans-serif !important;
}

[data-testid="stHeader"] {
    background-color: #000000 !important;
}

[data-testid="stSidebar"] {
    background-color: #0d0d0d !important;
    border-right: 1px solid #1a1a1a !important;
}

[data-testid="stSidebar"] * {
    color: #cccccc !important;
    font-family: 'Montserrat', sans-serif !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stSidebar"] .stSlider label {
    color: #fc6100 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] div {
    color: #888888 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #1a1a1a !important;
}

h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

p, span, div, label, li {
    font-family: 'Montserrat', sans-serif !important;
}

.page-header {
    padding: 2.5rem 0 1rem 0;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 2rem;
}

.page-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.1;
}

.page-title span {
    color: #fc6100;
}

.page-subtitle {
    font-family: 'Montserrat', sans-serif;
    color: #888888;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

.section-label {
    font-family: 'Poppins', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #fc6100;
    margin-bottom: 0.5rem;
}

.section-heading {
    font-family: 'Poppins', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 1.2rem 0;
}

.color-card {
    background: #0d0d0d;
    border: 1px solid #1c1c1c;
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
    transition: border-color 0.2s;
}

.color-swatch {
    width: 100%;
    height: 80px;
    border-radius: 7px;
    margin-bottom: 0.7rem;
    border: 1px solid rgba(255,255,255,0.06);
}

.color-hex {
    font-family: 'Poppins', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
    display: block;
    margin-bottom: 0.2rem;
}

.color-pct {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.78rem;
    color: #fc6100;
    font-weight: 500;
    display: block;
    margin-bottom: 0.2rem;
}

.color-rgb {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.7rem;
    color: #555555;
    display: block;
}

[data-testid="stFileUploader"] {
    background: #0a0a0a !important;
    border: 1.5px dashed #2a2a2a !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #fc6100 !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    color: #888888 !important;
    font-family: 'Montserrat', sans-serif !important;
}

[data-testid="stFileUploader"] button {
    background-color: #fc6100 !important;
    color: #000000 !important;
    border: none !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border-radius: 7px !important;
    padding: 0.4rem 1.2rem !important;
}

[data-testid="stFileUploader"] button span {
    display: none !important;
}

[data-testid="stFileUploader"] button::after {
    content: "Upload" !important;
}

[data-testid="stFileUploader"] section {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.5rem !important;
    padding: 1.2rem !important;
}

[data-testid="stFileUploader"] section > div {
    text-align: center !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #0a0a0a !important;
    border: 1.5px dashed #2a2a2a !important;
    border-radius: 12px !important;
    padding: 1.5rem 1rem !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.6rem !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #fc6100 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 0.3rem !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    text-align: center !important;
    display: block !important;
}

.stButton > button {
    background: #fc6100 !important;
    color: #000000 !important;
    border: none !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    border: none !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #fc6100 !important;
    border: 1.5px solid #fc6100 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}

.stDownloadButton > button:hover {
    background: #fc6100 !important;
    color: #000000 !important;
}

.stDataFrame {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
}

.stDataFrame th {
    background: #111111 !important;
    color: #fc6100 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    border-bottom: 1px solid #2a2a2a !important;
}

.stDataFrame td {
    color: #cccccc !important;
    font-family: 'Montserrat', sans-serif !important;
    border-bottom: 1px solid #1a1a1a !important;
}

.stAlert {
    background: #0d0d0d !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 8px !important;
    color: #cccccc !important;
}

.stAlert [data-testid="stAlertContentInfo"] {
    color: #fc6100 !important;
}

.stSuccess {
    background: #0a1a0a !important;
    border-color: #1a3a1a !important;
}

.divider {
    height: 1px;
    background: #1a1a1a;
    margin: 2rem 0;
}

.sidebar-brand {
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff !important;
    margin-bottom: 0.3rem;
}

.sidebar-made {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.7rem;
    color: #444444 !important;
    border-top: 1px solid #1a1a1a;
    padding-top: 0.8rem;
    margin-top: 1rem;
}

.image-container-label {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.78rem;
    color: #555555;
    text-align: center;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <p class="page-title">Color Palette <span>Extractor</span></p>
    <p class="page-subtitle">Dominant color extraction using K-Means Clustering</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<p class="sidebar-brand">About</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; line-height: 1.7;">
    This tool uses <strong style="color:#fc6100;">K-Means Clustering</strong> 
    to find the most dominant colors in an uploaded image, 
    with interactive visual markers on the result.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    requested_k = st.slider(
        "Target color count",
        min_value=3,
        max_value=10,
        value=7,
        step=1,
        help="Number of dominant colors to extract (auto-adjusted based on image)"
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-made">140810240018 - Jeane</p>', unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    "Upload Image (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    with st.spinner("Processing image..."):
        image_small = image.resize((200, 200))
        img_array = np.array(image_small)
        pixels = img_array.reshape(-1, 3)

        unique_colors = np.unique(pixels, axis=0)
        unique_count = len(unique_colors)

        if requested_k > unique_count:
            st.warning(f"Image has only {unique_count} unique colors. K adjusted from {requested_k} to {unique_count}.")
            K = unique_count
        else:
            K = requested_k

        if K < 3:
            st.info(f"Image has only {K} unique colors. Displaying all.")
            colors = unique_colors
            percentages = np.ones(len(colors)) / len(colors) * 100
        else:
            kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
            kmeans.fit(pixels)
            colors = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            label_counts = np.bincount(labels)
            percentages = (label_counts / len(labels)) * 100

        sorted_indices = np.argsort(percentages)[::-1]
        colors = colors[sorted_indices]
        percentages = percentages[sorted_indices]
        final_k = len(colors)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_img, col_palette = st.columns([3, 2], gap="large")

    with col_img:
        st.markdown('<p class="section-label">Source Image</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-heading">Uploaded Image with Color Markers</p>', unsafe_allow_html=True)

        img_w, img_h = image.size
        scale_w = 600
        scale_h = int(img_h * scale_w / img_w)
        image_display = image.resize((scale_w, scale_h))
        img_array_full = np.array(image_display)

        fig_img, ax_img = plt.subplots(figsize=(8, scale_h / 75))
        fig_img.patch.set_facecolor('#000000')
        ax_img.set_facecolor('#000000')
        ax_img.imshow(img_array_full)
        ax_img.axis('off')

        np.random.seed(42)
        margin_x = scale_w * 0.12
        margin_y = scale_h * 0.12
        used_positions = []

        for i in range(final_k):
            color_rgb = colors[i] / 255.0
            attempts = 0
            while attempts < 60:
                rx = np.random.uniform(margin_x, scale_w - margin_x)
                ry = np.random.uniform(margin_y, scale_h - margin_y)
                too_close = False
                for px, py in used_positions:
                    dist = np.sqrt((rx - px)**2 + (ry - py)**2)
                    if dist < scale_w * 0.14:
                        too_close = True
                        break
                if not too_close:
                    used_positions.append((rx, ry))
                    break
                attempts += 1
            else:
                used_positions.append((rx, ry))

            norm_x = rx / scale_w
            norm_y = ry / scale_h

            circle_bg = plt.Circle(
                (norm_x, norm_y),
                0.045,
                color='white',
                linewidth=0,
                transform=ax_img.transAxes,
                zorder=5
            )
            ax_img.add_patch(circle_bg)

            circle_color = plt.Circle(
                (norm_x, norm_y),
                0.038,
                color=color_rgb,
                linewidth=0,
                transform=ax_img.transAxes,
                zorder=6
            )
            ax_img.add_patch(circle_color)

            ring = plt.Circle(
                (norm_x, norm_y),
                0.045,
                fill=False,
                edgecolor='white',
                linewidth=1.5,
                transform=ax_img.transAxes,
                zorder=7
            )
            ax_img.add_patch(ring)

            hex_str = "#{:02X}{:02X}{:02X}".format(colors[i][0], colors[i][1], colors[i][2])
            brightness = 0.299 * colors[i][0] + 0.587 * colors[i][1] + 0.114 * colors[i][2]
            text_color = 'white' if brightness < 128 else 'black'

            ax_img.text(
                norm_x, norm_y,
                str(i + 1),
                ha='center', va='center',
                fontsize=7.5,
                fontweight='bold',
                color=text_color,
                transform=ax_img.transAxes,
                zorder=8
            )

        plt.tight_layout(pad=0)
        st.pyplot(fig_img, use_container_width=True)
        st.markdown('<p class="image-container-label">Circles mark the dominant color zones identified by K-Means</p>', unsafe_allow_html=True)

    with col_palette:
        st.markdown('<p class="section-label">Extracted Colors</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="section-heading">{final_k} Dominant Colors</p>', unsafe_allow_html=True)

        for i in range(final_k):
            hex_color = "#{:02X}{:02X}{:02X}".format(colors[i][0], colors[i][1], colors[i][2])
            st.markdown(f"""
            <div class="color-card" style="margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.8rem; text-align: left; padding: 0.7rem 0.9rem;">
                <div style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%; background: {hex_color}; border: 2px solid rgba(255,255,255,0.15); flex-shrink: 0;">
                    <span style="font-family: Poppins, sans-serif; font-size: 0.75rem; font-weight: 700; color: {'#000' if (0.299*colors[i][0]+0.587*colors[i][1]+0.114*colors[i][2]) > 128 else '#fff'};">{i+1}</span>
                </div>
                <div style="flex: 1;">
                    <span class="color-hex">{hex_color}</span>
                    <span style="font-family: Montserrat; font-size: 0.72rem; color: #555; display: block;">RGB({colors[i][0]}, {colors[i][1]}, {colors[i][2]})</span>
                </div>
                <div style="text-align: right;">
                    <span class="color-pct">{percentages[i]:.1f}%</span>
                    <div style="width: 60px; height: 5px; background: #1a1a1a; border-radius: 3px; overflow: hidden;">
                        <div style="width: {percentages[i]:.1f}%; height: 100%; background: #fc6100; border-radius: 3px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Color Distribution Chart</p>', unsafe_allow_html=True)

    fig_height = max(3.5, final_k * 0.5)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#0a0a0a')

    y_pos = np.arange(final_k)
    color_rgb_list = [np.array(c) / 255 for c in colors]

    bars = ax.barh(y_pos, percentages, color=color_rgb_list, height=0.55, edgecolor='none')

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(
        [f"Color {i+1}" for i in range(final_k)],
        color='#888888',
        fontsize=10,
        fontfamily='monospace'
    )
    ax.set_xlabel("Percentage (%)", color='#444444', fontsize=9)
    ax.tick_params(axis='x', colors='#333333', labelsize=8)
    ax.tick_params(axis='y', length=0)
    ax.invert_yaxis()
    ax.xaxis.grid(True, color='#1a1a1a', linewidth=0.5, linestyle='--')
    ax.set_axisbelow(True)

    for i, p in enumerate(percentages):
        hex_str = "#{:02X}{:02X}{:02X}".format(colors[i][0], colors[i][1], colors[i][2])
        ax.text(p + 0.4, i, f"{p:.1f}%  {hex_str}", va='center', color='#cccccc', fontsize=8.5, fontweight='bold')

    plt.tight_layout(pad=1)
    st.pyplot(fig)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Palette</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Proportional Color Palette</p>', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(10, 1.2))
    fig2.patch.set_facecolor('#000000')
    ax2.set_facecolor('#000000')

    left = 0
    for i, color in enumerate(colors):
        width = percentages[i] / 100
        ax2.add_patch(patches.FancyBboxPatch(
            (left, 0.05), width, 0.9,
            boxstyle="square,pad=0",
            facecolor=np.array(color) / 255,
            edgecolor='#000000',
            linewidth=1.5
        ))
        left += width

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig2)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Data</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Color Detail Table</p>', unsafe_allow_html=True)

    df = pd.DataFrame({
        'No': [i + 1 for i in range(final_k)],
        'HEX': [f"#{colors[i][0]:02X}{colors[i][1]:02X}{colors[i][2]:02X}" for i in range(final_k)],
        'R': [int(colors[i][0]) for i in range(final_k)],
        'G': [int(colors[i][1]) for i in range(final_k)],
        'B': [int(colors[i][2]) for i in range(final_k)],
        'Percentage': [f"{percentages[i]:.1f}%" for i in range(final_k)]
    })
    st.dataframe(df, hide_index=True, use_container_width=True)

    csv = df.to_csv(index=False)
    col_dl, _ = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "Download Color Palette (CSV)",
            csv,
            "color_palette.csv",
            "text/csv"
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.success(f"Successfully extracted {final_k} dominant colors.")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Method</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Method Information</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 10px; padding: 1.5rem;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem;">Algorithm</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; margin-bottom: 1rem;">K-Means Clustering</p>
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem;">Distance Metric</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; margin-bottom: 1rem;">Euclidean Distance</p>
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem;">Unique Colors in Image</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; margin: 0;">{unique_count}</p>
            </div>
            <div>
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem;">Requested K</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; margin-bottom: 1rem;">{requested_k}</p>
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 700; color: #ffffff; margin-bottom: 0.3rem;">Applied K</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; margin-bottom: 1rem;">{final_k}</p>
            </div>
        </div>
        <p style="font-family: Montserrat, sans-serif; font-size: 0.75rem; color: #444444; margin: 1rem 0 0 0; padding-top: 1rem; border-top: 1px solid #1a1a1a;">
            If the number of unique colors is less than the requested K, K is automatically adjusted.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    col_info, _ = st.columns([2, 1])
    with col_info:
        st.markdown("""
        <div style="background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 12px; padding: 2rem;">
            <p style="font-family: Poppins, sans-serif; font-size: 1rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem;">How to use</p>
            <ol style="font-family: Montserrat, sans-serif; font-size: 0.85rem; color: #888888; line-height: 2; padding-left: 1.2rem; margin: 0;">
                <li>Upload an image (JPG, PNG, JPEG) using the uploader above</li>
                <li>Set the target number of colors in the sidebar (3–10)</li>
                <li>View dominant colors marked with circles on the image</li>
                <li>Explore the distribution chart, proportional palette, and data table</li>
                <li>Download the palette as a CSV file</li>
            </ol>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #1a1a1a;">
                <p style="font-family: Poppins, sans-serif; font-size: 0.78rem; font-weight: 600; color: #fc6100; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.5rem;">Tips</p>
                <p style="font-family: Montserrat, sans-serif; font-size: 0.82rem; color: #555555; line-height: 1.7; margin: 0;">
                    Use images with varied colors for best results. Simple images like logos may yield fewer colors than requested — K is automatically adjusted.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)