import streamlit as st
import streamlit.components.v1 as components
import json
import random
import html
import math
import base64
import os

st.set_page_config(
    page_title="Review Score Challenge",
    page_icon="\u25c6",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SCALE_MIN, SCALE_MAX = 3.0, 7.0
STD_SCALE_MAX = 1.0
BG_MUSIC_FILE = "walking-in-the-park.mp3"
BEEP_B64 = "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"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    :root {
        --bg: #f6f7fb; --card: #ffffff; --line: #e7e9f0; --ink: #0f172a; --muted: #64748b; --faint: #94a3b8;
        --blue: #4f46e5; --blue-d: #4338ca; --blue-l: #eef2ff;
        --violet: #7c3aed; --violet-l: #f5f3ff;
        --green: #10b981; --green-l: #ecfdf5; --red: #ef4444; --red-l: #fef2f2; --amber: #f59e0b;
    }
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; box-sizing: border-box; }
    html, body { background: var(--bg) !important; color: var(--ink) !important; }
    .stApp, [data-testid="stAppViewContainer"] { background: radial-gradient(1200px 500px at 50% -10%, #e9ebff 0%, transparent 60%), var(--bg) !important; }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { padding: 1.4rem 1rem 3rem 1rem !important; max-width: 1180px !important; }
    h1, h2, h3, h4, h5, p, div, span, label { color: var(--ink); }
    *::-webkit-scrollbar { width: 12px; height: 12px; }
    *::-webkit-scrollbar-track { background: transparent; }
    *::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #a5b4fc 0%, #c4b5fd 100%); border-radius: 999px; border: 3px solid transparent; background-clip: padding-box; min-height: 48px; transition: background .2s ease; }
    *::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%); background-clip: padding-box; border: 3px solid transparent; }
    *::-webkit-scrollbar-corner { background: transparent; }
    @supports not selector(::-webkit-scrollbar) { * { scrollbar-width: thin; scrollbar-color: #a5b4fc transparent; } }
    html { scroll-behavior: smooth; }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @keyframes pop { 0% { transform: scale(.85); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    @keyframes flashGreen { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,.55); } 70% { box-shadow: 0 0 0 16px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
    .fx { animation: fadeUp .35s ease both; }
    .flash-ok { animation: pop .3s ease both, flashGreen .9s ease 1; }
    [data-testid="stTooltipContent"], div[role="tooltip"], div[role="tooltip"] > div { background: #0f172a !important; background-color: #0f172a !important; border-radius: 10px !important; box-shadow: 0 8px 20px rgba(15,23,42,.25) !important; }
    [data-testid="stTooltipContent"] *, div[role="tooltip"] * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-size: 12px !important; font-weight: 600 !important; opacity: 1 !important; }
    [data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"], span[data-testid^="stIcon"], .material-symbols-rounded, .material-symbols-outlined, .material-icons { font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important; font-size: 18px !important; }
    [data-testid="stExpander"] summary { display: flex !important; align-items: center !important; gap: 6px !important; background: var(--card) !important; background-color: var(--card) !important; border-radius: 12px !important; padding: 10px 14px !important; font-size: 12.5px !important; font-weight: 700 !important; }
    [data-testid="stExpander"] summary:hover { background: #f8f9ff !important; background-color: #f8f9ff !important; }
    [data-testid="stExpander"] summary *, [data-testid="stExpander"] summary span, [data-testid="stExpander"] summary p { color: var(--ink) !important; background: transparent !important; }
    [data-testid="stExpander"] { background: var(--card) !important; background-color: var(--card) !important; border: 1.5px solid var(--line) !important; border-radius: 14px !important; margin-bottom: 9px !important; overflow: hidden !important; }
    [data-testid="stExpanderDetails"] { background: var(--card) !important; background-color: var(--card) !important; color: var(--ink) !important; padding: 2px 14px 12px 14px !important; }
    [data-testid="stExpanderDetails"] p, [data-testid="stExpanderDetails"] div { color: var(--ink); }
    .stButton button, button[kind="secondary"], button[kind="primary"], [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"], div[class*="st-key-lopt_"] button, div[class*="st-key-ropt_"] button, div[class*="st-key-cta_"] button { background: #ffffff !important; background-color: #ffffff !important; background-image: none !important; color: var(--ink) !important; border: 1.5px solid var(--line) !important; border-radius: 14px !important; box-shadow: 0 1px 2px rgba(15,23,42,.04) !important; text-shadow: none !important; transition: all .16s ease !important; }
    div[class*="st-key-cta_"] button { background: linear-gradient(135deg, #4f46e5, #6d5cf5) !important; border: none !important; box-shadow: 0 8px 20px rgba(79,70,229,.28) !important; padding: 15px 24px !important; width: 100% !important; margin-top: 10px !important; }
    div[class*="st-key-cta_"] button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 26px rgba(79,70,229,.38) !important; }
    div[class*="st-key-cta_"] button *, div[class*="st-key-cta_"] button p { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; background: transparent !important; font-weight: 700 !important; font-size: 15px !important; }
    div[class*="st-key-lopt_"] button, div[class*="st-key-ropt_"] button { width: 100% !important; text-align: left !important; justify-content: flex-start !important; padding: 15px 18px !important; font-size: 13.5px !important; font-weight: 600 !important; line-height: 1.5 !important; white-space: pre-wrap !important; height: auto !important; min-height: 0 !important; display: block !important; text-transform: none !important; letter-spacing: 0 !important; margin-bottom: 4px !important; }
    div[class*="st-key-lopt_"] button:hover { border-color: var(--blue) !important; background: #f8f9ff !important; box-shadow: 0 6px 16px rgba(79,70,229,.12) !important; transform: translateY(-1px) !important; }
    div[class*="st-key-ropt_"] button:hover { border-color: var(--violet) !important; background: #fbf9ff !important; box-shadow: 0 6px 16px rgba(124,58,237,.12) !important; transform: translateY(-1px) !important; }
    div[class*="st-key-lopt_"] button:focus, div[class*="st-key-ropt_"] button:focus { outline: none !important; }
    div[class*="st-key-lopt_"] button *, div[class*="st-key-ropt_"] button * { background: transparent !important; color: var(--ink) !important; text-align: left !important; font-weight: 600 !important; font-size: 13.5px !important; line-height: 1.5 !important; white-space: pre-wrap !important; text-shadow: none !important; }
    div[class*="st-key-lopt_"] button p::first-letter { color: var(--blue) !important; font-weight: 900 !important; font-size: 16px !important; }
    div[class*="st-key-ropt_"] button p::first-letter { color: var(--violet) !important; font-weight: 900 !important; font-size: 16px !important; }

    /* Center the st.image component */
    [data-testid="stImage"] { display: flex !important; justify-content: center !important; align-items: center !important; width: 100% !important; margin: 0 auto !important; }
    [data-testid="stImage"] img { max-width: 220px !important; width: auto !important; height: auto !important; aspect-ratio: 1 / 1 !important; object-fit: contain !important; border-radius: 12px !important; border: 1.5px solid var(--line) !important; display: block !important; margin: 0 auto !important; cursor: zoom-in !important; }

    /* ============ REMOVE STREAMLIT'S NATIVE FULLSCREEN BUTTON ENTIRELY ============ */
    [data-testid="stImage"] button,
    [data-testid="stImage"] > div > button,
    [data-testid="stImage"] > div > div > button,
    [data-testid="StyledFullScreenButton"],
    button[title="View fullscreen"],
    button[title="Fullscreen"],
    button[aria-label="View fullscreen"],
    button[aria-label="Fullscreen"],
    button[aria-label="Full screen"],
    [class*="FullScreenButton"],
    [class*="fullscreenButton"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
    }
    /* Ensure image container doesn't reserve space for the hidden button */
    [data-testid="stImage"] > div { position: relative !important; }

    .hd { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 0 2px 16px 2px; margin-bottom: 16px; border-bottom: 1.5px solid var(--line); }
    .brand { display: flex; align-items: center; gap: 10px; }
    .brand-mark { width: 32px; height: 32px; border-radius: 10px; background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 900; box-shadow: 0 6px 14px rgba(79,70,229,.3); }
    .brand-name { font-size: 16px; font-weight: 800; letter-spacing: -.02em; }
    .brand-name span { color: var(--blue); }
    .pills { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .pill { background: var(--card); border: 1.5px solid var(--line); border-radius: 999px; padding: 6px 14px; font-size: 12px; color: var(--muted); font-weight: 600; display: inline-flex; gap: 7px; align-items: center; }
    .pill b { color: var(--ink); font-weight: 800; font-size: 13px; }
    .pill.hot { background: #fffbeb; border-color: #fde68a; }
    .pill.hot b { color: #b45309; }
    .prog-top { display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-weight: 700; color: var(--faint); text-transform: uppercase; letter-spacing: .1em; margin-bottom: 9px; padding: 0 2px; }
    .prog-top .cur { color: var(--blue); }
    .segs { display: flex; gap: 6px; margin-bottom: 22px; }
    .seg { flex: 1; height: 6px; border-radius: 4px; background: #e3e6ef; }
    .seg.ok { background: var(--green); }
    .seg.half { background: var(--amber); }
    .seg.bad { background: #f87171; }
    .seg.now { background: linear-gradient(90deg, #4f46e5, #7c3aed); }
    .topic-wrap { text-align: center; margin-bottom: 6px; }
    .qs-topic { display: inline-block; font-size: 11px; font-weight: 700; color: var(--blue); background: var(--blue-l); padding: 6px 16px; border-radius: 999px; text-transform: uppercase; letter-spacing: .09em; margin: 0 4px; }
    .qs-topic.spec { color: var(--violet); background: var(--violet-l); }
    .qs-sub { text-align: center; font-size: 13px; color: var(--muted); margin: 8px 0 20px 0; font-weight: 500; }
    .col-hd { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; padding: 12px 14px; background: var(--card); border: 1.5px solid var(--line); border-radius: 16px; }
    .col-num { width: 32px; height: 32px; border-radius: 10px; background: var(--blue); color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 900; flex-shrink: 0; }
    .col-num.right { background: var(--violet); }
    .col-title { font-size: 14.5px; font-weight: 800; line-height: 1.25; }
    .col-sub { font-size: 12px; color: var(--muted); margin-top: 2px; font-weight: 500; }
    .col-state { margin-left: auto; font-size: 10.5px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; background: #f1f5f9; color: var(--faint); }
    .col-state.wait { background: var(--blue-l); color: var(--blue-d); }
    .col-state.done-ok { background: var(--green-l); color: #047857; }
    .col-state.done-no { background: var(--red-l); color: #b91c1c; }
    .locked { padding: 13px 15px; border-radius: 14px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; background: #f8f9fc; border: 1.5px dashed var(--line); animation: pop .3s ease both; }
    .locked-letter { width: 28px; height: 28px; border-radius: 8px; background: var(--blue-l); color: var(--blue-d); display: inline-flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; flex-shrink: 0; }
    .locked-text { font-size: 12.5px; color: var(--muted); font-weight: 600; line-height: 1.45; }
    .locked-text b { color: var(--ink); font-weight: 800; }
    .result-panel { padding: 13px 15px; border-radius: 14px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; animation: pop .3s ease both; }
    .result-ok { background: var(--green-l); border: 1.5px solid #6ee7b7; color: #065f46; }
    .result-no { background: var(--red-l); border: 1.5px solid #fca5a5; color: #991b1b; }
    .r-letter { width: 28px; height: 28px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; color: #fff; flex-shrink: 0; }
    .result-ok .r-letter { background: var(--green); } .result-no .r-letter { background: var(--red); }
    .result-text { font-size: 13px; font-weight: 600; line-height: 1.45; }
    .result-text b { font-weight: 800; }
    .rev { background: var(--card); border: 1.5px solid var(--line); border-radius: 14px; padding: 13px 15px; margin-bottom: 9px; animation: fadeUp .35s ease both; }
    .rev-top { display: flex; align-items: flex-start; gap: 11px; }
    .rev-ok { border-color: var(--green) !important; background: #f6fef9 !important; }
    .rev-pick-no { border-color: #fca5a5 !important; background: #fffafa !important; }
    .rev-letter { width: 24px; height: 24px; border-radius: 7px; background: #f1f5f9; color: var(--muted); font-size: 12px; font-weight: 900; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; }
    .rev-ok .rev-letter { background: var(--green); color: #fff; }
    .rev-pick-no .rev-letter { background: var(--red); color: #fff; }
    .rev-info { flex: 1; min-width: 0; }
    .rev-title { font-size: 12.8px; font-weight: 600; line-height: 1.45; }
    .rev-tags { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }
    .tag { font-size: 10px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; padding: 2px 8px; border-radius: 6px; }
    .tag.best { background: var(--green); color: #fff; } .tag.you { background: var(--blue-l); color: var(--blue-d); }
    .tag.you-no { background: var(--red-l); color: #b91c1c; }
    .rev-score { font-size: 13px; font-weight: 800; padding: 5px 10px; border-radius: 9px; white-space: nowrap; flex-shrink: 0; background: #f1f5f9; color: var(--muted); }
    .rev-ok .rev-score { background: var(--green); color: #fff; }
    .bar-track { position: relative; height: 8px; border-radius: 6px; background: #eef1f6; margin-top: 11px; overflow: hidden; }
    .bar-range { position: absolute; top: 0; bottom: 0; background: #c7d2fe; border-radius: 6px; transform-origin: left; animation: grow .6s ease both; }
    .bar-fill { position: absolute; top: 0; bottom: 0; left: 0; background: #cbd5e1; border-radius: 6px; transform-origin: left; animation: grow .6s ease both; }
    .rev-ok .bar-fill { background: linear-gradient(90deg, #34d399, #10b981); }
    .bar-dot { position: absolute; top: -1px; width: 10px; height: 10px; border-radius: 50%; background: var(--blue); border: 2px solid #fff; transform: translateX(-50%); box-shadow: 0 1px 3px rgba(0,0,0,.25); }
    .rev-ok .bar-dot { background: #047857; }
    .rev-meta { font-size: 10.8px; color: var(--faint); margin-top: 7px; font-weight: 500; display: flex; justify-content: space-between; }
    .paper-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 7px 4px; border-bottom: 1px solid var(--line); font-size: 12px; }
    .paper-row:last-child { border-bottom: none; }
    .paper-row a { color: var(--blue-d); text-decoration: none; font-weight: 600; }
    .paper-row a:hover { text-decoration: underline; }
    .paper-score { color: var(--muted); font-weight: 700; white-space: nowrap; flex-shrink: 0; margin-left: 10px; }
    .sec-hd { font-size: 11px; font-weight: 800; color: var(--faint); text-transform: uppercase; letter-spacing: .12em; margin: 14px 0 10px 0; }
    .round-sum { text-align: center; margin: 18px auto 0 auto; max-width: 520px; padding: 14px 18px; border-radius: 16px; background: var(--card); border: 1.5px solid var(--line); animation: pop .3s ease both; }
    .round-sum .rs-t { font-size: 15px; font-weight: 800; }
    .round-sum .rs-s { font-size: 12.5px; color: var(--muted); margin-top: 3px; font-weight: 500; }
    .hero { background: var(--card); border: 1.5px solid var(--line); border-radius: 24px; padding: 44px 32px 34px 32px; text-align: center; margin: 14px auto 8px auto; max-width: 760px; box-shadow: 0 10px 34px rgba(15,23,42,.06); animation: fadeUp .4s ease both; }
    .hero-badge { display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--blue); background: var(--blue-l); padding: 6px 14px; border-radius: 999px; margin-bottom: 18px; }
    .hero-title { font-size: 40px; font-weight: 900; letter-spacing: -.035em; line-height: 1.08; margin-bottom: 12px; }
    .hero-title span { background: linear-gradient(90deg, #4f46e5, #7c3aed); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent; }
    .hero-sub { font-size: 15px; color: var(--muted); line-height: 1.65; max-width: 540px; margin: 0 auto 28px auto; }
    .steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: left; margin-bottom: 8px; }
    .step { background: #fafbfe; border: 1.5px solid var(--line); border-radius: 16px; padding: 16px; }
    .step-n { width: 26px; height: 26px; border-radius: 8px; background: var(--blue-l); color: var(--blue); font-weight: 900; font-size: 13px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 10px; }
    .step-t { font-size: 13.5px; font-weight: 800; margin-bottom: 3px; }
    .step-d { font-size: 12.3px; color: var(--muted); line-height: 1.5; }
    .hero-foot { font-size: 12px; color: var(--faint); margin-top: 16px; font-weight: 500; }
    .done { background: var(--card); border: 1.5px solid var(--line); border-radius: 24px; padding: 38px 30px 30px 30px; text-align: center; margin: 14px auto 10px auto; max-width: 680px; box-shadow: 0 10px 34px rgba(15,23,42,.06); animation: fadeUp .4s ease both; }
    .done-ring { width: 118px; height: 118px; border-radius: 50%; margin: 0 auto 18px auto; display: flex; align-items: center; justify-content: center; }
    .done-ring-in { width: 92px; height: 92px; border-radius: 50%; background: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .done-ring-v { font-size: 26px; font-weight: 900; line-height: 1; color: var(--ink); }
    .done-ring-l { font-size: 9px; font-weight: 800; letter-spacing: .08em; color: var(--faint); margin-top: 4px; text-transform: uppercase; text-align: center; }
    .done-rank { font-size: 12px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--blue); margin-bottom: 6px; }
    .done-title { font-size: 26px; font-weight: 900; letter-spacing: -.025em; margin-bottom: 6px; }
    .done-sub { font-size: 14px; color: var(--muted); margin-bottom: 10px; line-height: 1.55; }
    .done-joke { font-size: 13.5px; color: var(--blue-d); background: var(--blue-l); border-radius: 12px; padding: 10px 14px; margin-bottom: 20px; font-weight: 600; line-height: 1.5; }
    .done-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
    .done-stat { background: #fafbfe; border: 1.5px solid var(--line); border-radius: 14px; padding: 14px 6px; }
    .done-stat-v { font-size: 22px; font-weight: 900; color: var(--blue); line-height: 1; }
    .done-stat-l { font-size: 10px; color: var(--faint); text-transform: uppercase; letter-spacing: .09em; font-weight: 800; margin-top: 7px; }
    .share-row { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
    .share-btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 12px; font-size: 13px; font-weight: 700; text-decoration: none; border: 1.5px solid var(--line); background: #fff; transition: all .16s ease; }
    .share-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(15,23,42,.1); }
    .share-btn.x { background: #000; border-color: #000; }
    .share-btn.li { background: #0a66c2; border-color: #0a66c2; }
    .share-btn.x, .share-btn.li { color: #ffffff !important; }
    .share-btn.x *, .share-btn.li * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    .hist { text-align: left; margin-top: 4px; }
    .hist-row { display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: 11px; background: #fafbfe; border: 1.5px solid var(--line); margin-bottom: 6px; font-size: 12.5px; font-weight: 600; }
    .hist-n { color: var(--faint); font-weight: 800; min-width: 22px; }
    .hist-topic { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .chip { font-size: 10.5px; font-weight: 800; padding: 3px 9px; border-radius: 7px; letter-spacing: .04em; }
    .chip.ok { background: var(--green-l); color: #047857; } .chip.no { background: var(--red-l); color: #b91c1c; }
    .done-credit { margin-top: 24px; padding-top: 20px; border-top: 1.5px solid var(--line); font-size: 12.5px; color: var(--muted); line-height: 1.8; }
    .done-credit b { color: var(--ink); font-weight: 700; }
    .brand-mark, .brand-mark *, .col-num, .col-num *, .r-letter, .r-letter *, .rev-ok .rev-letter, .rev-ok .rev-letter *, .rev-pick-no .rev-letter, .rev-pick-no .rev-letter *, .rev-ok .rev-score, .rev-ok .rev-score *, .tag.best, .tag.best *, div[class*="st-key-cta_"] button, div[class*="st-key-cta_"] button * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    .chip.ok, .chip.ok * { color: #047857 !important; }
    .chip.no, .chip.no * { color: #b91c1c !important; }
    .tag.you, .tag.you * { color: #4338ca !important; }
    .tag.you-no, .tag.you-no * { color: #b91c1c !important; }
    .col-state.done-ok, .col-state.done-ok * { color: #047857 !important; }
    .col-state.done-no, .col-state.done-no * { color: #b91c1c !important; }
    .col-state.wait, .col-state.wait * { color: #4338ca !important; }
    .rev-meta, .rev-meta * { color: var(--faint) !important; }
    .paper-score, .paper-score * { color: var(--muted) !important; }
    .paper-row a, .paper-row a * { color: var(--blue-d) !important; }
    .done-ring-in { position: relative; z-index: 1; }
    .done-title, .done-rank, .done-joke, .done-stats, .share-row, .hist, .done-credit { position: relative; z-index: 1; }
    @media (max-width: 720px) {
        .hero-title { font-size: 30px; } .steps { grid-template-columns: 1fr; }
        .done-stats { grid-template-columns: repeat(2, 1fr); } .hero { padding: 32px 18px 26px 18px; }
    }
</style>
""", unsafe_allow_html=True)


def _find_file(filename):
    for p in (filename, os.path.join("hf_deploy", filename)):
        if os.path.exists(p):
            return p
    return filename


@st.cache_data(show_spinner=False)
def load_questions(version="v27"):
    with open(_find_file("questions.json"), "r") as f:
        return json.load(f)


def load_images(version="v27"):
    try:
        path = _find_file("images.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


questions = load_questions("v27")
images_b64 = load_images("v27")

for q in questions:
    q.setdefault("specificity", "Focused")
    for opt in q["options"]:
        opt.setdefault("score_min", opt.get("avg_rating", 0))
        opt.setdefault("score_max", opt.get("avg_rating", 0))
        opt.setdefault("num_reviews", 0)
        opt.setdefault("num_papers", 0)
        opt.setdefault("std", 0.0)
        opt.setdefault("papers", [])
        opt.setdefault("node_id", None)
    q.setdefault("variance_correct", q["correct_option"])

ALL_SPECIFICITIES = sorted({q["specificity"] for q in questions})
TOTAL_TARGET = min(5, len(questions))
N_OPTIONS_IN_DATA = len(questions[0]["options"]) if questions else 2
RANDOM_GUESS_P = 1.0 / N_OPTIONS_IN_DATA


def esc(x):
    return html.escape(str(x))


def _install_viewer_js():
    """Install custom zoom viewer + click handlers. Also force-removes Streamlit's native fullscreen button."""
    components.html("""
    <html><head><style>html,body{margin:0;padding:0;background:transparent;overflow:hidden;height:0;}</style></head><body>
    <script>
      (function() {
        var pd = window.parent.document;

        // ---------- 1) Kill Streamlit native fullscreen button ----------
        function killNativeFS() {
          var sels = [
            '[data-testid="StyledFullScreenButton"]',
            '[data-testid="stImage"] button',
            'button[title="View fullscreen"]',
            'button[title="Fullscreen"]',
            'button[aria-label="View fullscreen"]',
            'button[aria-label="Fullscreen"]',
            'button[aria-label="Full screen"]',
            '[class*="FullScreenButton"]',
            '[class*="fullscreenButton"]'
          ];
          sels.forEach(function(s) {
            pd.querySelectorAll(s).forEach(function(el) {
              el.style.setProperty('display', 'none', 'important');
              el.style.setProperty('visibility', 'hidden', 'important');
              el.style.setProperty('opacity', '0', 'important');
              el.style.setProperty('pointer-events', 'none', 'important');
              el.style.setProperty('width', '0', 'important');
              el.style.setProperty('height', '0', 'important');
              el.remove();
            });
          });
        }
        killNativeFS();

        // ---------- 2) Custom zoom viewer ----------
        if (!pd.getElementById('fsViewerGlobal')) {
          var v = pd.createElement('div');
          v.id = 'fsViewerGlobal';
          v.style.cssText = 'display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(255,255,255,0.98);z-index:2147483647;align-items:center;justify-content:center;cursor:zoom-out;';

          var img = pd.createElement('img');
          img.id = 'fsImgGlobal';
          img.style.cssText = 'max-width:min(1024px,88vw);max-height:min(1024px,88vh);width:auto;height:auto;border-radius:10px;box-shadow:0 12px 48px rgba(15,23,42,.35);background:#ffffff;display:block;object-fit:contain;';

          var cb = pd.createElement('button');
          cb.id = 'fsCloseGlobal';
          cb.type = 'button';
          cb.setAttribute('aria-label', 'Close');
          cb.textContent = '\\u2715';
          cb.style.cssText = 'position:fixed;top:76px;right:14px;width:52px;height:52px;border-radius:50%;border:none;background:#0f172a;font-size:24px;font-weight:900;font-family:Inter,-apple-system,sans-serif;cursor:pointer;line-height:1;box-shadow:0 6px 20px rgba(15,23,42,.45);display:flex;align-items:center;justify-content:center;padding:0;z-index:2147483647;transition:background .15s ease;';
          cb.style.setProperty('color', '#ffffff', 'important');
          cb.style.setProperty('-webkit-text-fill-color', '#ffffff', 'important');

          cb.onmouseenter = function() { cb.style.background = '#334155'; };
          cb.onmouseleave = function() { cb.style.background = '#0f172a'; };
          cb.onclick = function(e) { e.stopPropagation(); v.style.display = 'none'; };

          v.appendChild(img);
          v.appendChild(cb);
          v.onclick = function(e) { if (e.target === v || e.target === img) v.style.display = 'none'; };
          pd.body.appendChild(v);

          pd.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && v.style.display === 'flex') v.style.display = 'none';
          });

          window.__openFs__ = function(src) {
            img.src = src;
            v.style.display = 'flex';
          };
        }

        // ---------- 3) Attach click-to-zoom on every thumbnail ----------
        function attach() {
          killNativeFS();
          pd.querySelectorAll('[data-testid="stImage"] img').forEach(function(el) {
            if (el.dataset.fsAttached === '1') return;
            el.dataset.fsAttached = '1';
            el.style.cursor = 'zoom-in';
            el.addEventListener('click', function(ev) {
              ev.preventDefault();
              ev.stopPropagation();
              var src = el.currentSrc || el.src;
              if (!src) return;
              window.__openFs__(src);
            }, true);
          });
        }
        attach();
        new MutationObserver(function() { attach(); }).observe(pd.body, { childList: true, subtree: true });
        setInterval(attach, 500);
      })();
    </script>
    </body></html>
    """, height=0, width=0)


def show_image(opt):
    """Centered image via st.image. Click opens custom 1024x1024 zoom viewer."""
    try:
        node_id = opt.get("node_id")
        if not node_id:
            return
        b64 = images_b64.get(node_id)
        if not b64 or not isinstance(b64, str) or len(b64) < 100:
            return

        if b64.startswith("data:") and "," in b64[:64]:
            b64 = b64.split(",", 1)[1]

        img_bytes = base64.b64decode(b64)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.image(img_bytes, use_container_width=True)
    except Exception:
        return


def new_deck():
    by_spec = {s: [i for i, q in enumerate(questions) if q["specificity"] == s] for s in ALL_SPECIFICITIES}
    for lst in by_spec.values():
        random.shuffle(lst)
    deck = []
    i = 0
    specs_cycle = list(ALL_SPECIFICITIES)
    random.shuffle(specs_cycle)
    while len(deck) < TOTAL_TARGET and any(by_spec[s] for s in specs_cycle):
        s = specs_cycle[i % len(specs_cycle)]
        if by_spec[s]:
            deck.append(by_spec[s].pop())
        i += 1
    return deck


def reset_game():
    st.session_state.deck = new_deck()
    st.session_state.left_answered = False
    st.session_state.right_answered = False
    st.session_state.left_selected = None
    st.session_state.right_selected = None
    st.session_state.round_ok = {"left": None, "right": None}
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.questions_completed = 0
    st.session_state.celebrated = False
    st.session_state.play_chime = False


if "stage" not in st.session_state:
    st.session_state.stage = "start"
    reset_game()


def current_question():
    return questions[st.session_state.deck[st.session_state.questions_completed]]


def answer(side, opt_id):
    q = current_question()
    correct = q["correct_option"] if side == "left" else q["variance_correct"]
    ok = opt_id == correct
    st.session_state[f"{side}_selected"] = opt_id
    st.session_state[f"{side}_answered"] = True
    st.session_state.round_ok[side] = ok
    st.session_state.total += 1
    if ok:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
        st.session_state.play_chime = True
    else:
        st.session_state.streak = 0


def start_game():
    reset_game()
    st.session_state.stage = "play"


def next_question():
    q = current_question()
    st.session_state.history.append({
        "specificity": q["specificity"],
        "left": bool(st.session_state.round_ok["left"]),
        "right": bool(st.session_state.round_ok["right"]),
    })
    st.session_state.questions_completed += 1
    st.session_state.left_answered = False
    st.session_state.right_answered = False
    st.session_state.left_selected = None
    st.session_state.right_selected = None
    st.session_state.round_ok = {"left": None, "right": None}
    if st.session_state.questions_completed >= TOTAL_TARGET:
        st.session_state.stage = "done"


def binom_percentile(k, n, p=RANDOM_GUESS_P):
    if n == 0:
        return 0.0
    cdf = sum(math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(0, k + 1))
    return round(cdf * 100, 1)


def funny_comment(pct, score, total):
    if total == 0:
        return ""
    if pct < 20:
        return "Statistically remarkable. Go buy a lottery ticket, your luck is clearly reserved for other things today."
    if pct < 45:
        return "Reviewer scores are chaos incarnate, and you have proven it beyond reasonable doubt."
    if pct < 60:
        return "Right around what a coin flip would get you. Democratic, in a way."
    if pct < 80:
        return "Solid instincts. You would survive at least one round of peer review yourself."
    return "Suspiciously good. Are you secretly an area chair?"


def result_panel(ok, msg):
    cls = "result-panel result-ok flash-ok" if ok else "result-panel result-no"
    return (f'<div class="{cls}">'
            f'<span class="r-letter">{"&#10003;" if ok else "&#10005;"}</span>'
            f'<span class="result-text">{msg}</span></div>')


def locked_panel(sel_letter):
    return (f'<div class="locked"><span class="locked-letter">{esc(sel_letter)}</span>'
            f'<span class="locked-text">Answer locked in - <b>waiting for the other question</b></span></div>')


def reveal_card(opt, mode, correct_id, picked_id, max_std):
    is_hi = opt["option_id"] == correct_id
    picked = opt["option_id"] == picked_id
    cls = "rev"
    if is_hi: cls += " rev-ok"
    elif picked: cls += " rev-pick-no"

    tags = ""
    if is_hi: tags += '<span class="tag best">Answer</span>'
    if picked: tags += '<span class="tag you">Your pick</span>' if is_hi else '<span class="tag you-no">Your pick</span>'
    tags_html = f'<div class="rev-tags">{tags}</div>' if tags else ""

    avg = float(opt["avg_rating"])
    if mode == "score":
        smin, smax = max(SCALE_MIN, float(opt["score_min"])), min(SCALE_MAX, float(opt["score_max"]))
        span = SCALE_MAX - SCALE_MIN
        badge = f"&#9733; {opt['avg_rating']}" if is_hi else f"{opt['avg_rating']}"
        pct = max(0, min(100, (avg - SCALE_MIN) / span * 100))
        rmin = max(0, min(100, (smin - SCALE_MIN) / span * 100))
        rw = max(0, min(100, (smax - SCALE_MIN) / span * 100)) - rmin
        bar = (f'<div class="bar-track"><div class="bar-range" style="left:{rmin:.1f}%;width:{max(rw, 1.5):.1f}%;"></div>'
               f'<div class="bar-dot" style="left:{pct:.1f}%;"></div></div>')
    else:
        badge = f"&#9733; std {opt['std']}" if is_hi else f"std {opt['std']}"
        pct = max(4, min(100, float(opt["std"]) / STD_SCALE_MAX * 100))
        bar = f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.1f}%;"></div></div>'

    meta = (f'<div class="rev-meta"><span>Scores {opt["score_min"]} to {opt["score_max"]}</span>'
            f'<span>{opt["num_papers"]} papers &middot; {opt["num_reviews"]} reviews</span></div>')

    return (f'<div class="{cls}"><div class="rev-top"><div class="rev-letter">{esc(opt["option_id"])}</div>'
            f'<div class="rev-info"><div class="rev-title">{esc(opt["title"])}</div>{tags_html}</div>'
            f'<div class="rev-score">{badge}</div></div>{bar}{meta}</div>')


def paper_detail_rows(opt):
    rows = ""
    for p in opt["papers"]:
        url = f"https://openreview.net/forum?id={p['paper_id']}"
        scores_str = ", ".join(str(s) for s in p.get("scores", [p.get("avg_rating")]))
        rows += (f'<div class="paper-row">'
                 f'<a href="{esc(url)}" target="_blank">{esc(p["title"])}</a>'
                 f'<span class="paper-score">{esc(scores_str)}</span>'
                 f'</div>')
    return rows


acc = (st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0


_install_viewer_js()


audio_js = f"""
<audio id="chime" src="data:audio/wav;base64,{BEEP_B64}"></audio>
<script>
  const chime = document.getElementById("chime");
  if (chime && {str(st.session_state.get("play_chime", False)).lower()}) {{
    chime.currentTime = 0;
    chime.play().catch(() => {{}});
  }}
</script>
"""
st.markdown(audio_js, unsafe_allow_html=True)
st.session_state.play_chime = False


try:
    with open(_find_file(BG_MUSIC_FILE), "rb") as music_file:
        music_b64 = base64.b64encode(music_file.read()).decode("utf-8")
except FileNotFoundError:
    music_b64 = ""

if music_b64:
    components.html(f"""
    <script>
      (function() {{
        const SRC = "data:audio/mpeg;base64,{music_b64}";
        const pd = window.parent.document;
        const top_doc = (function() {{
          try {{ return window.top.document; }} catch(e) {{ return pd; }}
        }})();

        let audio = pd.getElementById('bgmusic-global');
        if (!audio) {{
          audio = pd.createElement('audio');
          audio.id = 'bgmusic-global';
          audio.src = SRC;
          audio.loop = true;
          audio.preload = 'auto';
          audio.style.display = 'none';
          pd.body.appendChild(audio);
        }}

        let btn = pd.getElementById('bgmusic-btn');
        if (!btn) {{
          btn = pd.createElement('button');
          btn.id = 'bgmusic-btn';
          btn.innerHTML = '&#127925; Music';
          btn.style.cssText = 'position:fixed;top:14px;right:14px;z-index:2147483647;border-radius:999px;border:1.5px solid #e7e9f0;background:#fff;padding:8px 16px;font-weight:700;cursor:pointer;font-family:Inter,-apple-system,sans-serif;font-size:13px;box-shadow:0 2px 6px rgba(15,23,42,.08);color:#0f172a;transition:all .2s ease;line-height:1.2;';
          pd.body.appendChild(btn);
        }}

        let desiredOn = localStorage.getItem('bgmusic_on') !== '0';

        function renderBtn() {{
          if (!desiredOn) {{
            btn.innerHTML = '&#127925; Music';
            btn.style.background = '#fff';
            btn.style.borderColor = '#e7e9f0';
            btn.style.color = '#0f172a';
          }} else if (audio.paused) {{
            btn.innerHTML = '&#128264; Tap to start';
            btn.style.background = '#fef3c7';
            btn.style.borderColor = '#fcd34d';
            btn.style.color = '#92400e';
          }} else {{
            btn.innerHTML = '&#128266; Music On';
            btn.style.background = '#eef2ff';
            btn.style.borderColor = '#4f46e5';
            btn.style.color = '#4f46e5';
          }}
        }}

        if (btn._bgHandler) btn.removeEventListener('click', btn._bgHandler);
        btn._bgHandler = function(ev) {{
          ev.stopPropagation();
          if (desiredOn) {{
            desiredOn = false;
            audio.pause();
            localStorage.setItem('bgmusic_on', '0');
          }} else {{
            desiredOn = true;
            localStorage.setItem('bgmusic_on', '1');
            audio.play().catch(function(){{}});
          }}
          renderBtn();
        }};
        btn.addEventListener('click', btn._bgHandler);

        if (!audio._bgTick) {{
          audio._bgTick = setInterval(function() {{
            if (!audio.paused) {{
              try {{ localStorage.setItem('bgmusic_time', audio.currentTime.toFixed(2)); }} catch (e) {{}}
            }}
          }}, 1000);
        }}

        const savedTime = parseFloat(localStorage.getItem('bgmusic_time') || '0');
        if (savedTime > 0 && audio.currentTime < 1) {{
          try {{ audio.currentTime = savedTime; }} catch (e) {{}}
        }}

        function tryPlay() {{
          if (!desiredOn || !audio.paused) return;
          audio.play().then(function() {{
            renderBtn();
          }}).catch(function() {{
            renderBtn();
          }});
        }}

        if (desiredOn) {{
          tryPlay();
          const events = ['click', 'keydown', 'touchstart', 'pointerdown',
                          'mousedown', 'scroll', 'wheel', 'mousemove', 'focus', 'visibilitychange'];
          events.forEach(function(ev) {{
            try {{ pd.addEventListener(ev, tryPlay, true); }} catch (e) {{}}
            try {{ window.addEventListener(ev, tryPlay, true); }} catch (e) {{}}
            try {{ top_doc.addEventListener(ev, tryPlay, true); }} catch (e) {{}}
          }});
          let tries = 0;
          const poll = setInterval(function() {{
            tries++;
            tryPlay();
            if (!audio.paused || tries > 300) clearInterval(poll);
          }}, 400);
        }}

        audio.addEventListener('play', renderBtn);
        audio.addEventListener('pause', renderBtn);

        renderBtn();
      }})();
    </script>
    """, height=0, width=0)


if st.session_state.stage == "start":
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">NeurIPS 2025 &middot; Real peer reviews &middot; COMPREHEND tree</div>
        <div class="hero-title">Can you predict<br><span>the reviewers?</span></div>
        <div class="hero-sub">
            Each round compares two research categories discovered by our hierarchy tree, from
            the same level of specificity. Guess which category scored highest, and which one
            split the reviewers the most.
        </div>
        <div class="steps">
            <div class="step"><div class="step-n">1</div><div class="step-t">Pick the top score</div>
                <div class="step-d">Which category earned the highest average rating?</div></div>
            <div class="step"><div class="step-n">2</div><div class="step-t">Spot the disagreement</div>
                <div class="step-d">Which category had the widest spread between reviewers?</div></div>
            <div class="step"><div class="step-n">3</div><div class="step-t">See where you rank</div>
                <div class="step-d">{TOTAL_TARGET} rounds, {TOTAL_TARGET * 2} guesses. Get a percentile at the end.</div></div>
        </div>
        <div class="hero-foot">Takes about 2 minutes</div>
    </div>
    """, unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1.4, 1])
    with c:
        st.button("Start Challenge", key="cta_start", on_click=start_game, use_container_width=True)


elif st.session_state.stage == "done":
    pct = binom_percentile(st.session_state.score, st.session_state.total)
    color = "#10b981" if pct >= 75 else ("#4f46e5" if pct >= 50 else "#f59e0b")
    joke = funny_comment(pct, st.session_state.score, st.session_state.total)
    rows = ""
    for i, h in enumerate(st.session_state.history, 1):
        l = '<span class="chip ok">Score &#10003;</span>' if h["left"] else '<span class="chip no">Score &#10005;</span>'
        r = '<span class="chip ok">Disagree &#10003;</span>' if h["right"] else '<span class="chip no">Disagree &#10005;</span>'
        rows += (f'<div class="hist-row"><span class="hist-n">{i}</span>'
                 f'<span class="hist-topic">{esc(h["specificity"])} round</span>{l}{r}</div>')

    share_text = html.escape(
        f"I scored {pct:.0f}th percentile vs. random guessing on the Review Score Challenge "
        f"({st.session_state.score}/{st.session_state.total} correct). Can you beat me?"
    )
    share_x = f"https://twitter.com/intent/tweet?text={share_text}"
    share_li = "https://www.linkedin.com/sharing/share-offsite/?url=" + html.escape("https://huggingface.co/spaces")

    st.markdown(f"""
    <div class="done">
        <div class="done-ring" style="background: conic-gradient({color} {pct * 3.6:.0f}deg, #eceff5 0deg);">
            <div class="done-ring-in"><div class="done-ring-v">{pct:.0f}%</div><div class="done-ring-l">vs. random<br>guessing</div></div>
        </div>
        <div class="done-rank">You outscored</div>
        <div class="done-title">{pct:.0f}% of random guessers</div>
        <div class="done-sub">Based on a {N_OPTIONS_IN_DATA}-option random-choice baseline across your {st.session_state.total} answers.</div>
        <div class="done-joke">{joke}</div>
        <div class="done-stats">
            <div class="done-stat"><div class="done-stat-v">{st.session_state.score}/{st.session_state.total}</div><div class="done-stat-l">Correct</div></div>
            <div class="done-stat"><div class="done-stat-v">{acc:.0f}%</div><div class="done-stat-l">Accuracy</div></div>
            <div class="done-stat"><div class="done-stat-v">{st.session_state.best_streak}</div><div class="done-stat-l">Best streak</div></div>
            <div class="done-stat"><div class="done-stat-v">{sum(1 for h in st.session_state.history if h["left"] and h["right"])}</div><div class="done-stat-l">Perfect rounds</div></div>
        </div>
        <div class="share-row">
            <a class="share-btn x" href="{share_x}" target="_blank">Share on X</a>
            <a class="share-btn li" href="{share_li}" target="_blank">Share on LinkedIn</a>
        </div>
        <div class="hist"><div class="sec-hd" style="text-align:center;">Round breakdown</div>{rows}</div>
        <div class="done-credit">
            Built by <b>Waqar Ali</b>, supervised by <b>Haw-Shiuan Chang</b><br>
            NeurIPS 2025 peer review dataset &middot; COMPREHEND 512-paper hierarchy tree<br>
            Thanks for playing.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if pct >= 80 and not st.session_state.celebrated:
        st.session_state.celebrated = True
        st.balloons()

    _, c, _ = st.columns([1, 1.4, 1])
    with c:
        st.button("Play Again", key="cta_again", on_click=start_game, use_container_width=True)


else:
    q = current_question()
    qn = st.session_state.questions_completed
    both_answered = st.session_state.left_answered and st.session_state.right_answered

    hot = " hot" if st.session_state.streak >= 3 else ""
    st.markdown(f"""
    <div class="hd">
        <div class="brand"><div class="brand-mark">&#9670;</div><div class="brand-name">Review Score <span>Challenge</span></div></div>
        <div class="pills">
            <span class="pill">Score <b>{st.session_state.score}/{st.session_state.total}</b></span>
            <span class="pill">Accuracy <b>{acc:.0f}%</b></span>
            <span class="pill{hot}">Streak <b>{st.session_state.streak}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    segs = ""
    for i in range(TOTAL_TARGET):
        if i < len(st.session_state.history):
            h = st.session_state.history[i]
            c = "ok" if (h["left"] and h["right"]) else ("half" if (h["left"] or h["right"]) else "bad")
        elif i == qn:
            c = "now"
        else:
            c = ""
        segs += f'<div class="seg {c}"></div>'
    st.markdown(f"""
    <div class="prog-top"><span class="cur">Round {qn + 1} of {TOTAL_TARGET}</span><span>Answer both questions</span></div>
    <div class="segs">{segs}</div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="topic-wrap"><span class="qs-topic spec">{esc(q["specificity"])} categories</span></div>'
        f'<div class="qs-sub">{N_OPTIONS_IN_DATA} categories from the same level of our research hierarchy. Trust your instincts.</div>',
        unsafe_allow_html=True)

    max_std = max(float(o["std"]) for o in q["options"])
    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        if both_answered:
            s_cls = "done-ok" if st.session_state.round_ok["left"] else "done-no"
            s_txt = "Correct" if st.session_state.round_ok["left"] else "Missed"
        elif st.session_state.left_answered:
            s_cls, s_txt = "wait", "Locked in"
        else:
            s_cls, s_txt = "", "Your turn"
        st.markdown(f"""
        <div class="col-hd fx">
            <div class="col-num">1</div>
            <div><div class="col-title">Highest score</div><div class="col-sub">Which category scored highest?</div></div>
            <div class="col-state {s_cls}">{s_txt}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.left_answered:
            for opt in q["options"]:
                show_image(opt)
                label = f"{opt['option_id']}     {opt['title']}"
                st.button(label, key=f"lopt_{opt['option_id']}_{q['question_id']}", use_container_width=True,
                          on_click=answer, args=("left", opt["option_id"]))
        elif not both_answered:
            st.markdown(locked_panel(st.session_state.left_selected), unsafe_allow_html=True)
        else:
            correct = q["correct_option"]
            sel = st.session_state.left_selected
            ok = sel == correct
            msg = (f'Correct. <b>{esc(correct)}</b> scored highest at <b>{esc(q["correct_rating"])}</b>.' if ok else
                   f'You picked <b>{esc(sel)}</b>. Correct was <b>{esc(correct)}</b> at <b>{esc(q["correct_rating"])}</b>.')
            st.markdown(result_panel(ok, msg), unsafe_allow_html=True)
            st.markdown(f'<div class="sec-hd">Score reveal &middot; scale {SCALE_MIN:.0f} to {SCALE_MAX:.0f}</div>', unsafe_allow_html=True)
            for opt in q["options"]:
                show_image(opt)
                st.markdown(reveal_card(opt, "score", correct, sel, max_std), unsafe_allow_html=True)
                with st.expander(f"See details - {opt['option_id']} ({opt['num_papers']} papers)"):
                    st.markdown(paper_detail_rows(opt), unsafe_allow_html=True)

    with right_col:
        if both_answered:
            s_cls = "done-ok" if st.session_state.round_ok["right"] else "done-no"
            s_txt = "Correct" if st.session_state.round_ok["right"] else "Missed"
        elif st.session_state.right_answered:
            s_cls, s_txt = "wait", "Locked in"
        else:
            s_cls, s_txt = "", "Your turn"
        st.markdown(f"""
        <div class="col-hd fx">
            <div class="col-num right">2</div>
            <div><div class="col-title">Disagreement</div><div class="col-sub">Which had the most reviewer disagreement?</div></div>
            <div class="col-state {s_cls}">{s_txt}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.right_answered:
            for opt in q["options"]:
                show_image(opt)
                label = f"{opt['option_id']}     {opt['title']}"
                st.button(label, key=f"ropt_{opt['option_id']}_{q['question_id']}", use_container_width=True,
                          on_click=answer, args=("right", opt["option_id"]))
        elif not both_answered:
            st.markdown(locked_panel(st.session_state.right_selected), unsafe_allow_html=True)
        else:
            vcorrect = q["variance_correct"]
            sel = st.session_state.right_selected
            ok = sel == vcorrect
            msg = (f'Correct. <b>{esc(vcorrect)}</b> had the highest disagreement.' if ok else
                   f'You picked <b>{esc(sel)}</b>. Correct was <b>{esc(vcorrect)}</b>.')
            st.markdown(result_panel(ok, msg), unsafe_allow_html=True)
            st.markdown('<div class="sec-hd">Disagreement reveal &middot; standard deviation</div>', unsafe_allow_html=True)
            for opt in q["options"]:
                show_image(opt)
                st.markdown(reveal_card(opt, "std", vcorrect, sel, max_std), unsafe_allow_html=True)
                with st.expander(f"See details - {opt['option_id']} ({opt['num_papers']} papers)"):
                    st.markdown(paper_detail_rows(opt), unsafe_allow_html=True)

    if both_answered:
        n_ok = int(bool(st.session_state.round_ok["left"])) + int(bool(st.session_state.round_ok["right"]))
        title = {2: "Perfect round", 1: "One out of two", 0: "Tough one"}[n_ok]
        sub = {2: "Both guesses landed. Keep the streak going.",
               1: "Half right. Reviewers are unpredictable.",
               0: "Nobody sees these coming. Shake it off."}[n_ok]
        st.markdown(f'<div class="round-sum"><div class="rs-t">{title} &middot; +{n_ok}</div><div class="rs-s">{sub}</div></div>',
                    unsafe_allow_html=True)
        is_last = qn + 1 >= TOTAL_TARGET
        _, mid, _ = st.columns([1, 1.6, 1])
        with mid:
            st.button("See Results" if is_last else "Next Question", key=f"cta_next_{q['question_id']}",
                      on_click=next_question, use_container_width=True)
