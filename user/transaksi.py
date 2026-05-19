"""
user/transaksi.py - Halaman Transaksi User (Full Redesign Premium)
Aplikasi Business Center SMKN 13 Bandung
Palet: Dark Green #051F20 → Pale Mint #DAF1DE
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import requests
from io import BytesIO

from db import get_db, get_drive_service, DRIVE_FOLDER_ID, IMAGES_DIR, API_URL

API_BASE_URL = API_URL

# ─── Palet Warna (seragam dengan login_admin.py) ──────────────────────────────
C_DARKEST   = "#051F20"   # Sidebar / header gelap
C_DARK      = "#0B2B26"   # Header hover / elemen gelap
C_MID       = "#163832"   # Tombol utama
C_MUTED     = "#235347"   # Aksen sekunder
C_MINT      = "#8EB69B"   # Border, ikon, teks sekunder hijau
C_PALE      = "#DAF1DE"   # Background input focus, badge, highlight
WHITE       = "#FFFFFF"
BG_MAIN     = "#F4FAF6"   # Background utama sedikit kehijauan
BG_CARD     = "#FFFFFF"
BG_CARD_HVR = "#F0FAF4"
BORDER_CLR  = "#D1E8D8"
DARK_TEXT   = "#1A2E22"   # Teks utama
GRAY_TEXT   = "#5C7A68"   # Teks sekunder
LIGHT_TEXT  = "#9DB8A8"   # Teks hint
STOCK_OK    = "#163832"
STOCK_LOW   = "#C07A00"
STOCK_OUT   = "#B83232"
REMOVE_CLR  = "#B83232"
SIDEBAR_W   = 300
CARD_IMG_SZ = (84, 84)
COLS        = 3


# ─── Helper: load foto produk ─────────────────────────────────────────────────
def _load_card_image(foto: str, stok: int):
<<<<<<< HEAD
    """Muat gambar produk dari local atau API. Return None jika tidak ada."""
    if not foto: return None
    try:
        # Nama file cache yang bersih
        clean_name = "".join([c for c in str(foto) if c.isalnum() or c in "._- "])
        local_filename = f"{clean_name}.png" if not clean_name.endswith(".png") else clean_name
        local_path = os.path.join(IMAGES_DIR, local_filename)

        # 1. Coba dari lokal dulu
        if os.path.isfile(local_path):
            try:
                with Image.open(local_path) as img:
                    img_ready = img.convert("RGBA")
                    return _process_card_image(img_ready, stok)
            except:
                pass
        
        # 2. Jika tidak ada di lokal, coba dari Google Drive
        try:
            service = get_drive_service()
            if not service: return None

            # Cari file ID berdasarkan nama di folder yang ditentukan
            query = f"name = '{foto}' and '{DRIVE_FOLDER_ID}' in parents and trashed = false"
            results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            items = results.get('files', [])
            
            if not items:
                # Jika tidak ketemu dengan nama, cek apakah 'foto' mungkin sebuah ID
                if "." in str(foto) or len(str(foto)) < 20:
                    pass # Bukan ID
                else:
                    file_id = foto
                    # Download media
                    request = service.files().get_media(fileId=file_id)
                    img_data = request.execute()
                    with Image.open(BytesIO(img_data)) as img:
                        img_ready = img.convert("RGBA")
                        try:
                            img_ready.save(local_path)
                        except: pass
                        return _process_card_image(img_ready, stok)
            else:
                file_id = items[0]['id']
                # Download media
                request = service.files().get_media(fileId=file_id)
                img_data = request.execute()
                with Image.open(BytesIO(img_data)) as img:
                    img_ready = img.convert("RGBA")
                    try:
                        img_ready.save(local_path)
                    except: pass
                    return _process_card_image(img_ready, stok)

        except Exception as e:
            print(f"Error fetching image from GDrive: {e}")
        
        # 3. Default jika gagal download (stok habis)
        if stok <= 0:
            with Image.new("RGBA", CARD_IMG_SIZE, (255, 255, 255, 0)) as img:
                return _process_card_image(img, stok)
            
        return None
=======
    try:
        path = os.path.join(IMAGES_DIR, foto) if foto else None
        if not (path and os.path.isfile(path)):
            return None
        img = Image.open(path).convert("RGBA")
        img.thumbnail(CARD_IMG_SZ, Image.LANCZOS)
        canvas = Image.new("RGBA", CARD_IMG_SZ, (255, 255, 255, 0))
        off = ((CARD_IMG_SZ[0]-img.width)//2, (CARD_IMG_SZ[1]-img.height)//2)
        canvas.paste(img, off, img)
        if stok <= 0:
            d = ImageDraw.Draw(canvas)
            w, h = CARD_IMG_SZ
            d.line((8,8,w-8,h-8), fill=(184,50,50,210), width=5)
            d.line((8,h-8,w-8,8), fill=(184,50,50,210), width=5)
        return ImageTk.PhotoImage(canvas)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
    except Exception:
        return None

def _process_card_image(img, stok):
    """Helper untuk memproses resize dan canvas."""
    # Buat copy agar tidak memodifikasi original jika diperlukan
    img_thumb = img.copy()
    img_thumb.thumbnail(CARD_IMG_SIZE, Image.LANCZOS)
    
    canvas = Image.new("RGBA", CARD_IMG_SIZE, (255, 255, 255, 0))
    offset = ((CARD_IMG_SIZE[0] - img_thumb.width)  // 2,
                (CARD_IMG_SIZE[1] - img_thumb.height) // 2)
    canvas.paste(img_thumb, offset, img_thumb)

    if stok <= 0:
        draw = ImageDraw.Draw(canvas)
        line_width = 8
        w, h = CARD_IMG_SIZE
        color = (204, 0, 0, 200) # PRIMARY (red) dengan alpha
        draw.line((15, 15, w-15, h-15), fill=color, width=line_width)
        draw.line((15, h-15, w-15, 15), fill=color, width=line_width)

    return ImageTk.PhotoImage(canvas)


# ─── Helper: pill button Canvas ───────────────────────────────────────────────
def _pill(parent, text, command, w=120, h=32, r=16,
          color=C_MID, hover=C_DARK, fg=WHITE,
          font=("Segoe UI", 8, "bold")):
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


# ═══════════════════════════════════════════════════════════════════════════════
class TransaksiWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master            = master
        self.keranjang         = {}
        self.barang_data       = []
        self._card_imgs        = {}
        self._checkout_enabled = False

        self.title("Transaksi — Business Center SMKN 13 Bandung")
        self.geometry("1200x700")
        self.minsize(960, 600)
        self.configure(bg=BG_MAIN)
        self._center(1200, 700)
        self._build_styles()
        self._build_ui()
        self._load_barang()
        self.grab_set()

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── ttk Styles ────────────────────────────────────────────────────────────
    def _build_styles(self):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("Thin.Vertical.TScrollbar",
                    gripcount=0, background=C_MINT,
                    troughcolor=BG_MAIN, borderwidth=0,
                    arrowsize=0, width=5)
        s.map("Thin.Vertical.TScrollbar",
              background=[("active", C_MUTED)])
        s.configure("Cart.Treeview",
                    font=("Segoe UI", 9), rowheight=34,
                    background=WHITE, fieldbackground=WHITE,
                    foreground=DARK_TEXT, borderwidth=0)
        s.configure("Cart.Treeview.Heading",
                    font=("Segoe UI", 8, "bold"),
                    background=BG_MAIN, foreground=GRAY_TEXT,
                    relief="flat", borderwidth=0)
        s.map("Cart.Treeview",
              background=[("selected", C_PALE)],
              foreground=[("selected", C_DARKEST)])

    # ── Layout Utama ──────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True)
        self._build_catalog(body)
        self._build_sidebar(body)

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=C_DARKEST, height=62)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
<<<<<<< HEAD
        tk.Label(hdr, text="Transaksi - Business Center SMKN 13 Bandung",
                 font=("Segoe UI", 13, "bold"), bg=PRIMARY, fg=WHITE).pack(
                     side="left", padx=20, pady=16)
        tk.Button(hdr, text="Kembali", font=("Segoe UI", 9),
                  bg=PRIMARY_DK, fg=WHITE, relief="flat", padx=12, pady=5,
                  cursor="hand2", command=self._kembali).pack(side="right", padx=16)
=======
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

        left_f = tk.Frame(hdr, bg=C_DARKEST)
        left_f.pack(side="left", fill="y", padx=20)
        tk.Label(left_f, text="🏪", font=("Segoe UI Emoji", 18),
                 bg=C_DARKEST).pack(side="left", padx=(0,10))
        title_col = tk.Frame(left_f, bg=C_DARKEST)
        title_col.pack(side="left", fill="y", pady=10)
        tk.Label(title_col,
                 text="Business Center  SMKN 13 Bandung",
                 font=("Segoe UI", 12, "bold"),
                 bg=C_DARKEST, fg=WHITE, anchor="w").pack(anchor="w")
        tk.Label(title_col, text="Halaman Transaksi Pelanggan",
                 font=("Segoe UI", 8),
                 bg=C_DARKEST, fg=C_MINT, anchor="w").pack(anchor="w")

        back = _pill(hdr, text="← Kembali", command=self._kembali,
                     w=110, h=34, r=17,
                     color=C_MUTED, hover=C_MID, fg=WHITE,
                     font=("Segoe UI", 9, "bold"))
        back.pack(side="right", padx=18, pady=14)
        back.config(bg=C_DARKEST)

    def _kembali(self):
        self.destroy()
        self.master.deiconify()

    # ── Panel Katalog (kiri) ───────────────────────────────────────────────────
    def _build_catalog(self, body):
        left = tk.Frame(body, bg=BG_MAIN)
        left.pack(side="left", fill="both", expand=True,
                  padx=(16,8), pady=14)

        # Search + Refresh
        sr = tk.Frame(left, bg=BG_MAIN)
        sr.pack(fill="x", pady=(0,12))

        sb_outer = tk.Frame(sr, bg=C_MINT, padx=1, pady=1)
        sb_outer.pack(side="left")
        sb_inner = tk.Frame(sb_outer, bg=WHITE)
        sb_inner.pack()
        tk.Label(sb_inner, text="🔍", font=("Segoe UI Emoji", 10),
                 bg=WHITE, fg=C_MINT).pack(side="left", padx=(10,4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_barang())
        ent = tk.Entry(sb_inner, textvariable=self.search_var,
                       font=("Segoe UI", 10), width=28,
                       relief="flat", bg=WHITE,
                       fg=DARK_TEXT, insertbackground=C_MID)
        ent.pack(side="left", ipady=9, padx=(0,10))
        ent.bind("<FocusIn>",  lambda e: sb_outer.config(bg=C_MID))
        ent.bind("<FocusOut>", lambda e: sb_outer.config(bg=C_MINT))

        btn_ref = _pill(sr, text="↻  Refresh", command=self._load_barang,
                        w=96, h=36, r=18,
                        color=BG_MAIN, hover=C_PALE, fg=C_MID,
                        font=("Segoe UI", 9, "bold"))
        btn_ref.pack(side="left", padx=10)
        btn_ref.config(bg=BG_MAIN)

        # Label section
        lrow = tk.Frame(left, bg=BG_MAIN)
        lrow.pack(fill="x", pady=(0,8))
        tk.Frame(lrow, bg=C_MID, width=4, height=20).pack(side="left")
        tk.Label(lrow, text="  Daftar Barang",
                 font=("Segoe UI", 10, "bold"),
                 bg=BG_MAIN, fg=DARK_TEXT).pack(side="left")
        self.lbl_prod_count = tk.Label(lrow, text="",
                                       font=("Segoe UI", 9),
                                       bg=BG_MAIN, fg=GRAY_TEXT)
        self.lbl_prod_count.pack(side="left", padx=6)

        # Grid scrollable
        wrap = tk.Frame(left, bg=BG_MAIN)
        wrap.pack(fill="both", expand=True)
        self.cat_canvas = tk.Canvas(wrap, bg=BG_MAIN, highlightthickness=0)
        vsb = ttk.Scrollbar(wrap, orient="vertical",
                            command=self.cat_canvas.yview,
                            style="Thin.Vertical.TScrollbar")
        self.cat_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.cat_canvas.pack(side="left", fill="both", expand=True)
        self.cat_frame = tk.Frame(self.cat_canvas, bg=BG_MAIN)
        self.cat_win   = self.cat_canvas.create_window(
            (0,0), window=self.cat_frame, anchor="nw")
        self.cat_frame.bind("<Configure>", lambda e:
            self.cat_canvas.configure(
                scrollregion=self.cat_canvas.bbox("all")))
        self.cat_canvas.bind("<Configure>", lambda e:
            self.cat_canvas.itemconfig(self.cat_win, width=e.width))
        self.cat_canvas.bind_all("<MouseWheel>",
            lambda e: self.cat_canvas.yview_scroll(
                int(-1*(e.delta/120)), "units"))

    # ── Sidebar Keranjang (kanan) ──────────────────────────────────────────────
    def _build_sidebar(self, body):
        side = tk.Frame(body, bg=WHITE, width=SIDEBAR_W)
        side.pack(side="right", fill="y", padx=(8,14), pady=14)
        side.pack_propagate(False)

        # Header sidebar
        s_hdr = tk.Frame(side, bg=C_DARKEST, height=56)
        s_hdr.pack(fill="x")
        s_hdr.pack_propagate(False)
        h_inner = tk.Frame(s_hdr, bg=C_DARKEST)
        h_inner.pack(fill="both", expand=True, padx=16)
        tk.Label(h_inner, text="🛒  Keranjang Belanja",
                 font=("Segoe UI", 11, "bold"),
                 bg=C_DARKEST, fg=WHITE).pack(side="left", pady=16)
        self.badge = tk.Label(h_inner, text="",
                              font=("Segoe UI", 8, "bold"),
                              bg=STOCK_OUT, fg=WHITE,
                              padx=7, pady=2)
        self.badge.pack(side="right", pady=18)

        # Treeview
        tree_wrap = tk.Frame(side, bg=WHITE)
        tree_wrap.pack(fill="both", expand=True)
        cols = ("Barang", "Qty", "Subtotal")
        self.cart_tree = ttk.Treeview(
            tree_wrap, columns=cols, show="headings",
            style="Cart.Treeview", selectmode="browse")
        self.cart_tree.heading("Barang",   text="Nama Barang")
        self.cart_tree.heading("Qty",      text="Qty")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.column("Barang",   width=130, anchor="w",  stretch=True)
        self.cart_tree.column("Qty",      width=34,  anchor="center", stretch=False)
        self.cart_tree.column("Subtotal", width=96,  anchor="e",  stretch=False)
        tsb = ttk.Scrollbar(tree_wrap, orient="vertical",
                            command=self.cart_tree.yview,
                            style="Thin.Vertical.TScrollbar")
        self.cart_tree.configure(yscrollcommand=tsb.set)
        tsb.pack(side="right", fill="y")
        self.cart_tree.pack(fill="both", expand=True)

        tk.Frame(side, bg=BORDER_CLR, height=1).pack(fill="x")

        # Aksi
        act = tk.Frame(side, bg=WHITE)
        act.pack(fill="x")
        tk.Button(act, text="✕  Hapus Item",
                  font=("Segoe UI", 8), bg=WHITE, fg=REMOVE_CLR,
                  relief="flat", pady=8, cursor="hand2",
                  activebackground="#FFF0F0",
                  command=self._hapus_item).pack(side="left", fill="x", expand=True)
        tk.Frame(act, bg=BORDER_CLR, width=1).pack(side="left", fill="y")
        tk.Button(act, text="🗑  Kosongkan",
                  font=("Segoe UI", 8), bg=WHITE, fg=GRAY_TEXT,
                  relief="flat", pady=8, cursor="hand2",
                  activebackground=BG_MAIN,
                  command=self._kosongkan).pack(side="left", fill="x", expand=True)

        tk.Frame(side, bg=BORDER_CLR, height=1).pack(fill="x")

        # Total
        tot_f = tk.Frame(side, bg=WHITE)
        tot_f.pack(fill="x", padx=16, pady=12)
        top = tk.Frame(tot_f, bg=WHITE)
        top.pack(fill="x")
        tk.Label(top, text="Total Belanja",
                 font=("Segoe UI", 9),
                 bg=WHITE, fg=GRAY_TEXT).pack(side="left")
        self.lbl_item_count = tk.Label(top, text="0 item",
                                       font=("Segoe UI", 8),
                                       bg=WHITE, fg=LIGHT_TEXT)
        self.lbl_item_count.pack(side="right")
        self.lbl_total = tk.Label(tot_f, text="Rp 0",
                                   font=("Segoe UI", 22, "bold"),
                                   bg=WHITE, fg=C_MID)
        self.lbl_total.pack(anchor="e", pady=(4,0))

        # Notif
        self.lbl_notif = tk.Label(side, text="",
                                   font=("Segoe UI", 8),
                                   bg=WHITE, fg=STOCK_OK,
                                   wraplength=270, justify="center")
        self.lbl_notif.pack(fill="x", padx=10, pady=(0,4))

        # Checkout canvas button
        self.checkout_cv = tk.Canvas(side, width=SIDEBAR_W, height=52,
                                      bg=WHITE, highlightthickness=0)
        self.checkout_cv.pack(fill="x")
        self._draw_checkout(False)
        self.checkout_cv.bind("<Button-1>", lambda e: self._checkout())

    def _draw_checkout(self, enabled: bool):
        cv   = self.checkout_cv
        w, h = SIDEBAR_W, 52
        fill = C_MID if enabled else C_MINT
        txt  = "CHECKOUT  →" if enabled else "Keranjang Kosong"
        cv.delete("all")
        cv.create_rectangle(0, 0, w, h, fill=fill, outline=fill)
        cv.create_text(w//2, h//2, text=txt,
                       fill=WHITE, font=("Segoe UI", 12, "bold"),
                       anchor="center")
        cv.config(cursor="hand2" if enabled else "arrow")
        self._checkout_enabled = enabled
        if enabled:
            cv.bind("<Enter>", lambda e: (
                cv.delete("all"),
                cv.create_rectangle(0,0,w,h,fill=C_DARK,outline=C_DARK),
                cv.create_text(w//2,h//2,text=txt,fill=WHITE,
                               font=("Segoe UI",12,"bold"),anchor="center")))
            cv.bind("<Leave>", lambda e: self._draw_checkout(True))
        else:
            cv.unbind("<Enter>")
            cv.unbind("<Leave>")

    # ── Load & Render ──────────────────────────────────────────────────────────
    def _load_barang(self):
        try:
<<<<<<< HEAD
            db = get_db()
            docs = db.collection('barang').stream()
            self.barang_data = []
            for doc in docs:
                b = doc.to_dict()
                b["id_barang"] = doc.id
                self.barang_data.append(b)
            self.barang_data.sort(key=lambda x: x.get("nama_barang", "").lower())
=======
            self.barang_data = execute_query(
                "SELECT id_barang, nama_barang, harga_barang, stok, foto "
                "FROM barang ORDER BY nama_barang",
                fetch=True)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        except Exception as e:
            messagebox.showerror("Error DB", str(e), parent=self)
            self.barang_data = []
        self.search_var.set("")
        self._render_katalog(self.barang_data)

    def _filter_barang(self):
        kw = self.search_var.get().lower()
        self._render_katalog(
            [b for b in self.barang_data
             if kw in b["nama_barang"].lower()])

    def _render_katalog(self, data):
        for w in self.cat_frame.winfo_children():
            w.destroy()
        self._card_imgs.clear()
        self.lbl_prod_count.config(
            text=f"({len(data)} produk)" if data else "")
        for idx, item in enumerate(data):
<<<<<<< HEAD
            try:
                r, c = divmod(idx, COLS)
                self._make_card(item, r, c)
                self.cat_frame.grid_columnconfigure(c, weight=1)
            except Exception as e:
                print(f"Error rendering item {item.get('id_barang')}: {e}")
                continue

=======
            r, c = divmod(idx, COLS)
            self._make_card(item, r, c)
        for c in range(COLS):
            self.cat_frame.grid_columnconfigure(c, weight=1, uniform="col")
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        if not data:
            tk.Label(self.cat_frame,
                     text="Tidak ada produk ditemukan.",
                     font=("Segoe UI", 11),
                     bg=BG_MAIN, fg=LIGHT_TEXT
                     ).grid(column=0, row=0, columnspan=COLS,
                            padx=20, pady=60)

    def _make_card(self, item, row, col):
        id_b  = item["id_barang"]
        nama  = item["nama_barang"]
        try:
            harga = float(item["harga_barang"] or 0)
        except (ValueError, TypeError):
            harga = 0
        stok  = item["stok"]
        foto  = item.get("foto")
        oos   = stok <= 0

        card = tk.Frame(self.cat_frame, bg=BG_CARD,
                        highlightbackground=BORDER_CLR,
                        highlightthickness=1,
                        width=208, height=222)
        card.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
        card.pack_propagate(False)
        card.grid_propagate(False)

        # Garis aksen atas
        tk.Frame(card, bg=C_MINT if not oos else "#CCCCCC",
                 height=3).pack(fill="x")

        # Area gambar
        img_area = tk.Frame(card,
                            bg=C_PALE if not oos else "#F0F0F0",
                            width=84, height=84)
        img_area.pack(pady=(12,4))
        img_area.pack_propagate(False)

        photo = _load_card_image(foto, stok)
        if photo:
            self._card_imgs[id_b] = photo
            tk.Label(img_area, image=photo,
                     bg=img_area["bg"]).pack(expand=True)
        else:
            if oos:
                cv_ph = tk.Canvas(img_area, width=84, height=84,
                                  bg="#F0F0F0", highlightthickness=0)
                cv_ph.pack()
                cv_ph.create_text(42,42,text="📦",
                                  font=("Segoe UI Emoji",24), fill="#CCCCCC")
                cv_ph.create_line(10,10,74,74,fill=STOCK_OUT,width=4)
                cv_ph.create_line(10,74,74,10,fill=STOCK_OUT,width=4)
            else:
                tk.Label(img_area, text="📦",
                         font=("Segoe UI Emoji", 28),
                         bg=C_PALE).pack(expand=True)

        # Nama
        tk.Label(card, text=nama,
                 font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=DARK_TEXT,
                 wraplength=188, justify="center").pack(padx=6)

        # Harga
        tk.Label(card, text=f"Rp {harga:,.0f}",
                 font=("Segoe UI", 11, "bold"),
                 bg=BG_CARD, fg=C_MID).pack(pady=(1,0))

        # Stok
        if stok > 5:
            sc, st = STOCK_OK,  f"● Stok: {stok}"
        elif stok > 0:
            sc, st = STOCK_LOW, f"⚠ Stok: {stok} (menipis)"
        else:
            sc, st = STOCK_OUT, "✕ Stok Habis"
        tk.Label(card, text=st, font=("Segoe UI", 7, "bold"),
                 bg=BG_CARD, fg=sc).pack()

        # Tombol / label
        if not oos:
            btn = _pill(card, text="+ Tambah",
                        command=lambda i=item: self._tambah_ke_keranjang(i),
                        w=116, h=30, r=15,
                        color=C_MID, hover=C_DARK,
                        font=("Segoe UI", 8, "bold"))
            btn.pack(pady=(5,10))
            btn.config(bg=BG_CARD)
            card.bind("<Enter>", lambda e, c=card: (
                c.config(bg=BG_CARD_HVR,
                         highlightbackground=C_MINT)))
            card.bind("<Leave>", lambda e, c=card: (
                c.config(bg=BG_CARD,
                         highlightbackground=BORDER_CLR)))
        else:
            tk.Label(card, text="Tidak Tersedia",
                     font=("Segoe UI", 8), bg=BG_CARD,
                     fg=LIGHT_TEXT).pack(pady=(5,10))

    # ── Logika Keranjang ──────────────────────────────────────────────────────
    def _tambah_ke_keranjang(self, item):
        id_b = item["id_barang"]
        try:
<<<<<<< HEAD
            db = get_db()
            doc = db.collection('barang').document(id_b).get()
            stok_db = doc.to_dict().get("stok", 0) if doc.exists else 0
=======
            cur     = execute_query(
                "SELECT stok FROM barang WHERE id_barang=%s",
                (id_b,), fetch=True)
            stok_db = cur[0]["stok"] if cur else 0
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        except Exception:
            stok_db = item.get("stok", 0)

        if id_b in self.keranjang:
            if self.keranjang[id_b]["jumlah"] >= stok_db:
<<<<<<< HEAD
                self._notif(f"Stok \"{item.get('nama_barang', '')}\" tidak mencukupi!", error=True)
                return
            self.keranjang[id_b]["jumlah"] += 1
        else:
            if stok_db <= 0:
                self._notif("Stok habis!", error=True)
                return
            self.keranjang[id_b] = {
                "nama": item.get("nama_barang", ""), "harga": float(item.get("harga_barang", 0)),
                "jumlah": 1, "stok": stok_db
            }
        self._update_cart_ui()
        self._notif(f"\"{item.get('nama_barang', '')}\" ditambahkan.")

    def _hapus_item(self):
        sel = self.cart_tree.selection()
        if sel:
            del self.keranjang[str(sel[0])]
            self._update_cart_ui()
=======
                self._notif(f"Stok \"{item['nama_barang']}\" tidak mencukupi!", err=True)
                return
            self.keranjang[id_b]["jumlah"] += 1
        else:
            if stok_db == 0:
                self._notif("Stok habis!", err=True)
                return
            self.keranjang[id_b] = {
                "nama":   item["nama_barang"],
                "harga":  float(item["harga_barang"]),
                "jumlah": 1,
                "stok":   stok_db,
            }
        self._update_cart()
        self._notif(f"✓  \"{item['nama_barang']}\" ditambahkan.")

    def _hapus_item(self):
        sel = self.cart_tree.selection()
        if not sel:
            self._notif("Pilih item yang ingin dihapus.", err=True)
            return
        id_b = int(sel[0])
        nama = self.keranjang[id_b]["nama"]
        del self.keranjang[id_b]
        self._update_cart()
        self._notif(f"✕  \"{nama}\" dihapus.")
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)

    def _kosongkan(self):
        if not self.keranjang:
            return
        if messagebox.askyesno("Kosongkan Keranjang",
                                "Yakin ingin mengosongkan keranjang?",
                                parent=self):
            self.keranjang.clear()
            self._update_cart()

    def _update_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        total = 0
        total_qty = 0
        for id_b, d in self.keranjang.items():
            sub        = d["harga"] * d["jumlah"]
            total     += sub
            total_qty += d["jumlah"]
            self.cart_tree.insert(
                "", "end", iid=str(id_b),
                values=(d["nama"], d["jumlah"], f"Rp {sub:,.0f}"))
        n = len(self.keranjang)
        self.lbl_total.config(text=f"Rp {total:,.0f}")
        self.lbl_item_count.config(
            text=f"{n} jenis · {total_qty} item" if n else "0 item")
        self.badge.config(text=f" {n} " if n else "")
        self._draw_checkout(enabled=n > 0)

    # ── Checkout ──────────────────────────────────────────────────────────────
    def _checkout(self):
        if not self._checkout_enabled or not self.keranjang:
            return
        total     = sum(v["harga"]*v["jumlah"] for v in self.keranjang.values())
        item_list = "\n".join(
            f"  • {v['nama']}  x{v['jumlah']}  =  Rp {v['harga']*v['jumlah']:,.0f}"
            for v in self.keranjang.values())
        if not messagebox.askyesno(
                "Konfirmasi Pesanan",
                f"Pesanan Anda:\n{item_list}\n\n"
                f"Total: Rp {total:,.0f}\n\n"
                "Lanjutkan? (Menunggu konfirmasi admin)",
                parent=self):
            return
        try:
<<<<<<< HEAD
            import datetime
            db = get_db()
            doc_ref = db.collection('pesanan').document()
            
            details = []
            for id_b, d in self.keranjang.items():
                details.append({
                    "id_barang": id_b,
                    "nama_barang": d["nama"],
                    "jumlah": d["jumlah"],
                    "subtotal": d["harga"] * d["jumlah"]
                })
            
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            doc_ref.set({
                "tanggal": now_str,
                "total_harga": total,
                "status": "pending",
                "detail_pesanan": details
            })
            
            id_pesanan = doc_ref.id[:8]
=======
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pesanan (total_harga, status) VALUES (%s,'pending')",
                (total,))
            id_pesanan = cursor.lastrowid
            for id_b, d in self.keranjang.items():
                cursor.execute(
                    "INSERT INTO detail_pesanan "
                    "(id_pesanan, id_barang, jumlah, subtotal) "
                    "VALUES (%s,%s,%s,%s)",
                    (id_pesanan, id_b, d["jumlah"], d["harga"]*d["jumlah"]))
            conn.commit()
            cursor.close()
            conn.close()
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
            self._show_sukses(id_pesanan, total)
            self.keranjang.clear()
            self._update_cart()
            self._load_barang()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    # ── Popup Sukses ──────────────────────────────────────────────────────────
    def _show_sukses(self, id_pesanan, total):
        pop = tk.Toplevel(self)
        pop.title("Pesanan Berhasil")
        pop.geometry("400x320")
        pop.resizable(False, False)
        pop.configure(bg=WHITE)
        pop.transient(self)
        pop.grab_set()
        x = self.winfo_x() + (self.winfo_width()  - 400) // 2
        y = self.winfo_y() + (self.winfo_height() - 320) // 2
        pop.geometry(f"400x320+{x}+{y}")

        tk.Frame(pop, bg=C_DARKEST, height=6).pack(fill="x")

        ic = tk.Frame(pop, bg=C_PALE, width=68, height=68)
        ic.pack(pady=(24,6))
        ic.pack_propagate(False)
        tk.Label(ic, text="✓", font=("Segoe UI", 30, "bold"),
                 bg=C_PALE, fg=C_MID).pack(expand=True)

        tk.Label(pop, text="Pesanan Berhasil!",
                 font=("Segoe UI", 15, "bold"),
                 bg=WHITE, fg=DARK_TEXT).pack()
        tk.Label(pop, text=f"ID Pesanan: #{id_pesanan}",
                 font=("Segoe UI", 9),
                 bg=WHITE, fg=GRAY_TEXT).pack(pady=(2,0))
        tk.Label(pop, text=f"Rp {total:,.0f}",
                 font=("Segoe UI", 20, "bold"),
                 bg=WHITE, fg=C_MID).pack(pady=6)
        tk.Label(pop, text="Menunggu konfirmasi admin...",
                 font=("Segoe UI", 9),
                 bg=WHITE, fg=STOCK_LOW).pack()

<<<<<<< HEAD
    def _kembali(self):
        """Tutup window transaksi dan kembali ke halaman pilih mode."""
        if hasattr(self.master, "_on_child_close"):
            self.master._on_child_close(self)
        else:
            self.destroy()
            self.master.deiconify()

    def _notif(self, msg: str, error: bool = False):
        self.lbl_notif.config(text=msg, fg=PRIMARY if error else ACCENT_G)
=======
        ok_btn = _pill(pop, text="OK, Tutup", command=pop.destroy,
                       w=160, h=40, r=20,
                       color=C_MID, hover=C_DARK,
                       font=("Segoe UI", 10, "bold"))
        ok_btn.config(bg=WHITE)
        ok_btn.pack(pady=18)

    # ── Notifikasi ────────────────────────────────────────────────────────────
    def _notif(self, msg: str, err: bool = False):
        self.lbl_notif.config(
            text=msg, fg=STOCK_OUT if err else STOCK_OK)
>>>>>>> 0e8bd3a (feat: redesign halaman utama dan login admin)
        if msg:
            self.after(3000, lambda: self.lbl_notif.config(text=""))