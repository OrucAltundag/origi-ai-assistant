# origi-ai-assistant

Yerel öncelikli kişisel yapay zekâ asistanı MVP'si.

## Özellikler (MVP)
- Not oluşturma, listeleme, güncelleme, silme
- Görev oluşturma, listeleme, tamamlama, silme
- Temel doğal dil komut çözümleme (`/api/commands`)
- SQLite tabanlı yerel veri saklama
- Eylem loglama
- Hassas silme işlemleri için onay (`confirm=true`)
- Basit web arayüzü

## Çalıştırma
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Uygulama: `http://127.0.0.1:8000`
