
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import html



conn = sqlite3.connect("splitmate.db", check_same_thread=False)

cursor = conn.cursor()






cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")




cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT NOT NULL,
    amount REAL NOT NULL,
    paid_by TEXT NOT NULL
)
""")




cursor.execute("""
CREATE TABLE IF NOT EXISTS expense_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    share_amount REAL NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES expenses(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS settlements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer TEXT NOT NULL,
    receiver TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT DEFAULT 'Pending'
)
""")
conn.commit()

st.set_page_config(
    page_title="SplitMate",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
:root {
    --ink: #202344;
    --muted: #68708f;
    --purple: #7048e8;
    --indigo: #5146c8;
    --blue: #3478e5;
    --teal: #10a992;
    --surface: rgba(255, 255, 255, 0.95);
    --line: #e8ebf5;
    --bg-soft: #f4f7fb;
    --bg-glow: rgba(92, 124, 239, 0.08);
    --shadow-soft: 0 10px 26px rgba(39, 45, 85, 0.08);
    --shadow-card: 0 14px 28px rgba(39, 45, 85, 0.06);
}

.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at top left, rgba(80, 111, 245, 0.08), transparent 32rem),
        radial-gradient(circle at top right, rgba(19, 169, 146, 0.07), transparent 28rem),
        linear-gradient(180deg, #f8faff 0%, #f3f7fc 100%);
    font-family: Aptos, 'Segoe UI', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: rgba(247, 250, 255, 0.75);
    backdrop-filter: blur(8px);
}

.block-container {
    max-width: 1440px;
    padding: 2.2rem 3rem 3.5rem;
    background: transparent;
}

[data-testid="stMain"] > div {
    background: transparent;
}

.stApp [data-testid="stVerticalBlock"] {
    gap: 1.1rem;
}

h1, h2, h3, [data-testid="stMetricValue"] {
    font-family: Aptos, 'Segoe UI', sans-serif;
    color: var(--ink);
    letter-spacing: -0.035em;
}

h1 {
    font-weight: 800;
}

h2, h3 {
    font-weight: 700;
}

.stApp p, .stApp label, .stApp li {
    color: #38405f;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

[data-testid="stSidebar"] {
    background: linear-gradient(155deg, #30236f 0%, #4939a7 54%, #245a9c 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.13);
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #fff;
}

[data-testid="stSidebar"] h1 {
    font-size: 1.35rem;
    letter-spacing: -0.025em;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: rgba(255, 255, 255, 0.82);
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    color: #29264b;
    background: #fff;
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 0.75rem;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #5146c8;
}

[data-testid="stMetric"] {
    min-height: 7rem;
    padding: 1.15rem 1.3rem;
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 3px solid var(--purple);
    border-radius: 1rem;
    box-shadow: 0 8px 24px rgba(37, 39, 86, 0.07);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #30286f;
    font-weight: 800;
}

.dashboard-metric-card {
    min-height: 7.25rem;
    padding: 1.2rem 1.25rem;
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.28);
    border-radius: 1rem;
    box-shadow: 0 10px 24px rgba(37, 39, 86, 0.14);
}

.dashboard-metric-card p {
    margin: 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    font-weight: 600;
}

.dashboard-metric-card strong {
    display: block;
    margin-top: 0.55rem;
    color: #fff;
    font-size: clamp(1.35rem, 2vw, 1.9rem);
    font-weight: 800;
    letter-spacing: -0.035em;
    line-height: 1.2;
    overflow-wrap: anywhere;
}

.dashboard-metric-purple {
    background: linear-gradient(135deg, #7550e8, #4938ad);
}

.dashboard-metric-blue {
    background: linear-gradient(135deg, #4388ee, #3156bd);
}

.dashboard-metric-teal {
    background: linear-gradient(135deg, #18bba2, #078c91);
}

.dashboard-metric-coral {
    background: linear-gradient(135deg, #f0798a, #bd4d8c);
}

.dashboard-balance-card,
.dashboard-payment-card {
    margin: 0.35rem 0 0.7rem;
    padding: 1rem 1.1rem;
    background: #fff;
    border: 1px solid var(--line);
    border-left: 4px solid var(--blue);
    border-radius: 0.9rem;
    box-shadow: 0 5px 16px rgba(37, 39, 86, 0.07);
}

.dashboard-balance-card p,
.dashboard-payment-card p {
    margin: 0;
}

.dashboard-balance-card strong,
.dashboard-payment-card strong {
    color: var(--ink);
    font-size: 1rem;
}

.dashboard-balance-card span,
.dashboard-payment-card span {
    color: var(--muted);
    font-size: 0.9rem;
}

.dashboard-balance-card em {
    display: block;
    margin-top: 0.3rem;
    color: var(--ink);
    font-size: 1.2rem;
    font-style: normal;
    font-weight: 800;
}

.dashboard-balance-receive {
    background: linear-gradient(120deg, #f0fbf8, #fff);
    border-left-color: var(--teal);
}

.dashboard-balance-pay {
    background: linear-gradient(120deg, #fff5f5, #fff);
    border-left-color: #e26b82;
}

.dashboard-balance-settled {
    background: linear-gradient(120deg, #f3f2ff, #fff);
    border-left-color: var(--purple);
}

.dashboard-payment-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    border-left-color: var(--purple);
}

.dashboard-payment-amount {
    flex-shrink: 0;
    padding: 0.4rem 0.65rem;
    color: #245caa;
    background: #edf4ff;
    border-radius: 0.65rem;
    font-weight: 800;
}

.dashboard-chart-title {
    margin-bottom: 0.6rem;
    color: var(--ink);
    font-size: 1.25rem;
    font-weight: 700;
}

.group-member-shell {
    margin-bottom: 1.2rem;
    padding: 1.2rem 1.35rem;
    background: linear-gradient(135deg, rgba(112, 72, 232, 0.08), rgba(52, 120, 229, 0.06), rgba(16, 169, 146, 0.05));
    border: 1px solid rgba(123, 101, 216, 0.12);
    border-radius: 1.3rem;
    box-shadow: 0 14px 32px rgba(55, 55, 110, 0.06);
}

.group-member-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.group-member-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.32rem 0.7rem;
    color: #2e7a6a;
    background: rgba(16, 169, 146, 0.12);
    border: 1px solid rgba(16, 169, 146, 0.12);
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.group-member-header h2 {
    margin: 0.5rem 0 0.25rem;
    color: #1d2441;
    font-size: clamp(2rem, 3vw, 2.8rem);
    letter-spacing: -0.05em;
}

.group-member-header p {
    margin: 0;
    color: #5d6789;
    font-size: 0.98rem;
}

.group-member-summary-card {
    min-width: 13.5rem;
    padding: 0.9rem 1rem;
    color: #fff;
    background: linear-gradient(135deg, #10a992 0%, #2d8ff5 44%, #6f4fe8 100%);
    border-radius: 1.1rem;
    box-shadow: 0 16px 26px rgba(82, 118, 191, 0.2);
}

.group-member-summary-card span,
.group-member-summary-card small {
    display: block;
    color: rgba(255, 255, 255, 0.82);
}

.group-member-summary-card strong {
    display: block;
    margin: 0.2rem 0 0.15rem;
    color: #fff;
    font-size: 1.5rem;
    letter-spacing: -0.04em;
}

.member-form-card {
    margin-top: 0.5rem;
    padding: 1.1rem 1.1rem 0.85rem;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(240, 245, 255, 0.9));
    border: 1px solid rgba(130, 141, 196, 0.14);
    border-radius: 1.15rem;
    box-shadow: 0 12px 26px rgba(44, 47, 94, 0.06);
}

.member-form-card .stButton > button {
    min-height: 2.8rem;
    padding: 0.65rem 1.2rem;
    color: #fff;
    background: linear-gradient(105deg, #6d49dd, #4e6ae2 55%, #13a797);
    border: 0;
    border-radius: 0.8rem;
    box-shadow: 0 8px 18px rgba(82, 86, 204, 0.2);
    font-weight: 700;
    transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
}

.member-form-card .stButton > button:hover {
    color: #fff;
    border: 0;
    box-shadow: 0 10px 22px rgba(82, 86, 204, 0.28);
    filter: brightness(1.06);
    transform: translateY(-1px);
}

.member-list-header {
    margin: 1.5rem 0 0.75rem;
    color: var(--ink);
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.member-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.9rem;
    padding: 0.8rem 0.95rem;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(128, 140, 180, 0.14);
    border-radius: 1rem;
    box-shadow: 0 8px 16px rgba(49, 60, 104, 0.05);
    transition: transform 140ms ease, box-shadow 140ms ease;
}

.member-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 22px rgba(49, 60, 104, 0.08);
}

.member-card-purple {
    background: linear-gradient(135deg, rgba(110, 78, 222, 0.06), rgba(255, 255, 255, 0.9));
}

.member-card-blue {
    background: linear-gradient(135deg, rgba(52, 120, 229, 0.06), rgba(255, 255, 255, 0.9));
}

.member-card-teal {
    background: linear-gradient(135deg, rgba(16, 169, 146, 0.06), rgba(255, 255, 255, 0.9));
}

.member-card-coral {
    background: linear-gradient(135deg, rgba(240, 121, 138, 0.08), rgba(255, 255, 255, 0.9));
}

.member-card-main {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    min-width: 0;
}

.member-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.8rem;
    height: 2.8rem;
    flex-shrink: 0;
    color: #fff;
    border-radius: 50%;
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.member-card-purple .member-avatar {
    background: linear-gradient(135deg, #6d49dd, #4a69d8);
}

.member-card-blue .member-avatar {
    background: linear-gradient(135deg, #2f8af4, #2d5ec8);
}

.member-card-teal .member-avatar {
    background: linear-gradient(135deg, #10a992, #0b8fa0);
}

.member-card-coral .member-avatar {
    background: linear-gradient(135deg, #f0808b, #c74b82);
}

.member-details {
    min-width: 0;
}

.member-name {
    color: #1f2a45;
    font-size: 1.02rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    overflow-wrap: anywhere;
}

.member-status {
    margin-top: 0.15rem;
    color: #5f6d8d;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.member-action {
    display: flex;
    justify-content: flex-end;
}

.member-action .stButton > button {
    min-height: 2.4rem;
    padding: 0.5rem 0.9rem;
    color: #fff;
    background: linear-gradient(105deg, #6d49dd, #4e6ae2);
    border: 0;
    border-radius: 0.75rem;
    box-shadow: 0 6px 14px rgba(82, 86, 204, 0.16);
    font-weight: 700;
}

.member-action .stButton > button:hover {
    color: #fff;
    border: 0;
    box-shadow: 0 10px 20px rgba(82, 86, 204, 0.22);
    filter: brightness(1.04);
}

.member-action .stButton > button:disabled {
    color: #5f6d8d;
    background: #e4e7f1;
    box-shadow: none;
}

.member-empty-state {
    padding: 1.5rem 1.2rem;
    background: linear-gradient(135deg, rgba(112, 72, 232, 0.04), rgba(16, 169, 146, 0.04));
    border: 1px solid rgba(112, 72, 232, 0.1);
    border-radius: 1rem;
    color: #445173;
    text-align: center;
    box-shadow: 0 8px 18px rgba(45, 50, 98, 0.04);
}

.member-empty-state strong {
    display: block;
    margin-bottom: 0.2rem;
    color: #1f2a45;
    font-size: 1.05rem;
}

.analytics-shell {
    margin-bottom: 1.1rem;
    padding: 1.2rem 1.35rem;
    background: linear-gradient(135deg, rgba(110, 73, 221, 0.08), rgba(52, 120, 229, 0.06), rgba(16, 169, 146, 0.05));
    border: 1px solid rgba(123, 101, 216, 0.12);
    border-radius: 1.3rem;
    box-shadow: 0 14px 32px rgba(55, 55, 110, 0.06);
}

.analytics-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.analytics-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.32rem 0.7rem;
    color: #4e39b1;
    background: rgba(110, 73, 221, 0.12);
    border: 1px solid rgba(110, 73, 221, 0.12);
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.analytics-header h2 {
    margin: 0.5rem 0 0.25rem;
    color: #1d2441;
    font-size: clamp(2rem, 3vw, 2.8rem);
    letter-spacing: -0.05em;
}

.analytics-header p {
    margin: 0;
    color: #5d6789;
    font-size: 0.98rem;
}

.analytics-summary-card {
    min-width: 13.5rem;
    padding: 0.9rem 1rem;
    color: #fff;
    background: linear-gradient(135deg, #6847df 0%, #335cc7 46%, #13a99b 100%);
    border-radius: 1.1rem;
    box-shadow: 0 16px 26px rgba(82, 86, 204, 0.2);
}

.analytics-summary-card span,
.analytics-summary-card small {
    display: block;
    color: rgba(255, 255, 255, 0.82);
}

.analytics-summary-card strong {
    display: block;
    margin: 0.2rem 0 0.15rem;
    color: #fff;
    font-size: 1.5rem;
    letter-spacing: -0.04em;
}

.analytics-metric-card {
    padding: 1.15rem 1.2rem;
    min-height: 8.4rem;
    border: 1px solid rgba(128, 138, 181, 0.14);
    border-radius: 1.1rem;
    box-shadow: 0 14px 28px rgba(40, 45, 84, 0.08);
}

.analytics-metric-card .metric-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.8rem;
    margin-bottom: 0.5rem;
}

.analytics-metric-card .metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.6rem;
    height: 2.6rem;
    color: #fff;
    background: rgba(255, 255, 255, 0.18);
    border-radius: 0.8rem;
    font-size: 1.2rem;
}

.analytics-metric-card .metric-label {
    color: rgba(255, 255, 255, 0.85);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.analytics-metric-card .metric-value {
    display: block;
    color: #fff;
    font-size: clamp(1.45rem, 2vw, 2rem);
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1.15;
}

.analytics-metric-purple {
    background: linear-gradient(135deg, #6d49dd 0%, #4f5fe1 100%);
}

.analytics-metric-blue {
    background: linear-gradient(135deg, #3f8ef5 0%, #2a5fcb 100%);
}

.analytics-metric-teal {
    background: linear-gradient(135deg, #17b69d 0%, #0d8b96 100%);
}

.analytics-panel {
    padding: 1rem 1.1rem 0.9rem;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(128, 138, 181, 0.12);
    border-radius: 1.1rem;
    box-shadow: 0 12px 24px rgba(41, 44, 86, 0.05);
}

.analytics-panel-title {
    margin: 0 0 0.8rem;
    color: var(--ink);
    font-size: 1.12rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.analytics-table-container {
    overflow: hidden;
    border-radius: 1rem;
    border: 1px solid rgba(128, 138, 181, 0.12);
    background: #fff;
}

.analytics-table-container [data-testid="stDataFrame"] {
    border: 0;
    border-radius: 0;
    box-shadow: none;
}

.analytics-table-container table {
    font-size: 0.92rem;
}

.analytics-table-container th {
    background: linear-gradient(135deg, rgba(110, 73, 221, 0.06), rgba(52, 120, 229, 0.04));
    color: #2a3454;
    font-weight: 800;
    letter-spacing: 0.01em;
}

.analytics-table-container td {
    color: #394764;
    font-weight: 600;
}

.analytics-table-container td:last-child,
.analytics-table-container td:nth-child(2) {
    color: #2b5ec7;
    font-weight: 800;
}

.chart-shell {
    padding: 0.8rem 0.6rem 0.2rem;
    border-radius: 1rem;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(245, 247, 255, 0.8));
    border: 1px solid rgba(128, 138, 181, 0.12);
}

.settlement-shell {
    margin-bottom: 1.2rem;
    padding: 1.2rem 1.35rem;
    background: linear-gradient(135deg, rgba(110, 73, 221, 0.08), rgba(52, 120, 229, 0.06), rgba(22, 184, 138, 0.05));
    border: 1px solid rgba(123, 101, 216, 0.12);
    border-radius: 1.3rem;
    box-shadow: 0 14px 32px rgba(55, 55, 110, 0.06);
}

.settlement-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.settlement-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.32rem 0.7rem;
    color: #4e39b1;
    background: rgba(110, 73, 221, 0.12);
    border: 1px solid rgba(110, 73, 221, 0.12);
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.settlement-header h2 {
    margin: 0.5rem 0 0.25rem;
    color: #1d2441;
    font-size: clamp(2rem, 3vw, 2.8rem);
    letter-spacing: -0.05em;
}

.settlement-header p {
    margin: 0;
    color: #5d6789;
    font-size: 0.98rem;
}

.settlement-summary-card {
    min-width: 13.5rem;
    padding: 0.9rem 1rem;
    color: #fff;
    background: linear-gradient(135deg, #5d4bcb 0%, #2e77d7 45%, #10a992 100%);
    border-radius: 1.1rem;
    box-shadow: 0 16px 26px rgba(82, 86, 204, 0.2);
}

.settlement-summary-card span,
.settlement-summary-card small {
    display: block;
    color: rgba(255, 255, 255, 0.82);
}

.settlement-summary-card strong {
    display: block;
    margin: 0.2rem 0 0.15rem;
    color: #fff;
    font-size: 1.5rem;
    letter-spacing: -0.04em;
}

.settlement-metric-card {
    padding: 1rem 1.1rem;
    min-height: 7.8rem;
    border: 1px solid rgba(128, 138, 181, 0.14);
    border-radius: 1.1rem;
    box-shadow: 0 14px 28px rgba(40, 45, 84, 0.08);
}

.settlement-metric-card .metric-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.8rem;
    margin-bottom: 0.7rem;
}

.settlement-metric-card .metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    color: #fff;
    background: rgba(255, 255, 255, 0.18);
    border-radius: 0.8rem;
    font-size: 1.15rem;
}

.settlement-metric-card .metric-label {
    color: rgba(255, 255, 255, 0.85);
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.settlement-metric-card .metric-value {
    display: block;
    color: #fff;
    font-size: clamp(1.52rem, 2vw, 1.9rem);
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1.15;
}

.settlement-metric-purple {
    background: linear-gradient(135deg, #6d49dd 0%, #4745c7 100%);
}

.settlement-metric-orange {
    background: linear-gradient(135deg, #f28a3f 0%, #df6d3d 100%);
}

.settlement-metric-blue {
    background: linear-gradient(135deg, #3aa8f1 0%, #2b63d6 100%);
}

.settlement-metric-green {
    background: linear-gradient(135deg, #11b995 0%, #0d8f88 100%);
}

.settlement-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.9rem 1rem;
    margin-bottom: 0.8rem;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(128, 138, 181, 0.14);
    border-left-width: 5px;
    border-radius: 1rem;
    box-shadow: 0 12px 24px rgba(41, 44, 86, 0.05);
}

.settlement-card.pending {
    border-left-color: #f39c42;
    background: linear-gradient(135deg, rgba(255, 173, 82, 0.08), rgba(255, 255, 255, 0.92));
}

.settlement-card.waiting {
    border-left-color: #4d6fe8;
    background: linear-gradient(135deg, rgba(77, 111, 232, 0.08), rgba(255, 255, 255, 0.92));
}

.settlement-card.completed {
    border-left-color: #10a992;
    background: linear-gradient(135deg, rgba(16, 169, 146, 0.08), rgba(255, 255, 255, 0.92));
}

.settlement-direction {
    color: #1f2a45;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.settlement-amount {
    color: #2b5ec7;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.settlement-meta {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.settlement-badge-pill {
    display: inline-flex;
    align-items: center;
    padding: 0.4rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.settlement-badge-pill.pending {
    color: #a75b00;
    background: rgba(243, 156, 66, 0.14);
}

.settlement-badge-pill.waiting {
    color: #2c58c8;
    background: rgba(77, 111, 232, 0.12);
}

.settlement-badge-pill.completed {
    color: #0a7f68;
    background: rgba(16, 169, 146, 0.12);
}

.settlement-card .stButton > button {
    min-height: 2.5rem;
    padding: 0.5rem 1rem;
    color: #fff;
    background: linear-gradient(105deg, #6d49dd, #3f8ef5);
    border: 0;
    border-radius: 0.75rem;
    box-shadow: 0 8px 18px rgba(82, 86, 204, 0.2);
    font-weight: 700;
}

.settlement-card .stButton > button:hover {
    color: #fff;
    border: 0;
    box-shadow: 0 10px 20px rgba(82, 86, 204, 0.24);
    filter: brightness(1.05);
}

.settlement-status-success {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 7rem;
    padding: 0.52rem 0.8rem;
    color: #0a7f68;
    background: rgba(16, 169, 146, 0.12);
    border: 1px solid rgba(16, 169, 146, 0.16);
    border-radius: 0.75rem;
    font-size: 0.85rem;
    font-weight: 800;
}

.settlement-empty-state {
    padding: 1.6rem 1.2rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(110, 73, 221, 0.04), rgba(16, 169, 146, 0.04));
    border: 1px solid rgba(110, 73, 221, 0.1);
    border-radius: 1rem;
    color: #45537c;
    box-shadow: 0 8px 18px rgba(45, 50, 98, 0.04);
}

.settlement-empty-state strong {
    display: block;
    margin-bottom: 0.25rem;
    color: #1f2a45;
    font-size: 1.05rem;
}

@media (max-width: 700px) {
    .dashboard-metric-card {
        min-height: 6rem;
        padding: 0.9rem 1rem;
    }

    .dashboard-payment-card {
        align-items: flex-start;
        flex-direction: column;
    }

    .group-member-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .group-member-summary-card {
        width: 100%;
        min-width: 0;
    }

    .member-card {
        align-items: flex-start;
        flex-direction: column;
    }

    .member-action {
        width: 100%;
        justify-content: flex-start;
    }
}

.stButton > button {
    min-height: 2.65rem;
    padding: 0.55rem 1.1rem;
    color: #fff;
    background: linear-gradient(105deg, #6b4fe0 0%, #4f73ea 54%, #17b29f 100%);
    border: 0;
    border-radius: 0.8rem;
    box-shadow: 0 8px 18px rgba(90, 90, 204, 0.19);
    font-weight: 700;
    transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
}

.stButton > button:hover {
    color: #fff;
    border: 0;
    box-shadow: 0 10px 22px rgba(90, 90, 204, 0.26);
    filter: brightness(1.04);
    transform: translateY(-1px);
}

.stButton > button:focus-visible {
    outline: 3px solid rgba(16, 169, 146, 0.55);
    outline-offset: 3px;
}

.stButton > button:disabled {
    color: #69708a;
    background: #e9eaf2;
    box-shadow: none;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    color: var(--ink);
    background: #fff;
    border: 1px solid #dfe5f1;
    border-radius: 0.8rem;
    box-shadow: 0 6px 18px rgba(30, 40, 70, 0.03);
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #6251d7;
    box-shadow: 0 0 0 3px rgba(98, 81, 215, 0.12);
}

[data-testid="stExpander"] {
    overflow: hidden;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--line);
    border-radius: 1rem;
    box-shadow: var(--shadow-soft);
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    overflow: hidden;
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 1rem;
    box-shadow: 0 8px 18px rgba(37, 39, 86, 0.06);
}

[data-testid="stAlert"] {
    border-radius: 0.9rem;
    box-shadow: 0 10px 20px rgba(39, 45, 85, 0.04);
}

[data-testid="stAlert"][kind="success"] {
    background: #ebfaf5;
    border: 1px solid #b5e9d7;
}

[data-testid="stAlert"][kind="warning"] {
    background: #fff8eb;
    border: 1px solid #f0dca3;
}

[data-testid="stAlert"][kind="info"] {
    background: #edf4ff;
    border: 1px solid #cfe0ff;
}

[data-testid="stAlert"] p {
    color: #29304d;
}

[data-testid="stNotificationContentSuccess"] {
    color: #087c6b;
}

hr {
    border-color: #e3e5f0;
    margin: 1.6rem 0;
}

@media (max-width: 900px) {
    .block-container {
        padding: 1.6rem 1.5rem 2.5rem;
    }

    [data-testid="stMetric"] {
        min-height: 6rem;
        padding: 0.95rem 1rem;
    }
}

@media (max-width: 600px) {
    .block-container {
        padding: 1.1rem 1rem 2rem;
    }

    h1 {
        font-size: 1.8rem;
    }

    h2 {
        font-size: 1.4rem;
    }

    .stButton > button {
        width: 100%;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)




if "members" not in st.session_state:
    cursor.execute("SELECT name FROM members")
    st.session_state.members = [
        row[0] for row in cursor.fetchall()
    ]

if "expenses" not in st.session_state:
    cursor.execute("""
        SELECT id, expense_name, amount, paid_by
        FROM expenses
        ORDER BY id
    """)

    saved_expenses = cursor.fetchall()
    st.session_state.expenses = []

    for expense_id, name, amount, paid_by in saved_expenses:
        cursor.execute("""
            SELECT member_name
            FROM expense_members
            WHERE expense_id = ?
        """, (expense_id,))

        split_members = [row[0] for row in cursor.fetchall()]

        st.session_state.expenses.append({
            "name": name,
            "amount": amount,
            "paid_by": paid_by,
            "members": split_members
        })




if "settlements" not in st.session_state:
    cursor.execute("""
        SELECT id, payer, receiver, amount, status
        FROM settlements
        ORDER BY id
    """)
    st.session_state.settlements = cursor.fetchall()
st.title("💰 SplitMate")
st.subheader("Smart Expense Sharing System")

st.write(
    "Manage group expenses, split bills fairly "
    "and track payments easily."
)




st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Choose a page",
    [
        "Dashboard",
        "Add Expense",
        "Group Members",
        "Analytics",
        "Settlement Payments"
    ]
)




if menu == "Dashboard":

    st.header("📊 Expense Dashboard")

    total_expenses = sum(
        expense["amount"]
        for expense in st.session_state.expenses
    )

    total_members = len(st.session_state.members)

    total_transactions = len(st.session_state.expenses)

    balances = {
        member: 0.0
        for member in st.session_state.members
    }

    for expense in st.session_state.expenses:

        split_members = expense["members"]

        if not split_members:
            continue

        share = expense["amount"] / len(split_members)

        payer = expense["paid_by"]

        

        if payer in balances:
            balances[payer] += expense["amount"]

        

        for member in split_members:

            if member in balances:
                balances[member] -= share

    new_settlements = []

    if st.session_state.expenses:
        creditors = []
        debtors = []

        for member, balance in balances.items():
            if balance > 0.005:
                creditors.append([member, balance])
            elif balance < -0.005:
                debtors.append([member, abs(balance)])

        i = 0
        j = 0

        while i < len(debtors) and j < len(creditors):
            amount = round(min(debtors[i][1], creditors[j][1]), 2)

            payer = debtors[i][0]
            receiver = creditors[j][0]

            new_settlements.append((payer, receiver, amount))

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] < 0.005:
                i += 1

            if creditors[j][1] < 0.005:
                j += 1

        for payer, receiver, amount in new_settlements:
            cursor.execute("""
                SELECT id, amount, status
                FROM settlements
                WHERE payer = ? AND receiver = ?
            """, (payer, receiver))

            existing = cursor.fetchone()

            if existing:
                settlement_id, old_amount, status = existing

                if round(old_amount, 2) != amount:
                    cursor.execute("""
                        UPDATE settlements
                        SET amount = ?, status = 'Pending'
                        WHERE id = ?
                    """, (amount, settlement_id))
            else:
                cursor.execute("""
                    INSERT INTO settlements
                    (payer, receiver, amount, status)
                    VALUES (?, ?, ?, 'Pending')
                """, (payer, receiver, amount))

        conn.commit()

    cursor.execute("""
        SELECT id, payer, receiver, amount, status
        FROM settlements
        ORDER BY id
    """)
    st.session_state.settlements = cursor.fetchall()

    current_settlement_amounts = {
        (payer, receiver): amount
        for payer, receiver, amount in new_settlements
    }
    outstanding_balances = balances.copy()
    completed_pairs = set()

    for _, payer, receiver, amount, status in st.session_state.settlements:
        pair = (payer, receiver)
        if (
            status == "Completed"
            and pair in current_settlement_amounts
            and round(amount, 2) == current_settlement_amounts[pair]
            and pair not in completed_pairs
        ):
            if payer in outstanding_balances:
                outstanding_balances[payer] += amount
            if receiver in outstanding_balances:
                outstanding_balances[receiver] -= amount
            completed_pairs.add(pair)

    pending_payments = sum(
        balance
        for balance in outstanding_balances.values()
        if balance > 0
    )

    metric_cards = [
        ("Total Expenses", f"₹{total_expenses:.2f}", "purple"),
        ("Total Members", f"{total_members}", "blue"),
        ("Pending Payments", f"₹{pending_payments:.2f}", "teal"),
        ("Total Transactions", f"{total_transactions}", "coral"),
    ]
    metric_columns = st.columns(4)

    for metric_column, (label, value, color) in zip(metric_columns, metric_cards):
        metric_column.markdown(
            f"""
            <div class="dashboard-metric-card dashboard-metric-{color}">
                <p>{label}</p>
                <strong>{value}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("Member Balance Summary")

    if st.session_state.expenses:

        member_balances = list(outstanding_balances.items())
        for start in range(0, len(member_balances), 3):
            balance_columns = st.columns(3)
            for balance_column, (member, balance) in zip(
                balance_columns,
                member_balances[start:start + 3]
            ):
                if balance > 0.005:
                    card_class = "dashboard-balance-receive"
                    message = "should receive"
                    value = f"₹{balance:.2f}"
                elif balance < -0.005:
                    card_class = "dashboard-balance-pay"
                    message = "should pay"
                    value = f"₹{abs(balance):.2f}"
                else:
                    card_class = "dashboard-balance-settled"
                    message = "settled"
                    value = ""

                amount_markup = f"<em>{value}</em>" if value else ""
                balance_column.markdown(
                    f"""
                    <div class="dashboard-balance-card {card_class}">
                        <strong>{html.escape(member)}</strong>
                        <span>{message}</span>
                        {amount_markup}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No expenses available. Start by adding an expense."
        )

    st.caption(
        f"Total transactions: {total_transactions}"
    )

    chart_column, payments_column = st.columns([1, 1.15])

    with chart_column:
        st.markdown(
            '<div class="dashboard-chart-title">Balance Overview</div>',
            unsafe_allow_html=True
        )

        if outstanding_balances:
            chart_members = list(outstanding_balances.items())
            chart_values = [balance for _, balance in chart_members]
            chart_colors = [
                "#10a992" if balance > 0.005
                else "#e26b82" if balance < -0.005
                else "#aab1c5"
                for balance in chart_values
            ]

            figure, axis = plt.subplots(
                figsize=(8, max(3.2, 0.48 * len(chart_members) + 0.8))
            )
            figure.patch.set_facecolor("#ffffff")
            axis.set_facecolor("#ffffff")
            bars = axis.barh(
                [member for member, _ in chart_members],
                chart_values,
                color=chart_colors,
                height=0.62,
                zorder=3
            )
            axis.axvline(0, color="#68708f", linewidth=1, zorder=2)
            axis.set_xlabel("Net balance (₹)", color="#68708f")
            axis.grid(axis="x", color="#e8e9f4", linewidth=0.8, zorder=0)
            axis.set_axisbelow(True)
            axis.tick_params(axis="both", colors="#38405f", labelsize=9)
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)
            axis.spines["left"].set_visible(False)
            axis.spines["bottom"].set_color("#e8e9f4")
            axis.bar_label(
                bars,
                labels=[f"₹{balance:,.2f}" for balance in chart_values],
                padding=4,
                fontsize=8,
                color="#38405f"
            )
            figure.tight_layout()
            st.pyplot(figure, use_container_width=True)
            plt.close(figure)
        else:
            st.info("No member balances available to chart.")

    with payments_column:
        st.subheader("💸 Who Pays Whom?")

        if st.session_state.expenses:
            creditors = []
            debtors = []

            for member, balance in outstanding_balances.items():
                if balance > 0.005:
                    creditors.append([member, balance])
                elif balance < -0.005:
                    debtors.append([member, abs(balance)])

            i = 0
            j = 0
            while i < len(debtors) and j < len(creditors):
                amount = round(min(debtors[i][1], creditors[j][1]), 2)
                payer = debtors[i][0]
                receiver = creditors[j][0]

                payments_column.markdown(
                    f"""
                    <div class="dashboard-payment-card">
                        <div>
                            <strong>{html.escape(payer)} → {html.escape(receiver)}</strong>
                            <p><span>Settlement payment</span></p>
                        </div>
                        <div class="dashboard-payment-amount">₹{amount:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                debtors[i][1] -= amount
                creditors[j][1] -= amount

                if debtors[i][1] < 0.005:
                    i += 1
                if creditors[j][1] < 0.005:
                    j += 1

        else:
            st.info("No expenses available to calculate settlements.")



elif menu == "Add Expense":

    total_logged = sum(
        expense["amount"]
        for expense in st.session_state.expenses
    )

    st.markdown(
        f"""
        <div class="add-expense-shell">
            <div class="add-expense-header">
                <div>
                    <span class="add-expense-badge">Fintech Dashboard</span>
                    <h2>Add New Expense</h2>
                    <p>Capture a new bill, assign the payer, and split it fairly with your group.</p>
                </div>
                <div class="add-expense-summary-card">
                    <span>Logged total</span>
                    <strong>₹{total_logged:.2f}</strong>
                    <small>{len(st.session_state.expenses)} expense(s)</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.members:

        st.warning(
            "Please add group members before creating an expense."
        )

    else:

        left_column, right_column = st.columns([1.6, 0.9])

        with left_column:
            expense_name = st.text_input(
                "Expense Name",
                placeholder="Example: Lunch, Movie, Travel"
            )

            amount = st.number_input(
                "Expense Amount (₹)",
                min_value=0.0,
                step=10.0,
                format="%.2f"
            )

        with right_column:
            st.markdown(
                f"""
                <div class="add-expense-summary-card" style="margin-top: 0.2rem; margin-bottom: 1rem;">
                    <span>Group snapshot</span>
                    <strong>{len(st.session_state.members)} members</strong>
                    <small>Ready to split across the group</small>
                </div>
                """,
                unsafe_allow_html=True
            )

            paid_by = st.selectbox(
                "Paid By",
                st.session_state.members
            )

            split_members = st.multiselect(
                "Split Between",
                st.session_state.members,
                default=st.session_state.members
            )

        if st.button("Add Expense", type="primary"):

            if not expense_name.strip():

                st.warning(
                    "Please enter an expense name."
                )

            elif amount <= 0:

                st.warning(
                    "Expense amount must be greater than zero."
                )

            elif not split_members:

                st.warning(
                    "Please select at least one member."
                )

            else:

                expense = {
                    "name": expense_name.strip(),
                    "amount": round(float(amount), 2),
                    "paid_by": paid_by,
                    "members": split_members.copy()
                }

                cursor.execute("""
                    INSERT INTO expenses (expense_name, amount, paid_by)
                    VALUES (?, ?, ?)
                """, (expense["name"], expense["amount"], expense["paid_by"]))

                expense_id = cursor.lastrowid

                share_amount = round(
                    expense["amount"] / len(expense["members"]), 2
                )

                for member_name in expense["members"]:
                    cursor.execute("""
                        INSERT INTO expense_members
                        (expense_id, member_name, share_amount)
                        VALUES (?, ?, ?)
                    """, (expense_id, member_name, share_amount))

                conn.commit()

                st.session_state.expenses.append(expense)

                st.success(
                    "Expense added successfully!"
                )



    st.divider()

    st.markdown(
        '<div class="expense-history-title">Expense History</div>',
        unsafe_allow_html=True
    )

    if st.session_state.expenses:

        for index, expense in enumerate(
            st.session_state.expenses,
            start=1
        ):

            number_of_members = len(expense["members"])
            share = expense["amount"] / number_of_members if number_of_members > 0 else 0

            with st.expander(
                f"🧾 {index}. {expense['name']} • ₹{expense['amount']:.2f}"
            ):

                st.markdown(
                    f"""
                    <div class="expense-history-card">
                        <div class="expense-history-head">
                            <div class="expense-history-name">{html.escape(expense['name'])}</div>
                            <div class="expense-history-amount">₹{expense['amount']:.2f}</div>
                        </div>
                        <div class="expense-history-meta">
                            <span class="expense-history-pill">💳 Paid by {html.escape(expense['paid_by'])}</span>
                            <span class="expense-history-pill">👥 {number_of_members} split</span>
                        </div>
                        <div class="expense-share-list">
                            {''.join(f'<div class="expense-share-item"><span>{html.escape(name)}</span><strong>₹{share:.2f}</strong></div>' for name in expense['members'])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No expenses added yet."
        )



elif menu == "Group Members":

    st.markdown(
        f"""
        <div class="group-member-shell">
            <div class="group-member-header">
                <div>
                    <span class="group-member-badge">Member hub</span>
                    <h2>Group Members</h2>
                    <p>Manage your split group, keep everyone in sync, and keep your shared bills organised.</p>
                </div>
                <div class="group-member-summary-card">
                    <span>Total members</span>
                    <strong>{len(st.session_state.members)}</strong>
                    <small>{'Ready to split bills' if st.session_state.members else 'Add your first member'}</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="member-form-card">',
        unsafe_allow_html=True
    )

    member = st.text_input(
        "Enter Member Name",
        key="member_input",
        placeholder="e.g. Alex, Priya, Jordan"
    )

    if st.button("Add Member"):

        clean_name = member.strip()

        if not clean_name:

            st.warning(
                "Please enter a member name."
            )

        elif clean_name.lower() in [
            name.lower()
            for name in st.session_state.members
        ]:

            st.warning(
                "Member already exists!"
            )
        else:

            try:
                cursor.execute(
                    "INSERT INTO members (name) VALUES (?)",
                    (clean_name,)
                )

                conn.commit()

                st.session_state.members.append(clean_name)

                st.success(
                    f"{clean_name} added successfully!"
                )

                st.rerun()

            except sqlite3.IntegrityError:
                st.warning("Member already exists!")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="member-list-header">All Group Members</div>',
        unsafe_allow_html=True
    )

    if st.session_state.members:

        for index, name in enumerate(st.session_state.members):

            color_classes = [
                "purple",
                "blue",
                "teal",
                "coral"
            ]
            color_class = color_classes[index % len(color_classes)]
            initials = "".join(part[0].upper() for part in name.split()[:2]) if name.strip() else "?"

            col1, col2 = st.columns([4.5, 1.3])

            has_expenses = any(
                name in expense["members"]
                or name == expense["paid_by"]
                for expense in st.session_state.expenses
            )

            with col1:
                st.markdown(
                    f"""
                    <div class="member-card member-card-{color_class}">
                        <div class="member-card-main">
                            <div class="member-avatar">{html.escape(initials)}</div>
                            <div class="member-details">
                                <div class="member-name">{html.escape(name)}</div>
                                <div class="member-status">{'In use' if has_expenses else 'Available'}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown('<div class="member-action">', unsafe_allow_html=True)
                if has_expenses:

                    col2.button(
                        "In Use",
                        key=f"in_use_{index}",
                        disabled=True
                    )

                else:

                    if col2.button(
                        "Remove",
                        key=f"remove_{index}"
                    ):

                        cursor.execute(
                            "DELETE FROM members WHERE name = ?",
                            (name,)
                        )
                        conn.commit()

                        st.session_state.members.pop(index)

                        st.success(f"{name} removed successfully!")

                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown(
            """
            <div class="member-empty-state">
                <strong>No group members yet</strong>
                Add your first member to start sharing expenses with confidence.
            </div>
            """,
            unsafe_allow_html=True
        )


elif menu == "Analytics":

    st.markdown(
        f"""
        <div class="analytics-shell">
            <div class="analytics-header">
                <div>
                    <span class="analytics-badge">Finance overview</span>
                    <h2>Expense Analytics</h2>
                    <p>Track spending trends, compare categories, and understand who is funding the group expenses.</p>
                </div>
                <div class="analytics-summary-card">
                    <span>Recorded spend</span>
                    <strong>₹{sum(expense['amount'] for expense in st.session_state.expenses):.2f}</strong>
                    <small>{len(st.session_state.expenses)} total expense(s)</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.expenses:

        df = pd.DataFrame(
            st.session_state.expenses
        )

        total_spending = df["amount"].sum()

        average_expense = df["amount"].mean()

        highest_expense = df["amount"].max()

        metric_cards = [
            ("Total Spending", f"₹{total_spending:.2f}", "purple", "💸"),
            ("Average Expense", f"₹{average_expense:.2f}", "blue", "📊"),
            ("Highest Expense", f"₹{highest_expense:.2f}", "teal", "🏆")
        ]

        metric_columns = st.columns(3)

        for metric_column, (label, value, color, icon) in zip(metric_columns, metric_cards):
            metric_column.markdown(
                f"""
                <div class="analytics-metric-card analytics-metric-{color}">
                    <div class="metric-header">
                        <span class="metric-label">{label}</span>
                        <span class="metric-icon">{icon}</span>
                    </div>
                    <span class="metric-value">{value}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.markdown(
            '<div class="analytics-panel-title">Expense Records</div>',
            unsafe_allow_html=True
        )

        display_df = df[
            ["name", "amount", "paid_by"]
        ].copy()

        display_df.columns = [
            "Expense Name",
            "Amount (₹)",
            "Paid By"
        ]

        st.markdown(
            '<div class="analytics-table-container">',
            unsafe_allow_html=True
        )
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            '<div class="analytics-panel-title">Spending Analysis</div>',
            unsafe_allow_html=True
        )

        chart_data = (
            df.groupby("name")["amount"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(9, 4.6))
        fig.patch.set_facecolor("#f6f7fc")
        ax.set_facecolor("#f9fafc")

        chart_data.plot(
            kind="bar",
            ax=ax,
            color=["#6d49dd", "#3f8ef5", "#17b69d", "#f29a57", "#e76f9a", "#8a6ef7", "#46a9d4", "#3db39e"][:len(chart_data)]
        )

        ax.set_xlabel("Expense Name", color="#38405f", fontsize=10, fontweight="bold")
        ax.set_ylabel("Amount (₹)", color="#38405f", fontsize=10, fontweight="bold")
        ax.set_title("Expense-wise Spending", color="#202344", fontsize=14, fontweight="800", pad=12)
        ax.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.3)
        ax.tick_params(axis="x", labelrotation=30, colors="#495a7b")
        ax.tick_params(axis="y", colors="#495a7b")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#dfe3f2")
        ax.spines["bottom"].set_color("#dfe3f2")

        for bars in ax.containers:
            ax.bar_label(
                bars,
                labels=[f"₹{value:,.2f}" for value in bars.datavalues] if hasattr(bars, "datavalues") else [],
                padding=4,
                fontsize=8,
                color="#2a3454",
                rotation=0
            )

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.divider()

        st.markdown(
            '<div class="analytics-panel-title">Member-wise Payments</div>',
            unsafe_allow_html=True
        )

        payer_data = (
            df.groupby("paid_by")["amount"]
            .sum()
        )

        chart_colors = [
            "#6d49dd",
            "#3f8ef5",
            "#17b69d",
            "#f29a57",
            "#e76f9a",
            "#5fc0d7",
            "#7b6df1",
            "#3bb4a2"
        ]

        fig2, ax2 = plt.subplots(figsize=(9, 4.3))
        fig2.patch.set_facecolor("#f6f7fc")
        ax2.set_facecolor("#f9fafc")
        ax2.bar(payer_data.index, payer_data.values, color=chart_colors[:len(payer_data)])
        ax2.set_xlabel("Member", color="#38405f", fontsize=10, fontweight="bold")
        ax2.set_ylabel("Amount (₹)", color="#38405f", fontsize=10, fontweight="bold")
        ax2.set_title("Member-wise Payments", color="#202344", fontsize=14, fontweight="800", pad=12)
        ax2.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.3)
        ax2.tick_params(axis="x", colors="#495a7b")
        ax2.tick_params(axis="y", colors="#495a7b")
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_color("#dfe3f2")
        ax2.spines["bottom"].set_color("#dfe3f2")

        for p, value in zip(ax2.patches, payer_data.values):
            ax2.text(
                p.get_x() + p.get_width() / 2,
                p.get_height() + 0.5,
                f"₹{value:,.2f}",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#2a3454"
            )

        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    else:

        st.info(
            "Please add expenses to view analytics."
        )





elif menu == "Settlement Payments":

    total_settlements = len(st.session_state.settlements)
    pending_count = sum(1 for _, _, _, _, status in st.session_state.settlements if status == "Pending")
    waiting_count = sum(1 for _, _, _, _, status in st.session_state.settlements if status == "Waiting for Confirmation")
    completed_count = sum(1 for _, _, _, _, status in st.session_state.settlements if status == "Completed")

    st.markdown(
        f"""
        <div class="settlement-shell">
            <div class="settlement-header">
                <div>
                    <span class="settlement-badge">Payment tracker</span>
                    <h2>Settlement Payments</h2>
                    <p>Track, manage and confirm group payments with a clear payment workflow.</p>
                </div>
                <div class="settlement-summary-card">
                    <span>All settlements</span>
                    <strong>{total_settlements}</strong>
                    <small>{pending_count} pending • {completed_count} complete</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_cards = [
        ("Total Settlements", total_settlements, "purple", "💳"),
        ("Pending Payments", pending_count, "orange", "⏳"),
        ("Waiting for Confirmation", waiting_count, "blue", "🔔"),
        ("Completed Payments", completed_count, "green", "✅")
    ]

    metric_columns = st.columns(4)

    for metric_column, (label, value, color, icon) in zip(metric_columns, metric_cards):
        metric_column.markdown(
            f"""
            <div class="settlement-metric-card settlement-metric-{color}">
                <div class="metric-header">
                    <span class="metric-label">{label}</span>
                    <span class="metric-icon">{icon}</span>
                </div>
                <span class="metric-value">{value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    if st.session_state.settlements:

        for settlement in st.session_state.settlements:

            settlement_id, payer, receiver, amount, status = settlement
            status_key = "pending" if status == "Pending" else "waiting" if status == "Waiting for Confirmation" else "completed"
            status_label = status

            st.markdown(
                f"""
                <div class="settlement-card {status_key}">
                    <div>
                        <div class="settlement-direction">{payer} → {receiver}</div>
                        <div class="settlement-meta">
                            <span class="settlement-badge-pill {status_key}">{status_label}</span>
                        </div>
                    </div>
                    <div class="settlement-amount">₹{amount:.2f}</div>
                    <div>
                """,
                unsafe_allow_html=True
            )

            if status == "Pending":

                if st.button(
                    "I Paid",
                    key=f"paid_{settlement_id}"
                ):

                    cursor.execute(
                        "UPDATE settlements SET status = ? WHERE id = ?",
                        ("Waiting for Confirmation", settlement_id)
                    )

                    conn.commit()

                    st.session_state.settlements = [
                        (
                            sid, p, r, a,
                            "Waiting for Confirmation" if sid == settlement_id else s
                        )
                        for sid, p, r, a, s in st.session_state.settlements
                    ]

                    st.rerun()

            elif status == "Waiting for Confirmation":

                if st.button(
                    "Confirm Received",
                    key=f"confirm_{settlement_id}"
                ):

                    cursor.execute(
                        "UPDATE settlements SET status = ? WHERE id = ?",
                        ("Completed", settlement_id)
                    )

                    conn.commit()

                    st.session_state.settlements = [
                        (
                            sid, p, r, a,
                            "Completed" if sid == settlement_id else s
                        )
                        for sid, p, r, a, s in st.session_state.settlements
                    ]

                    st.rerun()

            else:

                st.markdown(
                    '<div class="settlement-status-success">Paid ✓</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="settlement-empty-state">
                <strong>No settlement payments yet</strong>
                Once members settle balances, payment tracking will appear here.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()

st.caption(
    "SplitMate | Smart and Fair Expense Sharing System"
)
