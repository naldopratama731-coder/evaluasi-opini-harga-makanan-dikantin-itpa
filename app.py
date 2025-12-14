import streamlit as st
import re
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# =============================
# DATA KAMUS PENILAIAN
# =============================
custom_dict = {
    "harga murah": 5,
    "murah": 5,
    "cukup murah": 4,
    "harga sedang": 3,
    "standar": 3,
    "normal": 3,
    "harga mahal": 1,
    "mahal": 1,
    "agak mahal": 2,
    "terlalu mahal": 1,
    "kemahalan": 1,
    "makanan enak": 5,
    "porsi banyak": 4,
    "porsi sedikit": 1,
    "tidak enak": 1,
}

rating_category = {
    5: "Sangat Memuaskan",
    4: "Memuaskan",
    3: "Cukup Baik",
    2: "Perlu Evaluasi",
    1: "Banyak Keluhan",
}

solution_suggestion = {
    5: "Kualitas dan harga sangat baik. Pertahankan standar.",
    4: "Harga cukup baik. Variasi menu bisa ditingkatkan.",
    3: "Harga standar. Evaluasi berkala diperlukan.",
    2: "Pertimbangkan menurunkan harga atau menambah porsi.",
    1: "Segera evaluasi harga karena banyak keluhan.",
}

# =============================
# SESSION STATE
# =============================
if "counter" not in st.session_state:
    st.session_state.counter = {v: 0 for v in rating_category.values()}

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =============================
# FUNGSI ANALISIS
# =============================
def analyze_food(text):
    score = 0
    count = 0
    complaints = []

    text = text.lower()

    for key in sorted(custom_dict, key=len, reverse=True):
        matches = re.findall(r"\b" + re.escape(key) + r"\b", text)
        for _ in matches:
            value = custom_dict[key]
            score += value
            count += 1
            if value <= 2:
                complaints.append(key)

    if count == 0:
        return None, None

    rating = round(max(1, min(5, score / count)))
    return rating, complaints

# =============================
# FUNGSI BUAT PDF
# =============================
def create_pdf(result_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    text_obj = c.beginText(40, 800)

    for line in result_text.split("\n"):
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# =============================
# UI STREAMLIT
# =============================
st.set_page_config(
    page_title="Evaluasi Harga Kantin ITPA",
    layout="centered"
)

st.title("📊 Evaluasi Opini Mahasiswa Tentang Harga Makanan di Kantin ITPA")

text = st.text_area("✍ Masukkan Opini Mahasiswa")

# =============================
# PROSES OPINI
# =============================
if st.button("🔍 Proses Opini"):
    if text.strip() == "":
        st.warning("⚠ Silakan masukkan opini terlebih dahulu.")
    else:
        rating, complaints = analyze_food(text)

        if rating is None:
            st.error("❌ Kata yang berhubungan dengan harga tidak ditemukan.")
        else:
            category = rating_category[rating]
            st.session_state.counter[category] += 1

            keluhan_text = ", ".join(complaints) if complaints else "Tidak ada"

            result_text = (
                "HASIL EVALUASI OPINI HARGA MAKANAN DI KANTIN ITPA\n\n"
                f"Rating   : {rating}\n"
                f"Kategori : {category}\n"
                f"Keluhan  : {keluhan_text}\n"
                f"Saran    : {solution_suggestion[rating]}"
            )

            st.session_state.last_result = result_text

            st.success("✅ Hasil Evaluasi")
            st.write(f"*Rating :* {rating}")
            st.write(f"*Kategori :* {category}")
            st.write(f"*Keluhan :* {keluhan_text}")
            st.write(f"*Saran :* {solution_suggestion[rating]}")

# =============================
# DOWNLOAD PDF
# =============================
if st.session_state.last_result:
    pdf_buffer = create_pdf(st.session_state.last_result)

    st.download_button(
        label="⬇ Download PDF Hasil Evaluasi",
        data=pdf_buffer,
        file_name="hasil_evaluasi_kantin_ITPA.pdf",
        mime="application/pdf"
    )

# =============================
# GRAFIK (MUNCUL SETELAH PROSES)
# =============================
if st.session_state.last_result:
    st.subheader("📈 Grafik Kepuasan Harga")

    fig, ax = plt.subplots()
    ax.bar(
        st.session_state.counter.keys(),
        st.session_state.counter.values()
    )
    ax.set_xlabel("Kategori")
    ax.set_ylabel("Jumlah")
    plt.xticks(rotation=20)

    st.pyplot(fig)
