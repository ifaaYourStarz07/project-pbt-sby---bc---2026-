"""
admin/konfirmasi.py - Panel Konfirmasi Pesanan (Redesign Premium)
Aplikasi Business Center SMKN 13 Bandung
Palet: Dark Green #051F20 → Pale Mint #DAF1DE
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db

# ─── Palet Warna (seragam seluruh aplikasi) ───────────────────────────────────
C_DARKEST   = "#051F20"
C_DARK      = "#0B2B26"
C_MID       = "#163832"
C_MUTED     = "#235347"
C_MINT      = "#8EB69B"
C_PALE      = "#DAF1DE"
WHITE       = "#FFFFFF"
BG_MAIN     = "#F4FAF6"
BORDER_CLR  = "#D1E8D8"
DARK_TEXT   = "#1A2E22"
GRAY_TEXT   = "#5C7A68"
LIGHT_TEXT  = "#9DB8A8"

# Status colors
S_PENDING   = "#C07A00"   # amber
S_DITERIMA  = "#163832"   # hijau gelap
S_DITOLAK   = "#8B1A1A"   # merah gelap

S_BG_PENDING  = "#FFF8E1"
S_BG_DITERIMA = "#F0FAF4"
S_BG_DITOLAK  = "#FFF0F0"

BTN_ACCEPT  = "#163832"
BTN_ACCEPT_H= "#0B2B26"
BTN_REJECT  = "#7A2020"
BTN_REJECT_H= "#5C1515"


# ─── Helper: pill button ──────────────────────────────────────────────────────
def _pill(parent, text, command, w=150, h=38, r=19,
          color=C_MID, hover=C_DARK, fg=WHITE,
          font=("Segoe UI", 9, "bold")):
    cv = tk.Canvas(parent, width=w, height=h,
                   bg=parent["bg"], highlightthickness=0, cursor="hand2")
    def _draw(fill):
        cv.delete("all")
        cv.create_arc(0,0,r*2,h,start=90,extent=180,fill=fill,outline=fill)
        cv.create_arc(w-r*2,0,w,h,start=270,extent=180,fill=fill,outline=fill)
        cv.create_rectangle(r,0,w-r,h,fill=fill,outline=fill)
        cv.create_text(w//2,h//2,text=text,fill=fg,font=font,anchor="center")
    _draw(color)
    cv.bind("<Enter>",    lambda e: _draw(hover))
    cv.bind("<Leave>",    lambda e: _draw(color))
    cv.bind("<Button-1>", lambda e: command())
    return cv


def _pill_disabled(parent, text, w=150, h=38, r=19,
                   font=("Segoe UI", 9, "bold")):
    """Pill non-interaktif untuk state disabled."""
    cv = tk.Canvas(parent, width=w, height=h,
                   bg=parent["bg"], highlightthickness=0)
    cv.create_arc(0,0,r*2,h,start=90,extent=180,fill=BORDER_CLR,outline=BORDER_CLR)
    cv.create_arc(w-r*2,0,w,h,start=270,extent=180,fill=BORDER_CLR,outline=BORDER_CLR)
    cv.create_rectangle(r,0,w-r,h,fill=BORDER_CLR,outline=BORDER_CLR)
    cv.create_text(w//2,h//2,text=text,fill=LIGHT_TEXT,font=font,anchor="center")
    return cv


# ═══════════════════════════════════════════════════════════════════════════════
class KonfirmasiPanel(tk.Frame):

    def __init__(self, parent, dashboard):
        super().__init__(parent, bg=BG_MAIN)
        self.dashboard   = dashboard
        self.selected_id = None
        self._filter_val = "semua"
        self._btn_terima_cv  = None
        self._btn_tolak_cv   = None
        self._btn_terima_dis = None
        self._btn_tolak_dis  = None
        self._build_styles()
        self._build()
        self._load_pesanan()

<<<<<<< HEAD
    # ── Layout ────────────────────────────────────────────────────────────────
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=WHITE, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📋  Konfirmasi Pesanan", font=("Segoe UI", 15, "bold"),
                 bg=WHITE, fg=DARK_TEXT).pack(side="left", padx=24, pady=14)
        tk.Button(hdr, text="🔄 Refresh", font=("Segoe UI", 9),
                  bg=LIGHT_GRAY, fg=DARK_TEXT, relief="flat", padx=10, pady=5,
                  cursor="hand2", command=self._refresh).pack(side="right", padx=4)
        tk.Button(hdr, text="🗑  Hapus Semua Histori", font=("Segoe UI", 9, "bold"),
                  bg="#B71C1C", fg=WHITE, relief="flat", padx=10, pady=5,
                  cursor="hand2", command=self._hapus_semua_histori).pack(side="right", padx=(16, 4))
=======
    def _build_styles(self):
        s = ttk.Style()
        s.theme_use("default")
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

        # Treeview pesanan
        s.configure("Pesanan.Treeview",
                    font=("Segoe UI", 9), rowheight=32,
                    background=WHITE, fieldbackground=WHITE,
                    foreground=DARK_TEXT, borderwidth=0)
        s.configure("Pesanan.Treeview.Heading",
                    font=("Segoe UI", 9, "bold"),
                    background=BG_MAIN, foreground=GRAY_TEXT,
                    relief="flat", borderwidth=0)
        s.map("Pesanan.Treeview",
              background=[("selected", C_PALE)],
              foreground=[("selected", C_DARKEST)])

        # Treeview detail
        s.configure("Detail.Treeview",
                    font=("Segoe UI", 9), rowheight=30,
                    background=WHITE, fieldbackground=WHITE,
                    foreground=DARK_TEXT, borderwidth=0)
        s.configure("Detail.Treeview.Heading",
                    font=("Segoe UI", 8, "bold"),
                    background=BG_MAIN, foreground=GRAY_TEXT,
                    relief="flat", borderwidth=0)
        s.map("Detail.Treeview",
              background=[("selected", C_PALE)])

        # Scrollbar tipis
        s.configure("Thin.Vertical.TScrollbar",
                    gripcount=0, background=C_MINT,
                    troughcolor=BG_MAIN, borderwidth=0,
                    arrowsize=0, width=5)
        s.map("Thin.Vertical.TScrollbar",
              background=[("active", C_MUTED)])

    # ── Build UI ──────────────────────────────────────────────────────────────
    def _build(self):
        self._build_topbar()
        self._build_filter_tabs()
        tk.Frame(self, bg=BORDER_CLR, height=1).pack(fill="x")
        self._build_body()

    def _build_topbar(self):
        topbar = tk.Frame(self, bg=WHITE, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # Aksen kiri
        tk.Frame(topbar, bg=C_MID, width=4).pack(side="left", fill="y")

        title_col = tk.Frame(topbar, bg=WHITE)
        title_col.pack(side="left", padx=20, fill="y", pady=12)
        tk.Label(title_col, text="Konfirmasi Pesanan",
                 font=("Segoe UI", 14, "bold"),
                 bg=WHITE, fg=DARK_TEXT, anchor="w").pack(anchor="w")
        tk.Label(title_col, text="Terima atau tolak pesanan dari pelanggan",
                 font=("Segoe UI", 8),
                 bg=WHITE, fg=GRAY_TEXT, anchor="w").pack(anchor="w")

        btn_ref = _pill(topbar, text="↻  Refresh", command=self._refresh,
                        w=100, h=32, r=16,
                        color=C_PALE, hover=C_MINT, fg=C_MID,
                        font=("Segoe UI", 8, "bold"))
        btn_ref.config(bg=WHITE)
        btn_ref.pack(side="right", padx=20, pady=16)

    def _build_filter_tabs(self):
        tab_wrap = tk.Frame(self, bg=WHITE)
        tab_wrap.pack(fill="x", padx=20, pady=(10,0))

        self.filter_btns = {}
        filters = [
            ("Semua",        "semua"),
            ("⏳  Pending",  "pending"),
            ("✅  Diterima", "diterima"),
            ("❌  Ditolak",  "ditolak"),
        ]
        for label, key in filters:
            btn = tk.Label(tab_wrap, text=label,
                           font=("Segoe UI", 9, "bold"),
                           bg=WHITE, fg=LIGHT_TEXT,
                           padx=14, pady=8, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, k=key: self._set_filter(k))
            self.filter_btns[key] = btn

        self._set_filter("semua", init=True)

    def _build_body(self):
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # ── Panel kiri: daftar pesanan ────────────────────────────────────────
        left = tk.Frame(body, bg=WHITE,
                        highlightbackground=BORDER_CLR,
                        highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0,8))

        # Sub-header kiri
        l_hdr = tk.Frame(left, bg=WHITE)
        l_hdr.pack(fill="x", padx=14, pady=(12,8))
        tk.Frame(l_hdr, bg=C_MID, width=4, height=16).pack(side="left")
        tk.Label(l_hdr, text="  Daftar Pesanan",
                 font=("Segoe UI", 10, "bold"),
                 bg=WHITE, fg=DARK_TEXT).pack(side="left")
        self.lbl_count = tk.Label(l_hdr, text="",
                                   font=("Segoe UI", 8),
                                   bg=WHITE, fg=GRAY_TEXT)
        self.lbl_count.pack(side="left", padx=6)

        tk.Frame(left, bg=BORDER_CLR, height=1).pack(fill="x")

        # Treeview
        tree_wrap = tk.Frame(left, bg=WHITE)
        tree_wrap.pack(fill="both", expand=True)

        cols = ("ID", "Tanggal", "Total", "Status")
        self.tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", style="Pesanan.Treeview",
                                  selectmode="browse")
        self.tree.heading("ID",      text="ID")
        self.tree.heading("Tanggal", text="Tanggal & Jam")
        self.tree.heading("Total",   text="Total Harga")
        self.tree.heading("Status",  text="Status")
        self.tree.column("ID",      width=52,  anchor="center", stretch=False)
        self.tree.column("Tanggal", width=165, anchor="center")
        self.tree.column("Total",   width=120, anchor="e",  stretch=False)
        self.tree.column("Status",  width=95,  anchor="center", stretch=False)

        tsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                            command=self.tree.yview,
                            style="Thin.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=tsb.set)
        tsb.pack(side="right", fill="y", pady=4)
        self.tree.pack(fill="both", expand=True, padx=(8,0), pady=4)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # ── Panel kanan: detail + aksi ────────────────────────────────────────
        right = tk.Frame(body, bg=WHITE, width=300,
                         highlightbackground=BORDER_CLR,
                         highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_detail_panel(right)

    def _build_detail_panel(self, parent):
        # Header detail
        d_hdr = tk.Frame(parent, bg=C_DARKEST, height=52)
        d_hdr.pack(fill="x")
        d_hdr.pack_propagate(False)
        tk.Label(d_hdr, text="Detail Pesanan",
                 font=("Segoe UI", 10, "bold"),
                 bg=C_DARKEST, fg=WHITE).pack(
                     side="left", padx=16, pady=15)

        # Info pesanan
        info = tk.Frame(parent, bg=WHITE)
        info.pack(fill="x", padx=14, pady=(14,8))

        self.lbl_id = tk.Label(info, text="Pilih pesanan dari daftar",
                                font=("Segoe UI", 11, "bold"),
                                bg=WHITE, fg=DARK_TEXT, anchor="w",
                                wraplength=260, justify="left")
        self.lbl_id.pack(anchor="w")

        self.lbl_tgl = tk.Label(info, text="",
                                 font=("Segoe UI", 8),
                                 bg=WHITE, fg=GRAY_TEXT, anchor="w")
        self.lbl_tgl.pack(anchor="w", pady=(2,0))

        # Badge status
        self.badge_frame = tk.Frame(parent, bg=WHITE)
        self.badge_frame.pack(fill="x", padx=14, pady=(0,10))
        self.lbl_badge = tk.Label(self.badge_frame, text="",
                                   font=("Segoe UI", 8, "bold"),
                                   bg=WHITE, fg=WHITE,
                                   padx=10, pady=4)
        self.lbl_badge.pack(side="left")

        tk.Frame(parent, bg=BORDER_CLR, height=1).pack(fill="x", padx=14)

        # Label detail items
        di_hdr = tk.Frame(parent, bg=WHITE)
        di_hdr.pack(fill="x", padx=14, pady=(10,6))
        tk.Frame(di_hdr, bg=C_MINT, width=3, height=14).pack(side="left")
        tk.Label(di_hdr, text="  Item Dipesan",
                 font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=DARK_TEXT).pack(side="left")

        # Treeview detail items
        det_wrap = tk.Frame(parent, bg=WHITE)
        det_wrap.pack(fill="both", expand=True, padx=8, pady=(0,4))

        det_cols = ("Barang", "Jml", "Subtotal")
        self.tree_detail = ttk.Treeview(det_wrap, columns=det_cols,
                                         show="headings", style="Detail.Treeview",
                                         height=6)
        self.tree_detail.heading("Barang",   text="Nama Barang")
        self.tree_detail.heading("Jml",      text="Qty")
        self.tree_detail.heading("Subtotal", text="Subtotal")
        self.tree_detail.column("Barang",   width=130, anchor="w")
        self.tree_detail.column("Jml",      width=36,  anchor="center", stretch=False)
        self.tree_detail.column("Subtotal", width=90,  anchor="e",  stretch=False)

        dsb = ttk.Scrollbar(det_wrap, orient="vertical",
                            command=self.tree_detail.yview,
                            style="Thin.Vertical.TScrollbar")
        self.tree_detail.configure(yscrollcommand=dsb.set)
        dsb.pack(side="right", fill="y")
        self.tree_detail.pack(fill="both", expand=True)

        tk.Frame(parent, bg=BORDER_CLR, height=1).pack(fill="x", padx=14, pady=(4,0))

        # Total
        tot_f = tk.Frame(parent, bg=WHITE)
        tot_f.pack(fill="x", padx=14, pady=10)
        tk.Label(tot_f, text="Total:",
                 font=("Segoe UI", 9),
                 bg=WHITE, fg=GRAY_TEXT).pack(side="left")
        self.lbl_total = tk.Label(tot_f, text="—",
                                   font=("Segoe UI", 16, "bold"),
                                   bg=WHITE, fg=C_MID)
        self.lbl_total.pack(side="right")

        tk.Frame(parent, bg=BORDER_CLR, height=1).pack(fill="x")

        # Notif aksi
        self.lbl_aksi_notif = tk.Label(parent, text="",
                                        font=("Segoe UI", 8),
                                        bg=WHITE, fg=GRAY_TEXT,
                                        wraplength=260, justify="center")
        self.lbl_aksi_notif.pack(fill="x", padx=10, pady=(6,0))

        # Tombol aksi
        self.aksi_frame = tk.Frame(parent, bg=WHITE)
        self.aksi_frame.pack(fill="x", padx=14, pady=(6,14))
        self._render_aksi_buttons(enabled=False, status=None)

    def _render_aksi_buttons(self, enabled: bool, status: str):
        for w in self.aksi_frame.winfo_children():
            w.destroy()

<<<<<<< HEAD
        self.btn_tolak = tk.Button(
            aksi_frame, text="❌  TOLAK", font=("Segoe UI", 11, "bold"),
            bg=PRIMARY, fg=WHITE, relief="flat", pady=10, cursor="hand2",
            state="disabled", activebackground=PRIMARY_DK, activeforeground=WHITE,
            command=self._tolak_pesanan
        )
        self.btn_tolak.pack(fill="x", pady=(0, 6))

        tk.Frame(aksi_frame, bg="#DDDDDD", height=1).pack(fill="x", pady=(4, 6))

        self.btn_hapus = tk.Button(
            aksi_frame, text="🗑  Hapus Pesanan Ini", font=("Segoe UI", 9, "bold"),
            bg="#37474F", fg=WHITE, relief="flat", pady=7, cursor="hand2",
            state="disabled", activebackground="#263238", activeforeground=WHITE,
            command=self._hapus_pesanan
        )
        self.btn_hapus.pack(fill="x")
=======
        if not enabled or status != "pending":
            # Disabled state
            d1 = _pill_disabled(self.aksi_frame, text="✅  Terima",
                                 w=260, h=40, r=20)
            d1.pack(pady=(0,8))
            d2 = _pill_disabled(self.aksi_frame, text="❌  Tolak",
                                 w=260, h=40, r=20)
            d2.pack()
            if status and status != "pending":
                self.lbl_aksi_notif.config(
                    text=f"Pesanan ini sudah {status.upper()}.",
                    fg=GRAY_TEXT)
            else:
                self.lbl_aksi_notif.config(text="")
        else:
            self.lbl_aksi_notif.config(text="")
            b1 = _pill(self.aksi_frame, text="✅  Terima Pesanan",
                       command=self._terima_pesanan,
                       w=260, h=42, r=21,
                       color=BTN_ACCEPT, hover=BTN_ACCEPT_H,
                       font=("Segoe UI", 10, "bold"))
            b1.config(bg=WHITE)
            b1.pack(pady=(0,8))

            b2 = _pill(self.aksi_frame, text="❌  Tolak Pesanan",
                       command=self._tolak_pesanan,
                       w=260, h=42, r=21,
                       color=BTN_REJECT, hover=BTN_REJECT_H,
                       font=("Segoe UI", 10, "bold"))
            b2.config(bg=WHITE)
            b2.pack()
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

    # ── Filter ────────────────────────────────────────────────────────────────
    def _set_filter(self, key: str, init: bool = False):
        self._filter_val = key
        for k, btn in self.filter_btns.items():
            if k == key:
                btn.config(fg=C_MID,
                           font=("Segoe UI", 9, "bold"))
                # Garis bawah aktif — pakai relief sunken tipis
                btn.config(relief="groove", bd=0,
                           highlightbackground=C_MID,
                           highlightthickness=2)
            else:
                btn.config(fg=LIGHT_TEXT,
                           font=("Segoe UI", 9),
                           relief="flat", bd=0)
        if not init:
            self._load_pesanan()

    # ── Data ──────────────────────────────────────────────────────────────────
    def _load_pesanan(self):
        self.selected_id = None
        self._clear_detail()
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            from firebase_admin import firestore
            db = get_db()
            if self._filter_val == "semua":
<<<<<<< HEAD
                docs = db.collection('pesanan').order_by('tanggal', direction=firestore.Query.DESCENDING).stream()
            else:
                docs = db.collection('pesanan').where('status', '==', self._filter_val).order_by('tanggal', direction=firestore.Query.DESCENDING).stream()
                
            for i, doc in enumerate(docs):
                r = doc.to_dict()
                total = f"Rp {r.get('total_harga', 0):,.0f}"
                tag   = r.get("status", "")
                self.tree.insert("", "end", iid=doc.id,
                                 values=(doc.id[:8], str(r.get("tanggal", ""))[:19],
                                         total, tag.upper()),
                                 tags=(tag, "alt" if i % 2 == 0 else ""))

            self.tree.tag_configure("pending",  foreground="#E65100")
            self.tree.tag_configure("diterima", foreground=ACCENT_G)
            self.tree.tag_configure("ditolak",  foreground=PRIMARY_DK)
            self.tree.tag_configure("alt",      background=ROW_ALT)
=======
                rows = execute_query(
                    "SELECT id_pesanan, tanggal, total_harga, status "
                    "FROM pesanan ORDER BY tanggal DESC",
                    fetch=True)
            else:
                rows = execute_query(
                    "SELECT id_pesanan, tanggal, total_harga, status "
                    "FROM pesanan WHERE status=%s ORDER BY tanggal DESC",
                    (self._filter_val,), fetch=True)

            self.lbl_count.config(text=f"({len(rows)} pesanan)")

            # Tag warna per status
            self.tree.tag_configure("pending",
                background=S_BG_PENDING,  foreground=S_PENDING)
            self.tree.tag_configure("diterima",
                background=S_BG_DITERIMA, foreground=S_DITERIMA)
            self.tree.tag_configure("ditolak",
                background=S_BG_DITOLAK,  foreground=S_DITOLAK)

            STATUS_LABEL = {
                "pending":  "⏳ Pending",
                "diterima": "✅ Diterima",
                "ditolak":  "❌ Ditolak",
            }
            for r in rows:
                total  = f"Rp {r['total_harga']:,.0f}"
                status = r["status"]
                label  = STATUS_LABEL.get(status, status.upper())
                self.tree.insert("", "end", iid=str(r["id_pesanan"]),
                                 values=(f"#{r['id_pesanan']}",
                                         str(r["tanggal"])[:19],
                                         total, label),
                                 tags=(status,))
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        except Exception as e:
            messagebox.showerror("Error DB", str(e), parent=self)

    def _on_select(self, _):
        sel = self.tree.selection()
        if not sel:
            return
<<<<<<< HEAD
        self.selected_id = str(sel[0])
=======
        self.selected_id = int(sel[0].replace("#", "").strip())
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        self._load_detail(self.selected_id)

    def _load_detail(self, id_pesanan: str):
        self._clear_detail()
        try:
<<<<<<< HEAD
            db = get_db()
            doc = db.collection('pesanan').document(id_pesanan).get()
            if not doc.exists:
                return
            p = doc.to_dict()
            status = p.get("status", "")

            self.lbl_id.config(text=f"Pesanan #{id_pesanan[:8]}")
            tgl    = str(p.get("tanggal", ""))[:19]
            total  = f"Rp {p.get('total_harga', 0):,.0f}"
            self.lbl_status.config(
                text=f"📅 {tgl}   |   Status: {status.upper()}",
                fg=STATUS_COLOR.get(status, GRAY_TEXT)
            )
            self.lbl_total.config(text=f"Total: {total}")

            # Aktifkan tombol sesuai status
            if status == "pending":
                self.btn_terima.config(state="normal")
                self.btn_tolak.config(state="normal")
                self.btn_hapus.config(state="disabled")
            else:
                self.btn_terima.config(state="disabled")
                self.btn_tolak.config(state="disabled")
                self.btn_hapus.config(state="normal")

            # Detail items
            detail_rows = p.get('detail_pesanan', [])
            for dr in detail_rows:
                sub = f"Rp {dr.get('subtotal', 0):,.0f}"
                self.tree_detail.insert("", "end",
                                        values=(dr.get("nama_barang", ""), dr.get("jumlah", 0), sub))
=======
            pesanan = execute_query(
                "SELECT * FROM pesanan WHERE id_pesanan=%s",
                (id_pesanan,), fetch=True)
            if not pesanan:
                return
            p      = pesanan[0]
            status = p["status"]

            self.lbl_id.config(text=f"Pesanan  #{p['id_pesanan']}")
            self.lbl_tgl.config(text=f"📅  {str(p['tanggal'])[:19]}")
            self.lbl_total.config(text=f"Rp {p['total_harga']:,.0f}")

            # Badge status
            badge_cfg = {
                "pending":  (S_BG_PENDING,  S_PENDING,  "⏳  PENDING"),
                "diterima": (S_BG_DITERIMA, S_DITERIMA, "✅  DITERIMA"),
                "ditolak":  (S_BG_DITOLAK,  S_DITOLAK,  "❌  DITOLAK"),
            }
            bg, fg, txt = badge_cfg.get(status, (BG_MAIN, GRAY_TEXT, status.upper()))
            self.lbl_badge.config(text=txt, bg=bg, fg=fg)

            # Render tombol sesuai status
            self._render_aksi_buttons(enabled=True, status=status)

            # Detail items
            details = execute_query(
                """SELECT dp.jumlah, dp.subtotal, b.nama_barang
                   FROM detail_pesanan dp
                   JOIN barang b ON dp.id_barang = b.id_barang
                   WHERE dp.id_pesanan = %s""",
                (id_pesanan,), fetch=True)
            for d in details:
                self.tree_detail.insert(
                    "", "end",
                    values=(d["nama_barang"], d["jumlah"],
                            f"Rp {d['subtotal']:,.0f}"))

>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        except Exception as e:
            messagebox.showerror("Error DB", str(e), parent=self)

    def _clear_detail(self):
<<<<<<< HEAD
        for item in self.tree_detail.get_children():
            self.tree_detail.delete(item)
        self.lbl_id.config(text="Pilih pesanan →")
        self.lbl_status.config(text="", fg=GRAY_TEXT)
        self.lbl_total.config(text="Total: -")
        self.btn_terima.config(state="disabled")
        self.btn_tolak.config(state="disabled")
        self.btn_hapus.config(state="disabled")
=======
        for row in self.tree_detail.get_children():
            self.tree_detail.delete(row)
        self.lbl_id.config(text="Pilih pesanan dari daftar")
        self.lbl_tgl.config(text="")
        self.lbl_total.config(text="—")
        self.lbl_badge.config(text="", bg=WHITE)
        self.lbl_aksi_notif.config(text="")
        self._render_aksi_buttons(enabled=False, status=None)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

    # ── Aksi ──────────────────────────────────────────────────────────────────
    def _terima_pesanan(self):
        if not self.selected_id:
            return
        if not messagebox.askyesno(
                "Konfirmasi Terima",
                f"Terima pesanan #{self.selected_id}?\n\nStok barang akan dikurangi.",
                parent=self):
            return
        try:
<<<<<<< HEAD
            from firebase_admin import firestore
            db = get_db()
            doc_ref = db.collection('pesanan').document(self.selected_id)
            doc = doc_ref.get()
            if not doc.exists: return
            p = doc.to_dict()
            details = p.get('detail_pesanan', [])
=======
            conn   = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT id_barang, jumlah FROM detail_pesanan WHERE id_pesanan=%s",
                (self.selected_id,))
            details = cursor.fetchall()
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

            # Cek stok
            for d in details:
<<<<<<< HEAD
                b_doc = db.collection('barang').document(d["id_barang"]).get()
                if not b_doc.exists: continue
                b = b_doc.to_dict()
                if b.get("stok", 0) < d["jumlah"]:
                    messagebox.showwarning(
                        "Stok Tidak Cukup",
                        f"Stok \"{b.get('nama_barang', '')}\" tidak cukup!\n"
                        f"Tersedia: {b.get('stok', 0)}, Dibutuhkan: {d['jumlah']}",
                        parent=self
                    )
                    return

            # Kurangi stok semua item dan update status
            batch = db.batch()
            for d in details:
                b_ref = db.collection('barang').document(d["id_barang"])
                batch.update(b_ref, {'stok': firestore.Increment(-d["jumlah"])})

            batch.update(doc_ref, {'status': 'diterima'})
            batch.commit()

            messagebox.showinfo("Berhasil",
                                f"✅ Pesanan #{self.selected_id[:8]} DITERIMA!\nStok berhasil dikurangi.",
                                parent=self)
=======
                cursor.execute(
                    "SELECT nama_barang, stok FROM barang WHERE id_barang=%s",
                    (d["id_barang"],))
                barang = cursor.fetchone()
                if barang["stok"] < d["jumlah"]:
                    messagebox.showwarning(
                        "Stok Tidak Cukup",
                        f"Stok \"{barang['nama_barang']}\" tidak mencukupi!\n"
                        f"Tersedia: {barang['stok']},  Dibutuhkan: {d['jumlah']}",
                        parent=self)
                    cursor.close(); conn.close()
                    return

            # Kurangi stok
            for d in details:
                cursor.execute(
                    "UPDATE barang SET stok = stok - %s WHERE id_barang=%s",
                    (d["jumlah"], d["id_barang"]))

            # Update status
            cursor.execute(
                "UPDATE pesanan SET status='diterima' WHERE id_pesanan=%s",
                (self.selected_id,))
            conn.commit()
            cursor.close(); conn.close()

            messagebox.showinfo(
                "Berhasil",
                f"✅  Pesanan #{self.selected_id} berhasil DITERIMA!\nStok barang telah dikurangi.",
                parent=self)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
            self._refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _tolak_pesanan(self):
        if not self.selected_id:
            return
        if not messagebox.askyesno(
                "Konfirmasi Tolak",
                f"Tolak pesanan #{self.selected_id}?\n\nStok tidak akan berubah.",
                parent=self):
            return
        try:
<<<<<<< HEAD
            db = get_db()
            db.collection('pesanan').document(self.selected_id).update({'status': 'ditolak'})
            messagebox.showinfo("Info",
                                f"❌ Pesanan #{self.selected_id[:8]} DITOLAK.",
                                parent=self)
=======
            execute_query(
                "UPDATE pesanan SET status='ditolak' WHERE id_pesanan=%s",
                (self.selected_id,))
            messagebox.showinfo(
                "Info",
                f"❌  Pesanan #{self.selected_id} berhasil DITOLAK.",
                parent=self)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
            self._refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _hapus_pesanan(self):
        """Hapus satu pesanan terpilih (hanya diterima/ditolak)."""
        if not self.selected_id:
            return
        if not messagebox.askyesno(
            "Hapus Pesanan",
            f"Hapus histori pesanan #{self.selected_id[:8]} secara permanen?",
            parent=self
        ):
            return
        try:
            db = get_db()
            db.collection('pesanan').document(self.selected_id).delete()
            
            messagebox.showinfo(
                "Berhasil",
                f"🗑  Pesanan #{self.selected_id[:8]} berhasil dihapus.",
                parent=self
            )
            self._refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _hapus_semua_histori(self):
        """Hapus semua pesanan berstatus diterima atau ditolak."""
        try:
            db = get_db()
            # Firestore tidak support query IN dengan stream secara langsung untuk delete massal yang efisien tanpa loop,
            # tapi kita bisa ambil ID-nya dulu.
            docs = db.collection('pesanan').where('status', 'in', ['diterima', 'ditolak']).stream()
            doc_ids = [d.id for d in docs]
            jumlah = len(doc_ids)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
            return

        if jumlah == 0:
            messagebox.showinfo(
                "Info",
                "Tidak ada histori yang bisa dihapus.\n(Pesanan pending tidak akan dihapus.)",
                parent=self
            )
            return

        if not messagebox.askyesno(
            "Hapus Semua Histori",
            f"Akan menghapus {jumlah} pesanan (diterima & ditolak) secara permanen.\n"
            "Pesanan berstatus PENDING tidak akan terpengaruh.\n\nLanjutkan?",
            parent=self
        ):
            return

        try:
            batch = db.batch()
            for did in doc_ids:
                batch.delete(db.collection('pesanan').document(did))
            batch.commit()

            messagebox.showinfo(
                "Berhasil",
                f"🗑  {jumlah} histori pesanan berhasil dihapus.",
                parent=self
            )
            self._refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _refresh(self):
        self.selected_id = None
        self._clear_detail()
        self._load_pesanan()