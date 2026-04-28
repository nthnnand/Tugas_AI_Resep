import streamlit as st
import os
import urllib.parse
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY_GROQ = os.getenv("GROQ_API_KEY")

st.title("AI Chef: Resep Sisa Kulkas")
st.write("Punya bahan sisa di kulkas tapi bingung mau dimasak apa? Tinggal masukin aja bahan-bahannya, nanti dicariin resep yang pas sekalian sama gambar masakannya.")

bahan_input = st.text_input("Bahan yang ada (pisahkan dengan koma):", placeholder="Contoh: Telur, Nasi, Sosis")

if st.button("Buat Resep!"):
    if bahan_input == "":
        st.warning("Isi dulu dong bahannya, jangan dikosongin.")
    else:
        pesan_tunggu = st.info("Lagi mikirin resep sama bikin gambarnya, tunggu bentar ya...")
        
        try:
            # Build the prompt for the AI and get the recipe
            client = Groq(api_key=API_KEY_GROQ)
            prompt_koki = (
                "Anda adalah koki rumahan yang jago masak. "
                f"Saya cuma punya bahan ini: {bahan_input}. "
                "Bikinin 1 resep masakan yang gampang dibuat. "
                "Format harus begini: "
                "Nama masakan di baris pertama. "
                "Lalu bagian 'Bahan', 'Peralatan' (singkat), dan 'Langkah memasak' yang detail dan step-by-step, "
                "pakai nomor 1, 2, 3. "
                "Jelasin juga cara masaknya (api kecil/sedang/besar, waktu kira-kira, kapan dibalik/diangkat). "
                "Pake bahasa Indonesia yang santai dan natural, jangan pake emoji, jangan pake tanda strip panjang."
            )
            
            respon_ai = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_koki}],
                model="llama-3.1-8b-instant",
            )
            
            # Create the image prompt and URL
            teks_resep = respon_ai.choices[0].message.content
            prompt_gambar = f"Delicious cooked food made with {bahan_input}, aesthetic food photography, high resolution"
            prompt_aman = urllib.parse.quote(prompt_gambar)
            url_gambar = f"https://image.pollinations.ai/prompt/{prompt_aman}?width=720&height=480&nologo=true"

            pesan_tunggu.empty()
            st.success("Nih resepnya udah jadi, cek di bawah ya.")
            
            # Fetch the image server-side to avoid client-side image load errors.
            response = requests.get(url_gambar, timeout=20)
            response.raise_for_status()
            st.image(response.content, caption=f"Kira-kira tampilannya kayak gini kalau dimasak dari: {bahan_input}")
            
            st.write(teks_resep)

        except Exception as e:
            st.error(f"Ada yang error nih, coba lagi nanti ya. Detail: {e}")