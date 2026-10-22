# Art Suzani Hotel — 20 soniyalik reklama video

Vertikal (1080×1920, 30 fps) motion-animatsion video: Instagram Reels, TikTok,
YouTube Shorts va Telegram uchun.

| Fayl | Nima |
|---|---|
| `out/art-suzani-hotel-20s-uz.mp4` | O‘zbekcha versiya (musiqa bilan) |
| `out/art-suzani-hotel-20s-en.mp4` | Inglizcha versiya — chet ellik sayyohlar uchun |
| `out/cover-uz.jpg`, `out/cover-en.jpg` | Post uchun muqova (cover) rasmi |

## Sahnalar

| Vaqt | Sahna |
|---|---|
| 0–4 s | Suzani naqshi ochiladi — “Ming yillik tarix qalbidagi uyingiz” |
| 4–8 s | Quyosh botishida Buxoro: Kalon minorasi, gumbazlar — “Kalon minorasidan bir necha qadam” |
| 8–12.5 s | Arka orqali milliy uslubdagi xonaga kirish + qulayliklar (bog‘, nonushta, Wi‑Fi, transfer) |
| 12.5–16 s | Mehmonlar bahosi 9.3 / 10, yulduzlar |
| 16–20 s | ART SUZANI logotipi, “Hozir bron qiling”, Google Maps |

Musiqa `music.py` da noldan yaratilgan (doira + torli cholg‘u ohangi), shuning
uchun mualliflik huquqi muammosi yo‘q.

## O‘z rasmlaringizni qo‘shish

Mehmonxonaning **o‘zingizga tegishli** rasmlarini (Google Maps’dagi “Owner”
rasmlari yoki o‘zingiz olgan suratlar) `photos/1.jpg`, `photos/2.jpg`,
`photos/3.jpg` deb qo‘ying — xona sahnasida chizilgan interyer o‘rniga ular
chiqadi. Keyin qayta render qiling:

```bash
npm install
python3 music.py
node render.mjs uz && node render.mjs en
for l in uz en; do
  ffmpeg -y -i out/video-$l.mp4 -i out/music.wav -c:v libx264 -preset slow -crf 23 \
    -pix_fmt yuv420p -c:a aac -b:a 192k -af loudnorm=I=-14:TP=-1.5 -shortest \
    -movflags +faststart out/art-suzani-hotel-20s-$l.mp4
done
```

Brauzerda `index.html` ni ochsangiz jonli ko‘rinishni ko‘rasiz (`?lang=en` — inglizcha).
Matnlar `index.html` ichidagi `T` obyektida — o‘zgartirish oson.

> Eslatma: Google Maps’dagi boshqa mehmonlar yuklagan rasmlar ularning
> mualliflik huquqiga tegishli — reklamada faqat o‘zingizning rasmlaringizdan
> foydalaning. Reyting (9.3/10) va manzil (Xaqiqat ko‘chasi, 9) booking
> saytlaridan olingan — post qilishdan oldin tekshiring.

## Post matni (tayyor)

**Instagram / Telegram (UZ):**

> Buxoroning qoq markazida, Kalon minorasidan bir necha qadamda — milliy ruhdagi
> shinam uy ✨
> 🌿 Bog‘ va terrasa · ☕ Nonushta · 📶 Bepul Wi‑Fi · 🚐 Aeroport transferi
> 📍 Google Maps: “Art Suzani Hotel”
> 📩 Bron uchun: Direct / WhatsApp / Telegram
>
> #Buxoro #Bukhara #ArtSuzani #BukharaHotel #Uzbekistan #VisitUzbekistan #Suzani #Mehmonxona

**Instagram (EN):**

> Wake up steps away from the Kalon Minaret 🕌 Cosy rooms in authentic Uzbek style,
> a garden terrace and breakfast every morning. Find “Art Suzani Hotel” on Google Maps.
> DM us to book ✨
>
> #Bukhara #Uzbekistan #VisitUzbekistan #SilkRoad #BukharaHotel #TravelUzbekistan #BoutiqueHotel

## Tashrif buyuruvchilarni oshirish uchun maslahatlar

Video yolg‘iz o‘zi natijani kafolatlamaydi — lekin quyidagilar bilan birga ishlatsangiz
samarasi ancha yuqori bo‘ladi:

1. **Ikki tilda post qiling.** Buxoroga keladiganlarning katta qismi chet elliklar —
   inglizcha versiyani Instagram, TikTok va Google Business profilingizga qo‘ying.
2. **Google Business Profile’ga videoni yuklang** (Google Maps’dagi sahifangiz).
   Odamlar mehmonxonani aynan shu yerda tanlaydi; yangi rasm/video ko‘rinishni oshiradi.
3. **Pullik reklama:** Instagram/Facebook’da 5–7 kun, kuniga $5–10,
   auditoriya: Buxoro/Samarqandga qiziquvchi sayyohlar (Yevropa, Rossiya, Turkiya, Koreya).
4. **Har bir sharhga javob bering** va mamnun mehmonlardan Google’da sharh qoldirishni
   so‘rang — reyting va sharhlar soni bron qarorini eng ko‘p belgilaydi.
5. **Bron tugmasini oson qiling:** Instagram bio’ga WhatsApp / Booking havolasini qo‘ying.
6. **Natijani o‘lchang:** post qilishdan oldingi va keyingi 2–4 hafta Google Business
   statistikasini (qo‘ng‘iroqlar, yo‘nalish so‘rovlari, sayt bosishlar) solishtiring.
