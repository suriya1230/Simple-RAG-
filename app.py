import streamlit as st
import re, os
from groq import Groq


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

MODELS = {
    "Llama 3.3 · 70B  —  Best Quality":   "llama-3.3-70b-versatile",
}

st.set_page_config(page_title="NovaDocs", page_icon="🔥",
                   layout="wide", initial_sidebar_state="expanded")

# ─────────────────────────────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
  --bg:        #080705;
  --surface:   #100d0a;
  --surface2:  #181310;
  --border:    rgba(255,140,50,0.10);
  --border-hi: rgba(255,140,50,0.28);
  --accent:    #f97316;
  --accent2:   #fb923c;
  --accent3:   #fdba74;
  --text:      #fdf3e9;
  --muted:     rgba(253,186,116,0.45);
  --muted2:    rgba(253,186,116,0.22);
}

*, html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif;
  box-sizing: border-box;
}

/* ── App background with subtle radial glow ── */
.stApp {
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 70% 45% at 15% 0%,   rgba(249,115,22,.07) 0%, transparent 55%),
    radial-gradient(ellipse 50% 35% at 85% 100%,  rgba(234,88,12,.05)  0%, transparent 50%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 28px !important; }

/* ── Sidebar select ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border-hi) !important;
  border-radius: 9px !important;
  color: var(--text) !important;
  font-size: .85rem !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--surface2) !important;
  border: 1.5px dashed var(--border-hi) !important;
  border-radius: 12px !important;
  transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--accent) !important;
  background: rgba(249,115,22,.04) !important;
}

/* ── Primary button ── */
.stButton > button {
  width: 100%;
  background: linear-gradient(135deg, #c2410c 0%, #ea580c 45%, #f97316 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important;
  font-size: .82rem !important;
  letter-spacing: .07em !important;
  text-transform: uppercase !important;
  padding: 12px 0 !important;
  transition: all .2s cubic-bezier(.4,0,.2,1) !important;
  box-shadow: 0 2px 18px rgba(234,88,12,.22) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 32px rgba(249,115,22,.38) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
  background: var(--accent) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
  background: var(--surface) !important;
  border-top: 1px solid var(--border) !important;
}
[data-testid="stChatInput"] textarea {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border-hi) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: .93rem !important;
  padding: 14px 18px !important;
}
[data-testid="stChatInput"] textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(249,115,22,.12) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 4px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(249,115,22,.25); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(249,115,22,.45); }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ════════════════════════════════
   KEYFRAMES
   ════════════════════════════════ */
@keyframes fadeUp {
  from { opacity:0; transform:translateY(16px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}
@keyframes orb-pulse {
  0%,100% { transform: scale(1);   opacity:.7; }
  50%      { transform: scale(1.2); opacity:1; }
}
@keyframes border-glow {
  0%,100% { box-shadow: 0 0 0 0   rgba(249,115,22,.0); }
  50%      { box-shadow: 0 0 18px 2px rgba(249,115,22,.18); }
}
@keyframes typing-cursor {
  0%,100% { opacity:1; }
  50%      { opacity:0; }
}

/* ════════════════════════════════
   COMPONENT STYLES
   ════════════════════════════════ */

/* Sidebar logo */
.sb-logo {
  font-family: 'Fraunces', serif;
  font-weight: 700;
  font-size: 1.65rem;
  letter-spacing: -.01em;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 55%, var(--accent3) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}
.sb-tagline {
  font-size: .67rem;
  color: var(--muted);
  letter-spacing: .18em;
  text-transform: uppercase;
  margin-top: 3px;
  display: flex;
  align-items: center;
  gap: 7px;
}
.sb-orb {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent);
  display: inline-block;
  animation: orb-pulse 2s infinite;
}

.sb-label {
  font-size: .62rem;
  font-weight: 700;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 18px 0 8px;
  padding-left: 2px;
}

/* Active doc card */
.doc-card {
  background: linear-gradient(135deg, rgba(234,88,12,.08), rgba(249,115,22,.04));
  border: 1px solid var(--border-hi);
  border-radius: 12px;
  padding: 14px 16px;
  margin-top: 12px;
  animation: border-glow 3s infinite;
}
.doc-name {
  color: var(--text);
  font-weight: 600;
  font-size: .84rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 8px;
}
.doc-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(249,115,22,.12);
  border: 1px solid rgba(249,115,22,.22);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: .68rem;
  font-weight: 700;
  color: var(--accent2);
  letter-spacing: .05em;
}

/* ─── HERO ─── */
.hero {
  max-width: 680px;
  margin: 60px auto 0;
  text-align: center;
  animation: fadeUp .55s cubic-bezier(.4,0,.2,1) both;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(249,115,22,.08);
  border: 1px solid rgba(249,115,22,.2);
  border-radius: 20px;
  padding: 5px 16px;
  font-size: .72rem;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--accent2);
  margin-bottom: 22px;
}
.hero-title {
  font-family: 'Fraunces', serif;
  font-weight: 700;
  font-size: 3.4rem;
  line-height: 1.05;
  letter-spacing: -.025em;
  color: var(--text);
  margin-bottom: 18px;
}
.hero-title span {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 50%, var(--accent3) 100%);
  background-size: 200% auto;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3.5s linear infinite;
}
.hero-desc {
  color: var(--muted);
  font-size: .97rem;
  line-height: 1.75;
  max-width: 460px;
  margin: 0 auto 40px;
  font-weight: 300;
}

/* ─── FEATURE CARDS (rendered via st.columns) ─── */
.feat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 18px;
  text-align: center;
  transition: all .25s cubic-bezier(.4,0,.2,1);
  cursor: default;
  height: 100%;
}
.feat-card:hover {
  border-color: var(--border-hi);
  background: var(--surface2);
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,.35), 0 0 0 1px var(--border-hi);
}
.feat-icon { font-size: 1.8rem; margin-bottom: 10px; display: block; }
.feat-model {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: .9rem;
  color: var(--accent2);
  margin-bottom: 4px;
}
.feat-desc { font-size: .75rem; color: var(--muted); font-weight: 300; }

/* ─── STEP LIST ─── */
.steps {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 380px;
  margin: 36px auto 0;
}
.step {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: .85rem;
  color: var(--muted);
}
.step-n {
  width: 26px; height: 26px; flex-shrink: 0;
  border-radius: 50%;
  border: 1px solid rgba(249,115,22,.3);
  background: rgba(249,115,22,.07);
  color: var(--accent);
  font-size: .7rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
}

/* ─── CHAT AREA ─── */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2px 18px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 22px;
  animation: fadeUp .35s ease both;
}
.chat-doc-info { display: flex; align-items: center; gap: 12px; }
.chat-icon {
  width: 42px; height: 42px;
  border-radius: 11px;
  background: linear-gradient(135deg, #c2410c, #f97316);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.15rem;
  box-shadow: 0 4px 16px rgba(234,88,12,.3);
  flex-shrink: 0;
}
.chat-doc-name {
  font-weight: 700;
  font-size: .97rem;
  color: var(--text);
  line-height: 1.2;
}
.chat-doc-sub {
  font-size: .72rem;
  color: var(--muted);
  margin-top: 2px;
}
.model-tag {
  font-family: 'Fira Code', monospace;
  font-size: .68rem;
  color: var(--accent2);
  background: rgba(249,115,22,.08);
  border: 1px solid rgba(249,115,22,.18);
  border-radius: 6px;
  padding: 5px 11px;
  white-space: nowrap;
}

/* ─── ANSWER CARD ─── */
.answer-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 26px;
  color: var(--text);
  font-size: .94rem;
  line-height: 1.85;
  position: relative;
  overflow: hidden;
  animation: fadeUp .3s ease both;
}
.answer-card::after {
  content: '';
  position: absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg,
    transparent 0%, var(--accent) 30%, var(--accent2) 60%, var(--accent3) 80%, transparent 100%);
  background-size: 200% 100%;
  animation: shimmer 2.5s linear infinite;
}
.answer-cursor { animation: typing-cursor .7s infinite; }

/* ─── SOURCE CHUNKS ─── */
.src-label {
  font-size: .62rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.src-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}
.src-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 2px solid var(--accent);
  border-radius: 8px;
  padding: 10px 13px;
  margin-bottom: 8px;
  animation: fadeUp .3s ease both;
}
.src-score {
  font-family: 'Fira Code', monospace;
  font-size: .62rem;
  color: var(--accent);
  font-weight: 500;
  letter-spacing: .04em;
  margin-bottom: 5px;
}
.src-text {
  font-size: .78rem;
  color: var(--muted);
  line-height: 1.6;
  font-weight: 300;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# RAG PIPELINE
# ──────────────────────────────────────────────────────────────────────
def extract_text(f):
    name = f.name.lower()
    if name.endswith((".txt", ".md")):
        return f.read().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        try:
            import pypdf
            return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(f).pages)
        except ImportError:
            st.error("Run: pip install pypdf"); return ""
    st.error("Use .txt, .pdf or .md"); return ""

def chunk_text(text, size=400, overlap=80):
    words = text.split(); chunks, i = [], 0
    while i < len(words):
        c = " ".join(words[i: i+size])
        if c.strip(): chunks.append(c.strip())
        i += size - overlap
    return chunks

def build_tfidf(chunks):
    import math
    def tok(t): return re.findall(r'\b[a-z]{2,}\b', t.lower())
    df = {}
    for c in chunks:
        for w in set(tok(c)): df[w] = df.get(w,0)+1
    N = len(chunks)
    idf = {w: math.log((N+1)/(f+1))+1 for w,f in df.items()}
    vecs = []
    for c in chunks:
        tokens=tok(c); tf={}
        for w in tokens: tf[w]=tf.get(w,0)+1
        t=len(tokens) or 1
        vecs.append({w:(cnt/t)*idf.get(w,1) for w,cnt in tf.items()})
    return vecs, idf, tok

def cosine(a, b):
    k=set(a)&set(b); dot=sum(a[i]*b[i] for i in k)
    return dot/((sum(v*v for v in a.values())**.5)*(sum(v*v for v in b.values())**.5)+1e-9)

def retrieve(q, chunks, vecs, idf, tok_fn, k):
    tokens=tok_fn(q); tf={}
    for w in tokens: tf[w]=tf.get(w,0)+1
    t=len(tokens) or 1
    qv={w:(cnt/t)*idf.get(w,1) for w,cnt in tf.items()}
    return sorted([(cosine(qv,v),c) for v,c in zip(vecs,chunks)],reverse=True)[:k]

def stream_groq(question, ctx_chunks, model_id):
    client = Groq()
    ctx = "\n\n---\n\n".join(ctx_chunks)
    prompt = (
        "Answer ONLY from the context. "
        "If not found, say \"I couldn't find that in the document.\"\n\n"
        f"CONTEXT:\n{ctx}\n\nQUESTION: {question}\n\nANSWER:"
    )
    for chunk in client.chat.completions.create(
        model=model_id,
        messages=[{"role":"user","content":prompt}],
        max_tokens=1024, stream=True
    ):
        d = chunk.choices[0].delta.content
        if d: yield d


# ── Session state ──
for k,v in dict(chunks=[],vecs=None,idf=None,tok_fn=None,doc_name=None,history=[]).items():
    if k not in st.session_state: st.session_state[k]=v


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:0 4px 20px">
        <div class="sb-logo">NovaDocs</div>
        <div class="sb-tagline">
            <span class="sb-orb"></span>
            RAG · Groq Inference
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Model</div>', unsafe_allow_html=True)
    model_label = st.selectbox("m", list(MODELS.keys()), label_visibility="collapsed")
    model_id = MODELS[model_label]

    st.markdown('<div class="sb-label">Document</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("f", type=["txt","pdf","md"], label_visibility="collapsed")

    with st.expander("⚙️  RAG Settings"):
        chunk_size = st.slider("Chunk size (words)", 200, 800, 400, 50)
        overlap    = st.slider("Overlap (words)", 20, 200, 80, 10)
        top_k      = st.slider("Sources retrieved", 1, 8, 4, 1)

    if uploaded:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥  Index Document"):
            with st.spinner("Processing…"):
                raw = extract_text(uploaded)
                if raw.strip():
                    chunks = chunk_text(raw, chunk_size, overlap)
                    vecs, idf, tok_fn = build_tfidf(chunks)
                    st.session_state.update(dict(
                        chunks=chunks, vecs=vecs, idf=idf, tok_fn=tok_fn,
                        doc_name=uploaded.name, history=[]
                    ))
                    st.success(f"✅  {len(chunks)} chunks ready")

    if st.session_state.doc_name:
        n = len(st.session_state.chunks)
        st.markdown(f"""
        <div class="doc-card">
            <div class="doc-name">🔥 &nbsp;{st.session_state.doc_name}</div>
            <span class="doc-badge">⬡ {n} chunks indexed</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✕  Remove document"):
            for k in ["chunks","vecs","idf","tok_fn","doc_name","history"]:
                st.session_state[k] = [] if k in ("chunks","history") else None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

# ─── LANDING ──────────────────────────────────────────────────────────
if not st.session_state.doc_name:

    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">
            <span style="width:6px;height:6px;border-radius:50%;background:#f97316;display:inline-block"></span>
            Powered by Groq · Open-Source LLMs
        </div>
        <div class="hero-title">
            Ask anything.<br><span>Get precise answers.</span>
        </div>
        <div class="hero-desc">
            Upload any document and instantly query it with the world's fastest
            open-source inference. No API costs. No subscriptions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards using st.columns (proper grid)
    st.markdown("""
<div style="
    display:flex;
    justify-content:center;
    align-items:center;
    width:100%;
    margin-top:40px;
">
    <div class="feat-card" style="width:320px; text-align:center;">
        <span class="feat-icon">🦙</span>
        <div class="feat-model">Llama 3.3 · 70B</div>
        <div class="feat-desc">Best answer quality</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class="steps">
        <div class="step"><div class="step-n">1</div> Upload a PDF, TXT or MD in the sidebar</div>
        <div class="step"><div class="step-n">2</div> Click <strong style="color:#f97316">🔥 Index Document</strong></div>
        <div class="step"><div class="step-n">3</div> Ask questions in the chat below</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.chat_input("Upload and index a document to start…", disabled=True)


# ─── CHAT ─────────────────────────────────────────────────────────────
else:
    n = len(st.session_state.chunks)

    st.markdown(f"""
    <div class="chat-header">
        <div class="chat-doc-info">
            <div class="chat-icon">🔥</div>
            <div>
                <div class="chat-doc-name">{st.session_state.doc_name}</div>
                <div class="chat-doc-sub">{n} chunks indexed · ready</div>
            </div>
        </div>
        <div class="model-tag">{model_id}</div>
    </div>
    """, unsafe_allow_html=True)

    # History
    for entry in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(f'<span style="color:var(--text,#fdf3e9)">{entry["q"]}</span>',
                        unsafe_allow_html=True)
        with st.chat_message("assistant"):
            a, c = st.columns([3, 2])
            with a:
                st.markdown(f'<div class="answer-card">{entry["a"]}</div>',
                            unsafe_allow_html=True)
            with c:
                st.markdown('<div class="src-label">Sources</div>', unsafe_allow_html=True)
                for score, chunk in entry["ctx"]:
                    st.markdown(f"""
                    <div class="src-card">
                        <div class="src-score">score {score:.4f}</div>
                        <div class="src-text">{chunk[:240]}{"…" if len(chunk)>240 else ""}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Input
    question = st.chat_input("Ask anything about your document…")

    if question:
        with st.chat_message("user"):
            st.markdown(f'<span style="color:#fdf3e9">{question}</span>',
                        unsafe_allow_html=True)

        with st.chat_message("assistant"):
            a_col, c_col = st.columns([3, 2])

            hits = retrieve(question, st.session_state.chunks,
                            st.session_state.vecs, st.session_state.idf,
                            st.session_state.tok_fn, top_k)
            ctx_chunks = [c for _, c in hits]

            with c_col:
                st.markdown('<div class="src-label">Sources</div>', unsafe_allow_html=True)
                for score, chunk in hits:
                    st.markdown(f"""
                    <div class="src-card">
                        <div class="src-score">score {score:.4f}</div>
                        <div class="src-text">{chunk[:240]}{"…" if len(chunk)>240 else ""}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with a_col:
                ph = st.empty()
                full = ""
                for token in stream_groq(question, ctx_chunks, model_id):
                    full += token
                    ph.markdown(f'<div class="answer-card">{full}<span class="answer-cursor">|</span></div>',
                                unsafe_allow_html=True)
                ph.markdown(f'<div class="answer-card">{full}</div>',
                            unsafe_allow_html=True)

        st.session_state.history.append({"q":question,"a":full,"ctx":hits})