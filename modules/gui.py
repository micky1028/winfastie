from logging import config
import tkinter as tk
from tkinter import messagebox
import importlib
import threading
from core.installer import SystemInstaller

class CustomScrollbar(tk.Canvas):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, width=12, highlightthickness=0, bg="#0a0a0a", **kwargs)
        self.command = command
        self.fraction_start = 0.0
        self.fraction_end = 1.0
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
    def set(self, start, end):
        self.fraction_start = float(start)
        self.fraction_end = float(end)
        self.draw()

    def draw(self):
        self.delete("all")
        self.create_rectangle(0, 0, 12, self.winfo_height(), fill="#0a0a0a", outline="")
        
        height = max(10, self.winfo_height())
        y1 = int(self.fraction_start * height)
        y2 = int(self.fraction_end * height)
        
        self.create_rectangle(3, y1, 9, y2, fill="#333333", outline="", tags="thumb")

    def on_click(self, event):
        if self.command and self.winfo_height() > 0:
            fraction = event.y / self.winfo_height()
            self.command("moveto", fraction)

    def on_drag(self, event):
        if self.command and self.winfo_height() > 0:
            fraction = max(0.0, min(1.0, event.y / self.winfo_height()))
            self.command("moveto", fraction)

class SetupApp:
    def __init__(self, root, config):
        self.root = root
        self.root.title("windows_but_fast(credits to:straykitty78)")
        
        self.root.geometry("800x580")
        self.root.resizable(False, False)
        
        self.config = config
        self.app_vars = {}
        
        self.root.config(bg="#0a0a0a")
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=800, height=580, highlightthickness=0, bg="#0a0a0a")
        self.canvas.pack(fill="both", expand=True)

        self.btn_exit = tk.Button(
            self.canvas, 
            text="✕", 
            bg="#0a0a0a", 
            fg="#ffffff", 
            font=("Consolas", 10, "bold"), 
            relief="flat",
            cursor="hand2",
            activebackground="#222222",
            activeforeground="#ffffff",
            command=self.root.destroy
        )
        self.canvas.create_window(765, 30, window=self.btn_exit, width=30, height=30)

        self.title_label = tk.Label(
            self.canvas, 
            text="windows_but_fast", 
            font=("Consolas", 16, "bold"), 
            bg="#0a0a0a", 
            fg="#ffffff"
        )
        self.canvas.create_window(400, 45, window=self.title_label)

        self.subtitle_label = tk.Label(
            self.canvas, 
            text="select software modules to deploy", 
            font=("Consolas", 9), 
            bg="#0a0a0a", 
            fg="#666666"
        )
        self.canvas.create_window(400, 75, window=self.subtitle_label)

        self.scroll_container_frame = tk.Frame(self.canvas, bg="#0a0a0a")
        self.scroll_container_frame.config(width=520, height=390)
        
        self.scroll_canvas = tk.Canvas(self.scroll_container_frame, width=490, height=390, highlightthickness=0, bg="#0a0a0a")
        
        self.scrollbar = CustomScrollbar(
            self.scroll_container_frame, 
            command=self.scroll_canvas.yview
        )
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg="#0a0a0a")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: [
                self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")),
                self.scrollbar.draw()
            ]
        )

        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scroll_container_window = self.canvas.create_window(400, 290, window=self.scroll_container_frame)

        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            self.scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            self.scrollbar.draw()
        self.scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for category_key, items in self.config.items():
            if items:
                category_title = category_key.replace("_", " ").upper()
                self.build_noir_box(category_title, items)

        self.btn_install = tk.Button(
            self.canvas, 
            text="START DEPLOYMENT", 
            bg="#ffffff", 
            fg="#0a0a0a", 
            font=("Consolas", 10, "bold"), 
            relief="flat",
            cursor="hand2",
            activebackground="#cccccc",
            activeforeground="#0a0a0a",
            command=self.start_installation
        )
        self.install_window_id = self.canvas.create_window(400, 545, window=self.btn_install, width=480, height=36)

    def build_noir_box(self, title, items):
        width = 480
        height = 45 + (len(items) * 30)
        
        box_canvas = tk.Canvas(self.scrollable_frame, width=width, height=height, highlightthickness=0, bg="#111111")
        box_canvas.pack(pady=10, padx=5)

        box_canvas.create_rectangle(0, 0, width, height, outline="#222222", width=1, fill="#111111")
        box_canvas.create_text(20, 14, text=f"// {title}", anchor="nw", fill="#888888", font=("Consolas", 9, "bold"))

        start_y = 40
        for item in items:
            var = tk.BooleanVar(value=False)
            self.app_vars[item['winget_id']] = var

            row_id = box_canvas.create_rectangle(15, start_y, width-15, start_y+26, fill="", outline="")
            chk_box = box_canvas.create_rectangle(20, start_y+5, 34, start_y+19, fill="#181818", outline="#444444", width=1)
            txt_item = box_canvas.create_text(46, start_y+4, text=item['name'], anchor="nw", fill="#aaaaaa", font=("Consolas", 9))

            def toggle(v=var, r=chk_box, t=txt_item, c=box_canvas):
                current = v.get()
                v.set(not current)
                if not current:
                    c.itemconfig(r, fill="#ffffff", outline="#ffffff")
                    c.itemconfig(t, fill="#ffffff")
                else:
                    c.itemconfig(r, fill="#181818", outline="#444444")
                    c.itemconfig(t, fill="#aaaaaa")

            box_canvas.tag_bind(row_id, "<Button-1>", lambda e, f=toggle: f())
            box_canvas.tag_bind(chk_box, "<Button-1>", lambda e, f=toggle: f())
            box_canvas.tag_bind(txt_item, "<Button-1>", lambda e, f=toggle: f())

            box_canvas.tag_bind(row_id, "<Enter>", lambda e, r=row_id, c=box_canvas: c.itemconfig(r, fill="#161616"))
            box_canvas.tag_bind(row_id, "<Leave>", lambda e, r=row_id, c=box_canvas: c.itemconfig(r, fill=""))

            start_y += 30

    def start_installation(self):
        to_install = []
        for winget_id, var in self.app_vars.items():
            if var.get():
                to_install.append(winget_id)

        if not to_install:
            messagebox.showwarning("Notice", "Select at least one module to deploy.")
            return

        self.canvas.itemconfig(self.scroll_container_window, state="hidden")
        self.canvas.itemconfig(self.install_window_id, state="hidden")

        self.subtitle_label.config(text="executing deployment sequence...")

        self.download_canvas = tk.Canvas(self.canvas, width=650, height=340, highlightthickness=0, bg="#111111")
        self.download_canvas.create_rectangle(0, 0, 650, 340, outline="#222222", width=1, fill="#111111")
        
        self.download_title = self.download_canvas.create_text(40, 30, text="PROCESSING...", anchor="nw", fill="#ffffff", font=("Consolas", 12, "bold"))
        
        self.progress_bg = self.download_canvas.create_rectangle(40, 70, 610, 92, fill="#181818", outline="#333333")
        self.progress_bar = self.download_canvas.create_rectangle(40, 70, 40, 92, fill="#ffffff", outline="")
        self.progress_text = self.download_canvas.create_text(325, 81, text="0%", anchor="center", fill="#000000", font=("Consolas", 8, "bold"))

        self.download_canvas.create_text(40, 120, text="live stream output:", anchor="nw", fill="#666666", font=("Consolas", 8, "bold"))
        self.log_box_bg = self.download_canvas.create_rectangle(40, 140, 610, 290, fill="#080808", outline="#222222")
        self.log_text = self.download_canvas.create_text(52, 155, text="system ready...", anchor="nw", fill="#cccccc", font=("Consolas", 8))

        self.download_window_id = self.canvas.create_window(400, 325, window=self.download_canvas)

        threading.Thread(target=self.run_installations_background, args=(to_install,), daemon=True).start()

    def run_installations_background(self, to_install):
        total_apps = len(to_install)
        
        for app_index, pkg_id in enumerate(to_install):
            self.root.after(0, lambda p=pkg_id, i=app_index+1: self.download_canvas.itemconfig(
                self.download_title, text=f"DEPLOYING [{i}/{total_apps}] -> {p}"
            ))
            
            base_percent = int((app_index / total_apps) * 100)
            self.update_progress(base_percent)

            for log_line in SystemInstaller.install_via_winget(pkg_id):
                if log_line:
                    clean_log = log_line[:75] + "..." if len(log_line) > 75 else log_line
                    self.root.after(0, lambda l=clean_log: self.download_canvas.itemconfig(self.log_text, text=l))
                    
                    if "%" in log_line:
                        try:
                            for part in log_line.split():
                                if "%" in part:
                                    val = int(part.replace("%", "").strip())
                                    app_share = val / total_apps
                                    total_p = int(base_percent + app_share)
                                    self.update_progress(total_p)
                                    break
                        except:
                            pass

        self.update_progress(100)
        self.root.after(0, self.installation_complete)

    def update_progress(self, percent):
        self.root.after(0, lambda p=percent: [
            self.download_canvas.coords(self.progress_bar, 40, 70, 40 + (570 * (p / 100)), 92),
            self.download_canvas.itemconfig(self.progress_text, text=f"{p}%")
        ])

    def installation_complete(self, *args):
        self.root.after(0, lambda: [
            self.download_canvas.itemconfig(self.download_title, text="DEPLOYMENT COMPLETED"),
            self.download_canvas.itemconfig(self.log_text, text="all packages successfully compiled & installed."),
            self.subtitle_label.config(text="system ready for operation"),
            self.btn_exit.config(state="normal")
        ])
        
        if not hasattr(self, 'btn_back') or self.btn_back is None:
            self.btn_back = tk.Button(
                self.canvas, 
                text="RETURN", 
                bg="#ffffff", 
                fg="#0a0a0a", 
                font=("Consolas", 10, "bold"), 
                relief="flat",
                cursor="hand2",
                activebackground="#cccccc",
                activeforeground="#0a0a0a",
                command=self.go_back_to_selection
            )
            self.root.after(0, lambda: setattr(self, 'btn_back_window', self.canvas.create_window(400, 545, window=self.btn_back, width=480, height=36)))

    def go_back_to_selection(self):
        self.canvas.delete(self.download_window_id)
        if hasattr(self, 'btn_back_window'):
            self.canvas.delete(self.btn_back_window)
            delattr(self, 'btn_back_window')

        self.canvas.itemconfig(self.scroll_container_window, state="normal")
        self.canvas.itemconfig(self.install_window_id, state="normal")

        self.subtitle_label.config(text="select software modules to deploy")