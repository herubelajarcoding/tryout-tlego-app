import json
import time
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP_DIR = Path(__file__).parent
BANK_PATH = APP_DIR / "question_bank.json"

st.set_page_config(
    page_title="Try Out Kompetensi Teknis DJPb",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root{
  --paper:#fbfaf6;
  --paper-2:#f4efe4;
  --ink:#1f2a37;
  --muted:#667085;
  --navy:#17324d;
  --blue:#2f5d8c;
  --gold:#b88a2f;
  --line:#e4dccb;
  --ok:#237a57;
  --warn:#b7791f;
  --bad:#b42318;
}
.stApp { background: linear-gradient(180deg, #fbfaf6 0%, #f7f2e8 100%); color: var(--ink); }
.block-container { padding-top: 1.25rem; padding-bottom: 2.2rem; max-width: 1280px; }
[data-testid="stSidebar"] { background: #fffdf8; border-right: 1px solid var(--line); }
[data-testid="stSidebar"] * { color: var(--ink); }
#MainMenu, footer { visibility: hidden; }
.hero {
  border: 1px solid var(--line);
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(184,138,47,.18), transparent 28%),
    linear-gradient(135deg, #ffffff 0%, #fbf6ea 55%, #f1eadb 100%);
  padding: 26px 30px;
  margin-bottom: 18px;
  box-shadow: 0 14px 35px rgba(31,42,55,.06);
}
.kicker { letter-spacing:.13em; text-transform:uppercase; color: var(--gold); font-weight:800; font-size:.78rem; margin-bottom: 8px; }
.hero h1 { color: var(--navy); margin:0; font-size:2.15rem; line-height:1.08; font-weight:850; }
.hero p { color:var(--muted); margin:.6rem 0 0 0; max-width: 860px; font-size:1rem; }
.card {
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px 18px;
  background:#fffdf9;
  box-shadow: 0 8px 24px rgba(31,42,55,.045);
}
.card h3 { margin-top:0; color: var(--navy); }
.metric-card {
  border:1px solid var(--line);
  border-radius:16px;
  padding:14px 16px;
  background:#fffdf9;
  box-shadow:0 6px 18px rgba(31,42,55,.045);
}
.metric-label {font-size:.77rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; font-weight:750;}
.metric-value {font-size:1.45rem; color:var(--navy); font-weight:850; margin-top:3px;}
.exam-chip { display:inline-block; padding:5px 10px; border-radius:999px; background:#eef4ff; color:#24466a; border:1px solid #d8e4f4; font-size:.78rem; font-weight:750; margin-right:6px; margin-bottom:6px;}
.exam-chip.gold { background:#fff6df; color:#7a5418; border-color:#ead49a; }
.exam-chip.green { background:#eaf8ef; color:#1f6b4b; border-color:#ccebd8; }
.exam-chip.red { background:#fff1f0; color:#b42318; border-color:#ffd4d0; }
.question-box {
  border:1px solid var(--line);
  border-radius:22px;
  padding:22px;
  background:#fffefb;
  box-shadow: 0 10px 30px rgba(31,42,55,.055);
}
.question-title { color:var(--navy); font-size:1.35rem; font-weight:850; margin:.25rem 0 1rem 0; }
.qtext { font-size:1.04rem; line-height:1.6; color:#243044; }
.nav-wrap { border:1px solid var(--line); border-radius:18px; padding:14px; background:#fffdf9; max-height:68vh; overflow:auto; }
.nav-caption { color:var(--muted); font-size:.84rem; margin-bottom:10px; }
.answer-note { color:var(--muted); font-size:.88rem; }
.correct { border-left:5px solid var(--ok); background:#f0fbf5; padding:12px 14px; border-radius:10px; }
.wrong { border-left:5px solid var(--bad); background:#fff3f1; padding:12px 14px; border-radius:10px; }
.neutral { border-left:5px solid #98a2b3; background:#f8fafc; padding:12px 14px; border-radius:10px; }
.option-study { border:1px solid var(--line); border-radius:12px; padding:11px 13px; margin:8px 0; background:#fffdf9; }
.option-study.correct-opt { border-left:5px solid var(--ok); background:#f0fbf5; }
.option-study.user-wrong-opt { border-left:5px solid var(--bad); background:#fff3f1; }
.option-study.other-opt { border-left:5px solid #98a2b3; background:#f8fafc; }
.option-label { font-weight:850; color:var(--navy); }
.option-explain { margin-top:5px; color:#344054; line-height:1.5; font-size:.94rem; }
hr { border-color: var(--line); }
.stButton>button {
  border-radius: 12px !important;
  border: 1px solid #d4c8b1 !important;
  background: #fffdf8 !important;
  color: #223047 !important;
  font-weight: 700 !important;
}
.stButton>button:hover { border-color: var(--gold) !important; color: var(--navy) !important; background:#fff8e8 !important; }

/* Navigation/button readability: prevent two/three digit numbers from wrapping */
.stButton>button {
  white-space: nowrap !important;
  word-break: keep-all !important;
  overflow-wrap: normal !important;
  line-height: 1.1 !important;
}
.stButton>button[kind="primary"] { background: linear-gradient(135deg, #237a57, #2f9b6d) !important; border: 0 !important; color: #fff !important; }
.stButton>button[kind="primary"]:hover { background: linear-gradient(135deg, #1f6b4b, #237a57) !important; color:#fff !important; }
.stRadio > div { gap: .55rem; }
[data-testid="stMetric"] { background:#fffdf9; border:1px solid var(--line); border-radius:16px; padding:12px 14px; box-shadow:0 6px 18px rgba(31,42,55,.045); }
[data-testid="stMetricLabel"] { color:var(--muted); }
[data-testid="stMetricValue"] { color:var(--navy); font-weight:850; }

/* === COLOR CONTRAST FIX ONLY (basis v3 tetap) === */
.stApp,
[data-testid="stAppViewContainer"],
.block-container {
  color: var(--ink) !important;
}

/* Pastikan teks umum pada area terang tetap gelap */
.block-container p,
.block-container span,
.block-container div,
.block-container label,
.block-container li,
.block-container h1,
.block-container h2,
.block-container h3,
.block-container h4,
.block-container h5,
.block-container h6 {
  color: inherit;
}

.hero, .hero *,
.card, .card *,
.metric-card, .metric-card *,
.question-box, .question-box *,
.nav-wrap, .nav-wrap *,
.option-study, .option-study *,
.correct, .correct *,
.wrong, .wrong *,
.neutral, .neutral * {
  color: var(--ink) !important;
}
.hero h1, .card h3, .metric-value, .question-title, .option-label {
  color: var(--navy) !important;
}
.hero p, .answer-note, .nav-caption, .metric-label {
  color: var(--muted) !important;
}

/* Selectbox/dropdown: jangan hitam-on-hitam */
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background-color: #fffdf8 !important;
  border: 1px solid #d4c8b1 !important;
  color: var(--ink) !important;
}
[data-baseweb="select"] *,
[data-testid="stSelectbox"] * {
  color: var(--ink) !important;
  fill: var(--ink) !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
  background: #fffdf8 !important;
  color: var(--ink) !important;
  border: 1px solid #d4c8b1 !important;
}
[role="option"],
[role="option"] *,
[data-baseweb="menu"] * {
  color: var(--ink) !important;
  background-color: #fffdf8 !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"] {
  background-color: #fff3d7 !important;
}

/* Radio dan checkbox: teks opsi harus terbaca */
[data-testid="stRadio"] *,
[data-testid="stCheckbox"] *,
.stRadio *,
.stCheckbox * {
  color: var(--ink) !important;
}
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
  background: transparent !important;
}

/* Tabs */
button[data-baseweb="tab"] {
  color: #5b667a !important;
  background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"]:hover {
  color: var(--bad) !important;
}

/* Expander/pembahasan: header dan body dibuat terang */
[data-testid="stExpander"] {
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  background: #fffefb !important;
  color: var(--ink) !important;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] div,
[data-testid="stExpander"] p,
[data-testid="stExpander"] span {
  background-color: #fffefb !important;
  color: var(--ink) !important;
}
[data-testid="stExpander"] summary {
  border-radius: 12px !important;
}

/* Alert sukses/error/info tetap terbaca */
[data-testid="stAlert"],
[data-testid="stAlert"] * {
  color: var(--ink) !important;
}

/* Text input/number input kalau ada */
input,
textarea {
  background-color: #fffdf8 !important;
  color: var(--ink) !important;
  border-color: #d4c8b1 !important;
}

/* Tombol tetap sesuai intent */
.stButton>button,
.stDownloadButton>button {
  color: #223047 !important;
  background: #fffdf8 !important;
}
.stButton>button[kind="primary"],
.stDownloadButton>button[kind="primary"] {
  color: #ffffff !important;
  background: linear-gradient(135deg, #237a57, #2f9b6d) !important;
}

/* Navigasi soal: tombol terjawab dibuat hijau, tetap kontras */
.nav-answer button {
  background: #e8f7ee !important;
  border-color: #7bc69a !important;
  color: #175c3b !important;
  font-weight: 850 !important;
}
.nav-answer button:hover {
  background: #d5f0df !important;
  border-color: #3d9a64 !important;
  color: #0f442b !important;
}
.nav-current button {
  box-shadow: 0 0 0 3px rgba(47,93,140,.22) !important;
  border-color: #2f5d8c !important;
}
.nav-flag button {
  background: #fff7e6 !important;
  border-color: #e2b24d !important;
  color: #7a5418 !important;
  font-weight: 850 !important;
}
.nav-empty button {
  background: #fffdf8 !important;
  color: #223047 !important;
}


.compact-hero { padding: 22px 28px; margin-bottom: 20px; }
.compact-hero h1 { font-size: 2rem; }

</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Gate login lokal
def login_gate() -> None:
    st.session_state.setdefault("auth_ok", False)
    if st.session_state["auth_ok"]:
        return
    st.markdown("""
    <div class="hero compact-hero">
      <h1>Masuk Try Out Kompetensi Teknis DJPb</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Masukkan password")
    pwd = st.text_input("Password", type="password", placeholder="Masukkan password akses")
    if st.button("Masuk", type="primary"):
        if pwd == "PPA2KALBAR":
            st.session_state["auth_ok"] = True
            st.rerun()
        else:
            st.error("Password salah.")
    st.stop()

login_gate()


@st.cache_data(show_spinner=False)
def load_bank() -> dict:
    with open(BANK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

bank = load_bank()
metadata = bank.get("metadata", {})

# Bank v5 memakai question_pool. Untuk backward compatibility, kalau file lama masih berisi packages,
# aplikasi akan otomatis flatten seluruh paket menjadi satu pool.
def get_question_pool(bank_data: dict) -> list:
    if "question_pool" in bank_data:
        return list(bank_data["question_pool"])
    pool = []
    seen = set()
    for _, items in bank_data.get("packages", {}).items():
        for q in items:
            key = (q.get("category"), q.get("question"), tuple(q.get("options", [])), q.get("answer_index"))
            if key not in seen:
                seen.add(key)
                pool.append(q)
    return pool

QUESTION_POOL = get_question_pool(bank)
DEFAULT_RULES = metadata.get("tryout_rules") or {
    "Pengetahuan Umum Keuangan Negara": 15,
    "Pelaksanaan Anggaran": 15,
    "Pengelolaan Kas Negara": 15,
    "Manajemen Investasi": 15,
    "Pembinaan dan Pengelolaan Keuangan BLU": 15,
    "Akuntansi dan Pelaporan Keuangan": 15,
    "Fungsi Pendukung": 10,
}
TO_QUESTION_COUNT = int(metadata.get("tryout_question_count", 100))
SUBJECT_QUESTION_COUNT = int(metadata.get("subject_question_count", 50))
CATEGORIES = sorted({q["category"] for q in QUESTION_POOL})
SOURCE_FILTER_OPTIONS = metadata.get("source_filter_options") or ["All", "Bank Soal 1", "Bank Soal 2"]


def question_source_type(q: dict) -> str:
    """Return human source type for sampling.

    Bank Soal = soal dari dokumen Word unggahan user.
    Non Bank Soal = soal hasil konstruksi/review internal aplikasi.
    """
    stype = q.get("source_type")
    if stype in {"Bank Soal", "Non Bank Soal"}:
        return stype
    qid = str(q.get("id", ""))
    src = ((q.get("reference") or {}).get("source") or "")
    if qid.startswith(("DOCX", "FREG")) or "Bank soal unggahan" in src or "Bank Soal Komprehensif" in src:
        return "Bank Soal"
    return "Non Bank Soal"


def filter_pool_by_source(pool: list, source_filter: str | None) -> list:
    source_filter = source_filter or "All"
    if source_filter in {"Bank Soal 1", "Bank Soal Only"}:
        return [q for q in pool if question_source_type(q) == "Bank Soal"]
    if source_filter in {"Bank Soal 2", "Non Bank Soal"}:
        return [q for q in pool if question_source_type(q) == "Non Bank Soal"]
    return list(pool)


def effective_subject_pool(category: str, source_filter: str | None) -> list:
    """Pool efektif untuk TO per materi.

    Khusus pilihan Bank Soal 1: ambil dari Bank Soal 1 dulu. Jika jumlah soal pada materi
    tersebut kurang dari target 50, sisanya boleh ditambah dari Bank Soal 2 pada materi yang sama.
    Pilihan All dan Bank Soal 2 tetap berjalan sesuai sumber yang dipilih.
    """
    source_filter = source_filter or "All"
    if source_filter in {"Bank Soal 1", "Bank Soal Only"}:
        primary = [q for q in QUESTION_POOL if q.get("category") == category and question_source_type(q) == "Bank Soal"]
        if len(primary) >= SUBJECT_QUESTION_COUNT:
            return primary
        fallback = [q for q in QUESTION_POOL if q.get("category") == category and question_source_type(q) == "Non Bank Soal"]
        return primary + fallback
    return [q for q in filter_pool_by_source(QUESTION_POOL, source_filter) if q.get("category") == category]


def subject_source_availability(category: str, source_filter: str | None) -> tuple[int, int, int]:
    """Return (effective_total, bank1_count, bank2_count) for UI captions."""
    bank1_count = sum(1 for q in QUESTION_POOL if q.get("category") == category and question_source_type(q) == "Bank Soal")
    bank2_count = sum(1 for q in QUESTION_POOL if q.get("category") == category and question_source_type(q) == "Non Bank Soal")
    source_filter = source_filter or "All"
    if source_filter in {"Bank Soal 1", "Bank Soal Only"}:
        return bank1_count + (0 if bank1_count >= SUBJECT_QUESTION_COUNT else bank2_count), bank1_count, bank2_count
    if source_filter in {"Bank Soal 2", "Non Bank Soal"}:
        return bank2_count, bank1_count, bank2_count
    return bank1_count + bank2_count, bank1_count, bank2_count


SOURCE_COUNTS = {
    "All": len(QUESTION_POOL),
    "Bank Soal 1": sum(1 for q in QUESTION_POOL if question_source_type(q) == "Bank Soal"),
    "Bank Soal 2": sum(1 for q in QUESTION_POOL if question_source_type(q) == "Non Bank Soal"),
    # aliases for backward compatibility with saved sessions/older metadata
    "Bank Soal Only": sum(1 for q in QUESTION_POOL if question_source_type(q) == "Bank Soal"),
    "Non Bank Soal": sum(1 for q in QUESTION_POOL if question_source_type(q) == "Non Bank Soal"),
}


def key_for(suffix: str) -> str:
    return f"active_{suffix}"


def purge_radio_keys(qn: int = 180) -> None:
    for i in range(qn):
        st.session_state.pop(f"radio_active_{i}", None)
        st.session_state.pop(f"nav_active_{i}", None)
    st.session_state.pop("confirm_submit_active", None)


def composition_counts(items: list) -> dict:
    counts = {}
    for q in items:
        counts[q["category"]] = counts.get(q["category"], 0) + 1
    return counts


def normalized_question_key(q: dict) -> str:
    import re
    text = (q.get("question") or "").lower()
    text = re.sub(r"\s+", " ", text).strip()
    # hilangkan nomor/format ringan bila ada
    return text[:220]

def _simple_tokens(text: str) -> set:
    import re
    stop = {"yang","dan","di","ke","dari","pada","untuk","dengan","dalam","adalah","paling","tepat","berikut","kondisi","tersebut","sebagai","atau","jika","karena","saat","agar","tidak","sudah","hanya","menjadi","terkait"}
    text = re.sub(r"[^a-z0-9à-ÿ]+", " ", (text or "").lower())
    return {w for w in text.split() if w not in stop and len(w) > 2}


def _too_similar_to_selected(selected: list, q: dict, threshold: float = 0.58) -> bool:
    """Avoid same-package questions that are substantively too close.

    This is intentionally runtime-level: some uploaded/Word items remain in the bank,
    but one try out should not feel repetitive.
    """
    import difflib
    q_group = q.get("similarity_group")
    q_tokens = _simple_tokens(q.get("question", ""))
    q_norm = " ".join(sorted(q_tokens))
    for old in selected:
        if old.get("category") != q.get("category"):
            continue
        if q_group and old.get("similarity_group") == q_group:
            return True
        old_tokens = _simple_tokens(old.get("question", ""))
        if not q_tokens or not old_tokens:
            continue
        jacc = len(q_tokens & old_tokens) / max(1, len(q_tokens | old_tokens))
        if jacc >= threshold:
            return True
        old_norm = " ".join(sorted(old_tokens))
        if difflib.SequenceMatcher(None, q_norm, old_norm).ratio() >= 0.70:
            return True
    return False


def append_unique_question(selected: list, q: dict, selected_ids: set, selected_texts: set, allow_similar: bool = False) -> bool:
    qid = q.get("id", id(q))
    qtext = normalized_question_key(q)
    if qid in selected_ids or qtext in selected_texts:
        return False
    if not allow_similar and _too_similar_to_selected(selected, q):
        return False
    selected.append(q)
    selected_ids.add(qid)
    selected_texts.add(qtext)
    return True


def generate_tryout_questions(seed: int | None = None, source_filter: str = "All") -> list:
    """Generate paket TO acak 100 soal dengan rules komposisi materi.

    - Tiap kategori disampling sesuai kuota.
    - Urutan soal diacak.
    - Jika kuota kategori tidak cukup, kekurangan diambil dari pool kategori lain.
    """
    import random
    rng = random.Random(seed if seed is not None else time.time_ns())
    active_pool = filter_pool_by_source(QUESTION_POOL, source_filter)
    by_cat = {}
    for q in active_pool:
        by_cat.setdefault(q["category"], []).append(q)

    selected = []
    selected_ids = set()
    selected_texts = set()
    # sampling utama per rules; hindari pertanyaan yang persis sama dalam satu TO
    for cat, quota in DEFAULT_RULES.items():
        candidates = list(by_cat.get(cat, []))
        rng.shuffle(candidates)
        for q in candidates:
            if sum(1 for x in selected if x.get("category") == cat) >= int(quota):
                break
            append_unique_question(selected, q, selected_ids, selected_texts)

    # Jika ada kategori kurang atau target berubah, top-up dari sisa pool.
    # Pass pertama tetap menghindari soal mirip; pass kedua hanya dipakai jika bank kategori tertentu tidak cukup.
    target = TO_QUESTION_COUNT
    if len(selected) < target:
        rest = [q for q in active_pool if q.get("id", id(q)) not in selected_ids]
        rng.shuffle(rest)
        for q in rest:
            if len(selected) >= target:
                break
            append_unique_question(selected, q, selected_ids, selected_texts)
    if len(selected) < target:
        rest = [q for q in active_pool if q.get("id", id(q)) not in selected_ids]
        rng.shuffle(rest)
        for q in rest:
            if len(selected) >= target:
                break
            append_unique_question(selected, q, selected_ids, selected_texts, allow_similar=True)

    # Jika kelebihan karena rules > target, pangkas acak proporsional sederhana
    rng.shuffle(selected)
    selected = selected[:target]

    # Randomkan urutan final, bukan urutan materi
    rng.shuffle(selected)
    # Copy dan beri nomor runtime agar export jelas
    final = []
    for no, q in enumerate(selected, start=1):
        qq = dict(q)
        qq["runtime_no"] = no
        final.append(qq)
    return final



def generate_subject_questions(category: str, seed: int | None = None, source_filter: str = "All") -> list:
    """Generate TO fokus per materi 50 soal.

    Untuk pilihan Bank Soal 1, sistem mengambil soal Bank Soal 1 terlebih dahulu. Jika jumlahnya
    belum mencapai 50 pada materi tersebut, kekurangan diisi dari Bank Soal 2.
    """
    import random
    rng = random.Random(seed if seed is not None else time.time_ns())
    candidates = effective_subject_pool(category, source_filter)
    rng.shuffle(candidates)
    selected = []
    selected_ids = set()
    selected_texts = set()
    for q in candidates:
        if len(selected) >= SUBJECT_QUESTION_COUNT:
            break
        append_unique_question(selected, q, selected_ids, selected_texts)
    if len(selected) < SUBJECT_QUESTION_COUNT:
        # Fallback aman: jika setelah penghindaran soal mirip kurang dari 50, isi sisa dengan opsi paling tidak bermasalah.
        for q in candidates:
            if len(selected) >= SUBJECT_QUESTION_COUNT:
                break
            append_unique_question(selected, q, selected_ids, selected_texts, allow_similar=True)
    rng.shuffle(selected)
    final = []
    for no, q in enumerate(selected, start=1):
        qq = dict(q)
        qq["runtime_no"] = no
        final.append(qq)
    return final

def init_state() -> None:
    st.session_state.setdefault(key_for("started"), False)
    st.session_state.setdefault(key_for("submitted"), False)
    st.session_state.setdefault(key_for("start_time"), None)
    st.session_state.setdefault(key_for("questions"), [])
    st.session_state.setdefault(key_for("answers"), [])
    st.session_state.setdefault(key_for("flags"), [])
    st.session_state.setdefault(key_for("current"), 0)
    st.session_state.setdefault(key_for("duration"), int(metadata.get("duration_minutes_default", 150)) * 60)
    st.session_state.setdefault(key_for("seed"), None)
    st.session_state.setdefault(key_for("attempt_no"), 0)
    st.session_state.setdefault(key_for("mode"), "TO Acak Umum")
    st.session_state.setdefault(key_for("category"), None)
    st.session_state.setdefault(key_for("source_filter"), "All")


def start_new_tryout(duration_min: int = 150, mode: str = "TO Acak Umum", category: str | None = None, source_filter: str = "All") -> None:
    old_qn = len(st.session_state.get(key_for("questions"), [])) or TO_QUESTION_COUNT
    purge_radio_keys(max(old_qn, TO_QUESTION_COUNT, SUBJECT_QUESTION_COUNT) + 10)
    seed = int(time.time_ns() % (2**32 - 1))
    if mode == "TO Per Materi" and category:
        qs = generate_subject_questions(category, seed, source_filter)
    else:
        qs = generate_tryout_questions(seed, source_filter)
        mode = "TO Acak Umum"
        category = None
    st.session_state[key_for("attempt_no")] = int(st.session_state.get(key_for("attempt_no"), 0)) + 1
    st.session_state[key_for("seed")] = seed
    st.session_state[key_for("mode")] = mode
    st.session_state[key_for("category")] = category
    st.session_state[key_for("source_filter")] = source_filter
    st.session_state[key_for("questions")] = qs
    st.session_state[key_for("answers")] = [None] * len(qs)
    st.session_state[key_for("flags")] = [False] * len(qs)
    st.session_state[key_for("current")] = 0
    st.session_state[key_for("duration")] = int(duration_min) * 60
    st.session_state[key_for("start_time")] = time.time()
    st.session_state[key_for("started")] = True
    st.session_state[key_for("submitted")] = False


def reset_current_tryout() -> None:
    qs = st.session_state.get(key_for("questions"), [])
    qn = len(qs)
    purge_radio_keys(max(qn, TO_QUESTION_COUNT) + 10)
    st.session_state[key_for("answers")] = [None] * qn
    st.session_state[key_for("flags")] = [False] * qn
    st.session_state[key_for("current")] = 0
    st.session_state[key_for("start_time")] = time.time()
    st.session_state[key_for("submitted")] = False
    st.session_state[key_for("started")] = True


def go_to_home() -> None:
    """Kembali ke menu awal tanpa keluar/login ulang."""
    qs = st.session_state.get(key_for("questions"), [])
    qn = len(qs) or TO_QUESTION_COUNT
    purge_radio_keys(max(qn, TO_QUESTION_COUNT, SUBJECT_QUESTION_COUNT) + 10)
    st.session_state[key_for("started")] = False
    st.session_state[key_for("submitted")] = False
    st.session_state[key_for("start_time")] = None
    st.session_state[key_for("questions")] = []
    st.session_state[key_for("answers")] = []
    st.session_state[key_for("flags")] = []
    st.session_state[key_for("current")] = 0
    st.session_state[key_for("mode")] = "TO Acak Umum"
    st.session_state[key_for("category")] = None
    st.session_state[key_for("source_filter")] = "All"
    # auth_ok sengaja tidak dihapus agar user tidak diminta login ulang.


def elapsed_seconds() -> int:
    start = st.session_state.get(key_for("start_time"))
    if not start:
        return 0
    return int(time.time() - start)


def remaining_seconds() -> int:
    return max(0, st.session_state[key_for("duration")] - elapsed_seconds())


def fmt_time(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def timer_component() -> None:
    rem = remaining_seconds()
    components.html(
        f"""
        <div id='timer' style='font-family:Inter,system-ui,Segoe UI,sans-serif; border:1px solid #e4dccb; border-radius:16px; padding:13px 15px; background:#fffdf9; font-weight:850; font-size:24px; text-align:center; color:#17324d; box-shadow:0 6px 18px rgba(31,42,55,.045);'>{fmt_time(rem)}</div>
        <script>
        var remaining = {rem};
        function pad(n) {{ return n.toString().padStart(2, '0'); }}
        function tick() {{
          var h = Math.floor(remaining/3600);
          var m = Math.floor((remaining%3600)/60);
          var s = remaining%60;
          document.getElementById('timer').innerHTML = pad(h)+":"+pad(m)+":"+pad(s);
          if (remaining > 0) remaining -= 1;
        }}
        tick(); setInterval(tick, 1000);
        </script>
        """,
        height=64,
    )


def score_tryout():
    qs = st.session_state[key_for("questions")]
    answers = st.session_state[key_for("answers")]
    correct = sum(1 for i, q in enumerate(qs) if answers[i] == q["answer_index"])
    return correct, len(qs), round(correct / len(qs) * 100, 2) if qs else 0


def composition_df(items):
    if not items:
        rows = [{"Materi": k, "Jumlah": v} for k, v in DEFAULT_RULES.items()]
        return pd.DataFrame(rows)
    df = pd.Series([q["category"] for q in items]).value_counts().rename_axis("Materi").reset_index(name="Jumlah")
    return df.sort_values("Materi")


init_state()
qs = st.session_state[key_for("questions")]
answers = st.session_state[key_for("answers")]
flags = st.session_state[key_for("flags")]

# Sinkronkan pilihan radio ke model jawaban sebelum navigasi/status dirender.
for _i in range(len(qs)):
    _rk = f"radio_active_{_i}"
    if _rk in st.session_state and st.session_state[_rk] is not None:
        answers[_i] = st.session_state[_rk]
st.session_state[key_for("answers")] = answers

started = st.session_state[key_for("started")]
submitted = st.session_state[key_for("submitted")]
answered_count = sum(a is not None for a in answers)
flag_count = sum(flags)

# Sidebar
st.sidebar.markdown("### 🎓 Try Out DJPb")
st.sidebar.caption("Simulasi CAT lokal · paket otomatis acak")
if st.sidebar.button("🏠 Beranda", use_container_width=True):
    go_to_home()
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.markdown("**Mode TO**")
st.sidebar.caption("TO umum 100 soal acak, atau TO fokus per materi 50 soal.")
st.sidebar.markdown(f"<span class='exam-chip green'>Pool {len(QUESTION_POOL)} soal</span>", unsafe_allow_html=True)
st.sidebar.markdown(f"<span class='exam-chip gold'>Umum {TO_QUESTION_COUNT} soal</span>", unsafe_allow_html=True)
st.sidebar.markdown(f"<span class='exam-chip gold'>Per materi {SUBJECT_QUESTION_COUNT} soal</span>", unsafe_allow_html=True)
if started:
    st.sidebar.markdown("---")
    mode_label = st.session_state.get(key_for("mode"), "TO Acak Umum")
    cat_label = st.session_state.get(key_for("category"))
    title_label = f"{mode_label}" + (f" · {cat_label}" if cat_label else "")
    st.sidebar.markdown(f"**TO Aktif #{st.session_state.get(key_for('attempt_no'), 1)}**")
    st.sidebar.caption(title_label)
    st.sidebar.caption(f"Sumber: {st.session_state.get(key_for('source_filter'), 'All')}")
    st.sidebar.caption(f"Seed: {st.session_state.get(key_for('seed'))}")
    st.sidebar.caption(f"Timer {st.session_state[key_for('duration')] // 60} menit")
    st.sidebar.progress(answered_count / len(qs), text=f"Terjawab {answered_count}/{len(qs)}")
    if st.sidebar.button("Reset TO ini", use_container_width=True):
        reset_current_tryout()
        st.rerun()
    if st.sidebar.button("Buat TO baru mode sama", use_container_width=True):
        start_new_tryout(st.session_state[key_for("duration")] // 60, mode_label, cat_label, st.session_state.get(key_for("source_filter"), "All"))
        st.rerun()

# Header
st.markdown(
    """
    <div class="hero compact-hero">
      <h1>Bank Soal Try Out Kompetensi Teknis DJPb</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Landing
if not started:
    c1, c2 = st.columns([1.05, 1.15], gap="large")
    with c1:
        st.markdown("### Mulai try out")
        mode_choice = st.radio("Pilih mode", ["TO Acak Umum", "TO Per Materi"], horizontal=True)
        subject_choice = None
        source_choice = st.selectbox(
            "Sumber soal",
            SOURCE_FILTER_OPTIONS,
            index=0,
            help="All = gabungan semua soal; Bank Soal 1 = soal dari file Word/Bank Soal unggahan; Bank Soal 2 = soal internal yang sudah direview.",
        )
        default_timer = int(metadata.get("duration_minutes_default", 150))
        if mode_choice == "TO Per Materi":
            subject_choice = st.selectbox("Pilih materi fokus", CATEGORIES)
            default_timer = 60
            available, bank1_available, bank2_available = subject_source_availability(subject_choice, source_choice)
            if source_choice == "Bank Soal 1" and bank1_available < SUBJECT_QUESTION_COUNT:
                st.caption(
                    f"Bank Soal 1 pada materi ini tersedia {bank1_available} soal. "
                    f"Karena kurang dari {SUBJECT_QUESTION_COUNT}, paket akan otomatis menambah dari Bank Soal 2 "
                    f"sebanyak kebutuhan yang tersedia. Total efektif: {available} soal."
                )
            else:
                st.caption(f"Tersedia {available} soal pada materi ini dari sumber: {source_choice}. Paket fokus akan mengambil {min(SUBJECT_QUESTION_COUNT, available)} soal secara acak.")
            if available == 0:
                st.warning("Tidak ada soal untuk kombinasi materi dan sumber ini. Pilih sumber atau materi lain.")
        else:
            available = SOURCE_COUNTS.get(source_choice, 0)
            st.caption(f"Tersedia {available} soal untuk sumber: {source_choice}.")
            st.write("TO umum disusun menjadi 100 soal: enam materi inti masing-masing 15 soal, dan Fungsi Pendukung 10 soal agar tidak mendominasi.")
        dur_min = st.number_input("Timer per TO (menit)", min_value=10, max_value=240, value=default_timer, step=5)
        if mode_choice == "TO Acak Umum":
            st.info("Saran simulasi asesmen: 100 soal dalam 150 menit. Setelah submit, jawaban terkunci dan pembahasan bisa dibuka.")
            start_label = "Mulai TO Acak Umum"
        else:
            st.info("TO per materi berisi 50 soal acak dari materi yang dipilih. Jika Bank Soal 1 pada materi tersebut kurang dari 50 soal, sistem otomatis menambah dari Bank Soal 2.")
            start_label = "Mulai TO Per Materi"
        can_start = not (mode_choice == "TO Per Materi" and available == 0) and available > 0
        if st.button(start_label, type="primary", use_container_width=True, disabled=not can_start):
            start_new_tryout(int(dur_min), mode_choice, subject_choice, source_choice)
            st.rerun()
    with c2:
        st.markdown("### Komposisi dan ketersediaan soal")
        rules_df = pd.DataFrame([{
            "Materi": k,
            "Kuota TO Umum": v,
            "Pool All": sum(1 for q in QUESTION_POOL if q.get("category") == k),
            "Bank Soal 1": sum(1 for q in QUESTION_POOL if q.get("category") == k and question_source_type(q) == "Bank Soal"),
            "Bank Soal 2": sum(1 for q in QUESTION_POOL if q.get("category") == k and question_source_type(q) == "Non Bank Soal"),
        } for k, v in DEFAULT_RULES.items()])
        st.dataframe(rules_df, hide_index=True, use_container_width=True)
        st.caption("TO umum memakai kuota komposisi selama pool sumber memadai. TO per materi juga mengikuti sumber soal yang dipilih dan mengambil hingga 50 soal acak dari materi tersebut.")
    st.stop()

# Jika user memulai dengan file lama yang belum punya qs aktif
if not qs:
    st.warning("Belum ada paket aktif. Klik 'Buat TO acak baru' di sidebar atau kembali ke awal.")
    st.stop()

# Top status cards
if not submitted and remaining_seconds() <= 0:
    st.warning("Waktu sudah habis. Silakan submit final untuk melihat hasil.")

m1, m2, m3, m4 = st.columns([1, 1, 1, 1.2])
with m1:
    _mode = st.session_state.get(key_for('mode'), 'TO Acak Umum')
    _src = st.session_state.get(key_for('source_filter'), 'All')
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Paket · {_src}</div><div class='metric-value'>{_mode} #{st.session_state.get(key_for('attempt_no'), 1)}</div></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Terjawab</div><div class='metric-value'>{answered_count}/{len(qs)}</div></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><div class='metric-label'>Ditandai</div><div class='metric-value'>{flag_count}</div></div>", unsafe_allow_html=True)
with m4:
    timer_component()

st.progress(answered_count / len(qs), text=f"Progress pengerjaan {answered_count}/{len(qs)} soal")

# Submitted result
if submitted:
    correct, total, score = score_tryout()
    st.success(f"Submit final selesai. Skor: {score} ({correct}/{total} benar).")
    c_home, c_retry = st.columns([1, 1])
    with c_home:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            go_to_home()
            st.rerun()
    with c_retry:
        if st.button("Buat TO Baru Mode Sama", use_container_width=True):
            start_new_tryout(st.session_state[key_for("duration")] // 60, st.session_state.get(key_for("mode"), "TO Acak Umum"), st.session_state.get(key_for("category")), st.session_state.get(key_for("source_filter"), "All"))
            st.rerun()
    tab1, tab2, tab3 = st.tabs(["Ringkasan", "Kunci & Pembahasan", "Ekspor Hasil"])
    with tab1:
        rows = []
        for cat in sorted(set(q["category"] for q in qs)):
            idxs = [i for i, q in enumerate(qs) if q["category"] == cat]
            c = sum(1 for i in idxs if answers[i] == qs[i]["answer_index"])
            rows.append({"Materi": cat, "Benar": c, "Jumlah": len(idxs), "Skor %": round(c / len(idxs) * 100, 2)})
        df = pd.DataFrame(rows)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.bar_chart(df.set_index("Materi")["Skor %"])
    with tab2:
        filter_cat = st.selectbox("Filter materi", ["Semua"] + sorted(set(q["category"] for q in qs)))
        only_wrong = st.checkbox("Tampilkan yang salah/kosong saja", value=False)
        for i, q in enumerate(qs):
            if filter_cat != "Semua" and q["category"] != filter_cat:
                continue
            is_correct = answers[i] == q["answer_index"]
            if only_wrong and is_correct:
                continue
            user_ans = "-" if answers[i] is None else chr(65 + answers[i])
            correct_ans = chr(65 + q["answer_index"])
            status = "✅ Benar" if is_correct else "❌ Salah/kosong"
            with st.expander(f"{i+1}. {status} · Jawaban Anda: {user_ans} · Kunci: {correct_ans} · {q['category']}"):
                st.markdown(f"<div class='qtext'><b>Soal:</b> {q['question']}</div>", unsafe_allow_html=True)
                st.markdown("**Pilihan jawaban:**")
                option_lines = []
                for j, opt in enumerate(q["options"]):
                    prefix = chr(65 + j)
                    option_lines.append(f"<li><b>{prefix}.</b> {opt}</li>")
                st.markdown("<ul>" + "".join(option_lines) + "</ul>", unsafe_allow_html=True)

                user_text = "Belum dijawab" if answers[i] is None else f"{chr(65 + answers[i])}. {q['options'][answers[i]]}"
                key_text = f"{chr(65 + q['answer_index'])}. {q['options'][q['answer_index']]}"
                ans_box = "correct" if is_correct else "wrong"
                st.markdown(f"<div class='{ans_box}'><b>Jawaban Anda:</b> {user_text}<br><b>Kunci Jawaban:</b> {key_text}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='neutral'><b>Pembahasan:</b> {q['explanation']}</div>", unsafe_allow_html=True)
                ref = q.get("reference", {})
                st.markdown(f"**Referensi utama soal:** {ref.get('source','-')}; {ref.get('page','-')}; keyword: `{ref.get('keyword','-')}`")
    with tab3:
        rows = []
        for i, q in enumerate(qs):
            rows.append({
                "No": i + 1,
                "ID": q.get("id", ""),
                "Materi": q["category"],
                "Tingkat": q.get("difficulty", ""),
                "Jawaban_User": "-" if answers[i] is None else chr(65 + answers[i]),
                "Kunci": chr(65 + q["answer_index"]),
                "Benar": answers[i] == q["answer_index"],
                "Referensi": f"{q.get('reference',{}).get('source','-')} | {q.get('reference',{}).get('page','-')} | {q.get('reference',{}).get('keyword','-')}",
            })
        result_df = pd.DataFrame(rows)
        st.download_button(
            "Download hasil CSV",
            result_df.to_csv(index=False).encode("utf-8"),
            file_name=f"hasil_TO_{st.session_state.get(key_for('mode'), 'acak').replace(' ', '_')}_{st.session_state.get(key_for('attempt_no'), 1)}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.dataframe(result_df, hide_index=True, use_container_width=True)
    st.stop()

# Exam UI
left, right = st.columns([0.32, 0.68], gap="large")
with left:
    st.markdown("### Navigasi Soal")
    st.markdown('<div class="nav-caption">✓ terjawab · ⚑ ditandai · nomor polos kosong</div>', unsafe_allow_html=True)
    nav_col_count = 4
    nav_cols = st.columns(nav_col_count)
    current_idx = st.session_state[key_for("current")]
    for i in range(len(qs)):
        label = str(i + 1)
        if answers[i] is not None and flags[i]:
            label = "✓ ⚑ " + label
            nav_class = "nav-answer nav-flag"
        elif answers[i] is not None:
            label = "✓ " + label
            nav_class = "nav-answer"
        elif flags[i]:
            label = "⚑ " + label
            nav_class = "nav-flag"
        else:
            nav_class = "nav-empty"
        if i == current_idx:
            nav_class += " nav-current"
        with nav_cols[i % nav_col_count]:
            st.markdown(f'<div class="{nav_class}">', unsafe_allow_html=True)
            btn_type = "primary" if answers[i] is not None else "secondary"
            clicked = st.button(label, key=f"nav_active_{i}", use_container_width=True, type=btn_type)
            st.markdown('</div>', unsafe_allow_html=True)
            if clicked:
                st.session_state[key_for("current")] = i
                st.rerun()
    st.markdown("---")
    st.caption(f"Kosong: {len(qs) - answered_count} soal")
    empty_nums = [str(i + 1) for i, a in enumerate(answers) if a is None]
    if empty_nums:
        st.caption("Nomor kosong: " + ", ".join(empty_nums[:60]) + (" ..." if len(empty_nums) > 60 else ""))

with right:
    idx = st.session_state[key_for("current")]
    q = qs[idx]
    st.markdown(f"<div class='question-title'>Soal {idx+1} dari {len(qs)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='qtext'>{q['question']}</div>", unsafe_allow_html=True)
    st.write("")

    current_answer = answers[idx]
    option_labels = [f"{chr(65+i)}. {opt}" for i, opt in enumerate(q["options"])]
    radio_key = f"radio_active_{idx}"
    selected = st.radio(
        "Pilih jawaban",
        options=list(range(len(option_labels))),
        format_func=lambda i: option_labels[i],
        index=current_answer if current_answer is not None else None,
        key=radio_key,
    )
    answers[idx] = selected
    st.session_state[key_for("answers")] = answers
    answered_count = sum(a is not None for a in answers)

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3, b4, b5 = st.columns([1, 1, 1, 1, 1.45])
    if b1.button("← Sebelumnya", disabled=idx == 0, use_container_width=True):
        st.session_state[key_for("current")] = max(0, idx - 1)
        st.rerun()
    if b2.button("Berikutnya →", disabled=idx == len(qs) - 1, use_container_width=True):
        st.session_state[key_for("current")] = min(len(qs) - 1, idx + 1)
        st.rerun()
    if b3.button("Tandai/Unflag", use_container_width=True):
        flags[idx] = not flags[idx]
        st.session_state[key_for("flags")] = flags
        st.rerun()
    if b4.button("Kosongkan", use_container_width=True):
        answers[idx] = None
        st.session_state[key_for("answers")] = answers
        st.session_state.pop(radio_key, None)
        st.rerun()
    with b5:
        submit_ready = st.checkbox("Saya yakin submit final", key="confirm_submit_active")
        if st.button("Submit Final", type="primary", disabled=not submit_ready, use_container_width=True):
            st.session_state[key_for("submitted")] = True
            st.rerun()

    with st.expander("Ringkasan jawaban sementara"):
        st.write(f"Terjawab: {answered_count}/{len(qs)} · Kosong: {len(qs)-answered_count} · Ditandai: {flag_count}")
        current_comp = composition_df(qs)
        st.dataframe(current_comp, hide_index=True, use_container_width=True)
        if len(qs) - answered_count > 0:
            empty_nums = [str(i + 1) for i, a in enumerate(answers) if a is None]
            st.caption("Nomor kosong: " + ", ".join(empty_nums[:100]) + (" ..." if len(empty_nums) > 100 else ""))
