import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.models import AIAnalysis

load_dotenv()

async def analyze_book_with_ai(metadata: dict, screenshot_base64: str) -> AIAnalysis:
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY tidak ditemukan di .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        temperature=0.0, 
        max_retries=2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    system_prompt = """
    PERAN: Anda adalah Auditor Ahli Perjenjangan Buku Kemendikbud (SK 030/P/2022).
    TUGAS: Analisis metadata buku dan screenshot halaman untuk menentukan 'Jenjang Pembaca' (A, B1, B2, B3, C, D, E) dengan presisi tinggi.

    PEDOMAN KLASIFIKASI MENDETAIL (STRICT RULES):

    1. [cite_start]JENJANG A (Pembaca Dini) -> Simbol: MERAH [cite: 236, 237, 240, 243, 245]
       - Target: PAUD (0-7 thn).
       - Fisik: 8-24 halaman. Font min 24pt.
       - [cite_start]Teks: HANYA kata, frasa, klausa, atau KALIMAT TUNGGAL sederhana. [cite: 243]
       - Panjang Kalimat: Maksimal 5 kata/kalimat. [cite_start]Maksimal 3 kalimat/halaman. [cite: 245]
       - [cite_start]Paragraf: BELUM ADA paragraf. [cite: 321]
       - Visual: Gambar SANGAT DOMINAN. [cite_start]Tanpa balon dialog. [cite: 245]
       - Diksi: Kata dasar & bentukan umum. [cite_start]Kosakata sangat akrab (familiar). [cite: 240]

    2. [cite_start]JENJANG B (Pembaca Awal) -> Simbol: UNGU [cite: 249, 253, 257, 261, 265]
       - Target: SD Kelas 1-3. Butuh perancah (scaffolding).
       - Sub-Jenjang B1:
         * Fisik: 16-32 hal. Font min 20pt.
         * Teks: Maks 7 kata/kalimat. [cite_start]Maks 5 kalimat/halaman. [cite: 253]
         * Struktur: Kalimat tunggal & majemuk setara sederhana. [cite_start]Belum ada paragraf. [cite: 253]
         * Visual: Gambar dominan. [cite_start]Tanpa balon dialog. [cite: 253]
       - Sub-Jenjang B2:
         * Fisik: 24-48 hal. Font min 18pt.
         * Teks: Maks 9 kata/kalimat. [cite_start]Maks 7 kalimat/halaman. [cite: 261, 263]
         * [cite_start]Struktur: Kalimat tunggal & majemuk setara. [cite: 261]
         * Visual: Gambar dominan. Tanpa balon dialog.
       - Sub-Jenjang B3:
         * Fisik: 32-48 hal. Font min 16pt.
         * [cite_start]Teks: Maks 12 kata/kalimat. [cite: 271]
         * [cite_start]Struktur Paragraf: MULAI ADA PARAGRAF SEDERHANA (Maks 3 paragraf/halaman, tiap paragraf maks 3 kalimat). [cite: 271, 321]
         * Visual: Proporsi gambar seimbang/lebih kecil dari teks. [cite_start]Tanpa balon dialog. [cite: 271]

    3. [cite_start]JENJANG C (Pembaca Semenjana) -> Simbol: BIRU [cite: 275, 280, 282]
       - Target: SD Kelas 4-6.
       - Struktur Paragraf: SUDAH BERBENTUK PARAGRAF PENUH (Narasi/Deskripsi). [cite_start]Maks 4 paragraf/halaman. [cite: 280]
       - Struktur Bahasa: Variasi kalimat tunggal & majemuk. [cite_start]Variasi paragraf (Deduktif/Induktif). [cite: 280]
       - Jenis Buku: Cerita rakyat, Biografi pendek, Komik (BOLEH ada balon dialog).
       - [cite_start]Diksi: Kata umum (>300 kata) & kata khusus materi. [cite: 277]

    4. [cite_start]JENJANG D (Pembaca Madya) -> Simbol: HIJAU [cite: 285, 286, 289]
       - Target: SMP (13-15 thn). Halaman > 48.
       - [cite_start]Jenis Buku: Antologi (Puisi/Drama/Cerpen), Novel Remaja, Komik, Kamus, Ensiklopedia, Buku How-to. [cite: 286]
       - Struktur Bahasa (KOMPLEKS): 
         * [cite_start]Menggunakan variasi paragraf: Deduktif, Induktif, Ineraktif, Campuran, Naratif. [cite: 289]
         * [cite_start]Penyajian: Narasi, Deskripsi, Eksposisi, Argumentasi, dan Persuasi. [cite: 289]
         * [cite_start]Kalimat: Menggunakan variasi kalimat tunggal, majemuk setara, dan majemuk bertingkat. [cite: 323]
       - Diksi: Kata serapan bahasa asing/daerah. [cite_start]Istilah teknis yang lebih kompleks (>600 kata). [cite: 286]

    5. [cite_start]JENJANG E (Pembaca Mahir) -> Simbol: KUNING [cite: 292, 293, 296]
       - Target: SMA/Dewasa (16+ thn).
       - [cite_start]Jenis Buku: Sastra Kanon, Karya Ilmiah, Antologi Sastra, Novel Kompleks, Buku Referensi Lanjut, Kamus, Ensiklopedia. [cite: 293]
       - Struktur Bahasa (SANGAT KOMPLEKS):
         * [cite_start]Sifat Teks: Analitis, kritis, dan sintesis pemikiran. [cite: 43]
         * [cite_start]Variasi Paragraf: Deduktif, Induktif, Ineraktif, Campuran dengan penyajian Argumentasi & Persuasi yang mendalam. [cite: 296]
       - Diksi: 
         * [cite_start]Kata khusus bidang keilmuan (Sains/Filosofi/Teknis). [cite: 293]
         * [cite_start]Termasuk penggunaan kata serapan dan kata asing (bahasa daerah/bahasa asing). [cite: 293]
         * [cite_start]Memuat >900 kosakata. [cite: 293]

    INSTRUKSI ANALISIS LOGIS (STEP-BY-STEP):
    1. IDENTIFIKASI JENIS BUKU: Apakah ini buku bantal (A), Novel (D/E), atau Sastra Kanon (E)?
    2. ANALISIS STRUKTUR PARAGRAF:
       - Tidak ada paragraf? -> A, B1, B2.
       - Paragraf Narasi sederhana? -> B3, C.
       - Paragraf Argumentasi/Persuasi/Deduktif/Induktif? -> D atau E.
    3. ANALISIS DIKSI & BAHASA:
       - Apakah ada istilah teknis/ilmiah ("metabolisme", "paradigma", "inflasi")? -> E.
       - Apakah ada kata serapan asing/daerah ("gadget", "reshuffle")? -> D.
       - Apakah kalimatnya majemuk bertingkat panjang? -> D atau E.
    4. CEK VISUAL:
       - Balon dialog? -> C (Komik) atau D. Dilarang di A/B.

    FORMAT OUTPUT (WAJIB JSON):
    {
        "jenjang": "Jenjang X - Nama Jenjang", 
        "confidence_score": 0-100,
        "alasan": "Jelaskan analisis teknis: Rata-rata panjang kalimat X kata. Struktur kalimat (Tunggal/Majemuk). Jenis paragraf (Deduktif/Induktif/dll). Proporsi gambar vs teks.",
        "saran": "Saran pendampingan spesifik (misal: Perancah penuh / Mandiri).",
        "badge_color": "WARNA (MERAH/UNGU/BIRU/HIJAU/KUNING)"
    }
    """

    metadata_info = f"""
    Data Buku:
    - Judul: {metadata['title']}
    - Jumlah Halaman: {metadata.get('page_count', 'Tidak diketahui')}
    - Kategori: {metadata.get('categories', [])}
    """
    content_message = [
        {"type": "text", "text": system_prompt},
        {"type": "text", "text": metadata_info}
    ]

    if screenshot_base64:
        content_message.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}
        })
    else:
        content_message.append({"type": "text", "text": "[PERINGATAN: Screenshot tidak tersedia. Analisis hanya berdasarkan Metadata.]"})

    message = HumanMessage(content=content_message)

    try:
        response = await llm.ainvoke([message])
        
        clean_content = response.content.replace("```json", "").replace("```", "").strip()
        result_json = json.loads(clean_content)
        
        return AIAnalysis(**result_json)
        
    except Exception as e:
        print(f"Error AI: {e}")
        return AIAnalysis(
            jenjang="Tidak Teridentifikasi",
            confidence_score=0,
            alasan=f"Gagal analisis AI: {str(e)}",
            saran="-",
            badge_color="ABU"
        )