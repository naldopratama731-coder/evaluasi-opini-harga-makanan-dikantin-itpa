import streamlit as st
import re

custom_dict = {
    "harga murah": 5, "murah": 5, "cukup murah": 4,
    "harga sedang": 3, "standar": 3, "normal": 3,
    "harga mahal": 1, "mahal": 1, "agak mahal": 2,
    "terlalu mahal": 1, "kemahalan": 1,
}

rating_category = {
    5: "Sangat Memuaskan",
    4: "Memuaskan",
    3: "Cukup Baik",
    2: "Perlu Evaluasi",
    1: "Banyak Keluhan",
}

solution_suggestion = {
    5: "Pertahankan kualitas dan harga.",
    4: "Tingkatkan variasi menu.",
    3: "Perlu evaluasi berkala.",
    2: "Pertimbangkan penyesuaian harga.",
    1: "Segera evaluasi harga.",
}

if "counter" not in st.session_state:
    st.session_state.counter = {v: 0 for v in rating_category.values()}

def analyze_food(text):
    score, count = 0, 0
    text = text.lower()
    for key, val in custom_dict.items():
        if key in text:
            score += val
            count += 1
    if count == 0:
        return None
    return round(max(1, min(5, score / count)))

st.set_page_config(page_title="Evaluasi Harga Kantin")

st.title("📊 Evaluasi Opini Harga Makanan")
st.write("Aplikasi Web Online (Tanpa Install)")

text = st.text_area(
    "Masukkan opini mahasiswa:",
    placeholder="Contoh: harga makanan cukup murah tapi porsinya kecil"
)

if st.button("🔍 Proses"):
    if not text.strip():
        st.warning("Masukkan opini terlebih dahulu.")
    else:
        rating = analyze_food(text)
        if rating is None:
            st.info("Kata harga tidak ditemukan.")
        else:
            cat = rating_category[rating]
            st.session_state.counter[cat] += 1
            st.success("Opini berhasil dianalisis")
            st.write(f"*Rating:* {rating}")
            st.write(f"*Kategori:* {cat}")
            st.write(f"*Saran:* {solution_suggestion[rating]}")

st.subheader("📈 Rekapitulasi Opini")
st.bar_chart(st.session_state.counter)
