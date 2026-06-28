import os
import time
from flask import Flask, render_template_string

app = Flask(__name__)

# Serverə gələn ümumi sorğu sayğacı
sorqu_saygaci = 0

# HTML, CSS və Dizayn daxildə (Render-də asan işləməsi üçün)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyber MBTI & DDoS Test Lab</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        body { background-color: #0d0e15; color: #e2e8f0; }
    </style>
</head>
<body class="font-sans antialiased">

    <nav class="border-b border-purple-900/40 bg-slate-900/50 p-4 backdrop-blur">
        <div class="container mx-auto flex items-center justify-between">
            <span class="text-xl font-bold text-purple-500 tracking-wider">⚡ CYBER-LAB</span>
            <span class="rounded bg-purple-900/50 px-3 py-1 text-xs text-purple-300 border border-purple-500/30">Render Free Plan</span>
        </div>
    </nav>

    <div class="container mx-auto max-w-4xl px-4 py-8">
        
        <header class="text-center my-10">
            <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500 mb-4">
                DDoS Test və MBTI İnformasiya Portalı
            </h1>
            <p class="text-slate-400 max-w-xl mx-auto">
                Bu sayt tam qorunmasız struktura malikdir və şəxsi yükləmə (stress) testləriniz üçün dizayn edilmişdir.
            </p>
        </header>

        <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 text-center mb-8 shadow-xl backdrop-blur">
            <h2 class="text-lg font-semibold mb-3 text-purple-300">Sistem Yoxlanışı</h2>
            <button onclick="alert('⚠️ DİQQƏT: Bu veb-sayt xüsusi olaraq DoS/DDoS stress testləri üçün qorunmasız qurulmuşdur!');" 
                    class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg shadow-purple-500/20 transition-all duration-300 transform hover:scale-105 cursor-pointer text-sm">
                Sistem Məqsədini Öyrən 🎯
            </button>
            <div class="mt-4 text-xs text-slate-500">
                Toplam qəbul edilən HTTP sorğusu: <span class="text-pink-500 font-mono font-bold">{{ saygac }}</span>
            </div>
        </div>

        <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6">
                <h3 class="text-xl font-bold text-pink-400 mb-3 flex items-center gap-2">
                    🛑 DDoS Nədir?
                </h3>
                <p class="text-sm text-slate-400 leading-relaxed mb-4">
                    <strong>DDoS (Distributed Denial of Service)</strong> — hədəf serverin və ya şəbəkənin normal trafikini iflic etmək üçün minlərlə fərqli qaynaqdan eyni anda edilən süni sorğu hücumudur. Server gələn saxta sorğuları emal etməyə çalışarkən həddindən artıq yüklənir (CPU/RAM bitir) və real istifadəçilərə xidmət göstərə bilmir.
                </p>
                <div class="bg-slate-950 p-3 rounded-lg border border-red-900/30 text-xs font-mono text-red-400">
                    // Bu server tək nüvəlidir (threaded=False). Saniyədə 100+ sorğu gəldikdə "502 Bad Gateway" verəcək.
                </div>
            </div>

            <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6">
                <h3 class="text-xl font-bold text-purple-400 mb-3 flex items-center gap-2">
                    🧠 MBTI Şəxsiyyət Tipləri (Böyük Data)
                </h3>
                <p class="text-xs text-slate-400 mb-4">
                    Hücum zamanı trafikin (MB) daha tez artması üçün aşağıya bütün MBTI tiplərinin geniş xarakteristikası əlavə edilib:
                </p>
                
                <div class="space-y-3 max-h-60 overflow-y-auto pr-2 text-xs text-slate-400 custom-scrollbar">
                    <p><strong>INTJ (Strateq):</strong> Analitik təfəkkürlü, hər şeyin arxasındakı məntiqi axtaran, uzunmüddətli planlar quran şəxslər.</p>
                    <p><strong>INTP (Məntiqçi):</strong> Yenilikçi ixtiraçılar, nəzəriyyələrə və sistemlərin necə işlədiyinə maraq göstərən kiber-beyinlər.</p>
                    <p><strong>ENTJ (Komandir):</strong> Cəsarətli, iradəli və hər zaman bir çıxış yolu tapan və ya özü yeni bir yol açan liderlər.</p>
                    <p><strong>ENTP (Mübahisəçi):</strong> İntellektual çağırışları sevən, qaydaları test etməkdən həzz alan strateqlər.</p>
                    <p><strong>INFJ (Vəkil):</strong> Müəmmalı, lakin insanları ruhlandıran, idealist və daxili dünyası çox zəngin olan şəxsiyyətlər.</p>
                    <p><strong>INFP (Vasitəçi):</strong> Şeirsel, xeyirxah və altruist, hər zaman yaxşı bir işə kömək etməyə can atan romantiklər.</p>
                    <p><strong>ENFJ (Protaqonist):</strong> Karizmatik və ilhamverici liderlər, dinləyicilərini maqnit kimi özünə çəkən şəxslər.</p>
                    <p><strong>ENFP (Kampaniyaçı):</strong> Həvəsli, yaradıcı və sosial azadlığı sevən, hər vəziyyətdə təbəssüm tapmağı bacaranlar.</p>
                    <p><strong>ISTJ (Logist):</strong> Praktiki və faktlara əsaslanan, etibarlılığı şübhə doğurmayan ciddi nizam-intizam adamları.</p>
                    <p><strong>ISFJ (Müdafiəçi):</strong> Çox isti və fədakar qoruyucular, sevdiklərini hər zaman müdafiə etməyə hazır olanlar.</p>
                    <p><strong>ESTJ (İcraçı):</strong> İnsanları və ya işləri idarə etməkdə bənzərsiz olan mükəmməl administratorlar.</p>
                    <p><strong>ESFJ (Konsul):</strong> Həddindən artıq qayğıkeş, sosial və populyar, hər zaman kömək etməyə hazır olan insanlar.</p>
                </div>
            </div>
        </div>

        <footer class="text-center mt-12 text-xs text-slate-600 border-t border-slate-900 pt-6">
            Cyber MBTI Lab &copy; 2026 — Sınaq Məqsədlidir.
        </footer>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    global sorqu_saygaci
    sorqu_saygaci += 1
    
    # 🚨 DDoS Testi üçün qəsdən yaradılan zəiflik:
    # Hər gələn sorğuda serveri 0.05 saniyə dincəldirik ki, parallel gələn sorğularda kilidlənsin.
    time.sleep(0.05)
    
    return render_template_string(HTML_TEMPLATE, saygac=sorqu_saygaci)

if __name__ == "__main__":
    # Render-in təyin etdiyi portu avtomatik götürür
    port = int(os.environ.get("PORT", 8080))
    # Serveri tək-işçi rejimində işlədirik (Qorumasız olması üçün threaded=False)
    app.run(host='0.0.0.0', port=port, threaded=False)
  
