import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from core.focus_engine import FocusTimer
from core.stats_manager import load_stats, add_completed_session
from core.process_manager import (
    block_apps,
    start_monitoring,
    stop_monitoring
)
from core.website_blocker import (
    block_websites,
    unblock_websites
)
from core.logger import add_log, get_logs
from core.config_manager import load_config, save_config
import os

# =========================
# APP CONFIG
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# =========================
# MAIN APP
# =========================

class FocusOS(ctk.CTk):

    def __init__(self):
        super().__init__()
        

        # Window
        self.title("FocusOS v2")
        self.geometry("1400x850")
        self.minsize(1200, 700)

        self.configure(fg_color="#0B1020")

        # Theme colors
        self.theme_color = "#8B5CF6"
        self.stats = load_stats()
        # Timer engine
        self.timer_engine = FocusTimer(
        self.update_timer_display,
        self.timer_finished )
        self.config_data = load_config()

        self.distracting_apps = self.config_data["distracting_apps"]

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color="#111827"
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main content
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#0B1020",
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Build UI
        self.create_sidebar()
        self.show_dashboard()

    # =========================
    # SIDEBAR
    # =========================

    def create_sidebar(self):

        title = ctk.CTkLabel(
            self.sidebar,
            text="FocusOS",
            font=("Segoe UI", 30, "bold")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="AI Productivity System",
            text_color="#9CA3AF",
            font=("Segoe UI", 14)
        )
        subtitle.pack(pady=(0, 30))

        # Navigation buttons
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("🎯 Focus Session", self.show_focus),
            ("📊 Analytics", self.show_analytics),
            ("⚙ Configuration", self.show_config),
            ("📁 Logs", self.show_logs),
        ]

        for text, command in nav_items:

            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=50,
                corner_radius=14,
                fg_color="#1F2937",
                hover_color=self.theme_color,
                anchor="w",
                font=("Segoe UI", 15, "bold")
            )

            btn.pack(fill="x", padx=20, pady=8)

        # Bottom status
        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(side="bottom", pady=30)

        status = ctk.CTkLabel(
            bottom_frame,
            text="● System Active",
            text_color="#10B981",
            font=("Segoe UI", 14, "bold")
        )

        status.pack()

    # =========================
    # CLEAR MAIN
    # =========================

    def clear_main(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =========================
    # ACTIVITY FEED
    # =========================

    def update_activity_feed(self):

        try:

            logs = get_logs()

            self.activity_box.delete("0.0", "end")

            for log in logs:
                self.activity_box.insert("end", f"{log}\n")

            self.after(2000, self.update_activity_feed)

        except:
            pass

    # =========================
    # DASHBOARD
    # =========================
    # =========================
    # TIMER CALLBACKS
    # =========================

    def update_timer_display(self, text):

        try:
            self.timer_label.configure(text=text)
        except:
            pass

    def timer_finished(self):
        stop_monitoring()

        add_log("✅ Focus session completed")

        unblock_websites()

        minutes = int(self.timer_option.get())

        self.stats = add_completed_session(minutes)

        try:
            self.timer_label.configure(text="DONE!")
        except:
            pass

        self.show_dashboard()

    # =========================
    # TIMER CONTROLS
    # =========================

    def start_focus(self):
        add_log("🟢 Focus session started")
        block_websites()

        start_monitoring(self.distracting_apps)

        minutes = int(self.timer_option.get())

        self.timer_engine.start(minutes)

    def pause_focus(self):

        self.timer_engine.pause()

    def resume_focus(self):

        self.timer_engine.resume()

    def stop_focus(self):
        add_log("🔴 Focus session stopped")

        stop_monitoring()

        unblock_websites()

        self.timer_engine.stop()

    def show_dashboard(self):

        self.clear_main()

        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="Dashboard",
            font=("Segoe UI", 38, "bold")
        )

        header.pack(anchor="w", padx=40, pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Monitor your productivity and stay focused 🚀",
            text_color="#9CA3AF",
            font=("Segoe UI", 16)
        )

        subtitle.pack(anchor="w", padx=40)

        # Cards container
        card_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        card_frame.pack(fill="x", padx=30, pady=30)

        # Grid
        card_frame.grid_columnconfigure((0,1,2,3), weight=1)

        metrics = [

            ("🔥 Focus Score", f"{self.stats['focus_score']}%"),

            ("⏳ Focus Hours", f"{self.stats['focus_hours']:.1f}h"),

            ("🚫 Distractions Blocked",
             str(self.stats['distractions_blocked'])),

            ("🏆 Level",
             str(self.stats['level']))
        ]

        for i, (title, value) in enumerate(metrics):

            card = ctk.CTkFrame(
                card_frame,
                height=160,
                corner_radius=22,
                fg_color="#111827"
            )

            card.grid(row=0, column=i, padx=15, sticky="nsew")

            card.grid_rowconfigure(0, weight=1)

            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI", 18, "bold"),
                text_color="#D1D5DB"
            )

            title_label.pack(pady=(30, 10))

            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Segoe UI", 40, "bold"),
                text_color=self.theme_color
            )

            value_label.pack()

        # Activity panel
        activity = ctk.CTkFrame(
            self.main_frame,
            corner_radius=22,
            fg_color="#111827"
        )

        activity.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        activity_title = ctk.CTkLabel(
            activity,
            text="Live Productivity Feed",
            font=("Segoe UI", 24, "bold")
        )

        activity_title.pack(anchor="w", padx=30, pady=(25, 20))

        self.activity_box = ctk.CTkTextbox(
            activity,
            corner_radius=16,
            font=("Consolas", 14)
        )

        self.activity_box.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        self.update_activity_feed()



    # =========================
    # FOCUS SESSION
    # =========================

    def show_focus(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Focus Session",
            font=("Segoe UI", 36, "bold")
        )

        title.pack(anchor="w", padx=40, pady=30)

        timer_card = ctk.CTkFrame(
            self.main_frame,
            height=350,
            corner_radius=30,
            fg_color="#111827"
        )

        timer_card.pack(fill="x", padx=40, pady=20)

        self.timer_option = ctk.CTkOptionMenu(
            timer_card,
            values=["25", "50", "90", "120"],
            width=200,
            height=40,
            font=("Segoe UI", 16)
        )

        self.timer_option.set("50")

        self.timer_option.pack(pady=(30, 10))

        timer_title = ctk.CTkLabel(
            timer_card,
            text="Deep Focus Timer",
            font=("Segoe UI", 24, "bold")
        )

        timer_title.pack(pady=(35, 20))

        self.timer_label = ctk.CTkLabel(
            timer_card,
            text="50:00",
            font=("Segoe UI", 90, "bold"),
            text_color=self.theme_color
        )

        self.timer_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(
            timer_card,
            fg_color="transparent"
        )

        btn_frame.pack(pady=25)

        buttons = [
            ("▶ Start", "#10B981", self.start_focus),
            ("⏸ Pause", "#F59E0B", self.pause_focus),
            ("▶ Resume", "#3B82F6", self.resume_focus),
            ("⏹ Stop", "#EF4444", self.stop_focus)
        ]

        for text, color, command in buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=command,
                width=140,
                height=50,
                corner_radius=14,
                fg_color=color,
                hover_color=color
            )

            btn.pack(side="left", padx=12)

    # =========================
    # ANALYTICS
    # =========================

    def show_analytics(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Analytics",
            font=("Segoe UI", 36, "bold")
        )

        title.pack(anchor="w", padx=40, pady=30)

        analytics_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=22,
            fg_color="#111827"
        )

        analytics_card.pack(fill="both", expand=True, padx=40, pady=20)

        stats = [

            f"🔥 Current Focus Score: {self.stats['focus_score']}%",

            f"⏳ Total Focus Hours: {self.stats['focus_hours']:.1f}h",

            f"🚫 Distractions Blocked: {self.stats['distractions_blocked']}",

            f"🏆 Current Level: {self.stats['level']}",

            f"🎯 Sessions Completed: {self.stats['focus_score'] // 5}"
        ]

        for stat in stats:

            label = ctk.CTkLabel(
                analytics_card,
                text=stat,
                font=("Segoe UI", 20),
                anchor="w"
            )

            label.pack(anchor="w", padx=30, pady=20)

    # =========================
    # CONFIG
    # =========================

    def show_config(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="Configuration",
            font=("Segoe UI", 36, "bold")
        )

        title.pack(anchor="w", padx=40, pady=30)

        frame = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=22,
            fg_color="#111827"
        )

        frame.pack(fill="both", expand=True, padx=40, pady=20)

        frame.grid_columnconfigure(0, weight=1)
        # Productive Apps
        label1 = ctk.CTkLabel(
            frame,
            text="📘 Productive Apps",
            font=("Segoe UI", 20, "bold")
        )
        label1.pack(anchor="w", padx=25, pady=(25, 8))

        self.productive_apps_box = ctk.CTkTextbox(
            frame,
            height=100
        )
        self.productive_apps_box.pack(fill="x", padx=25)

        self.productive_apps_box.insert(
            "0.0",
            "\n".join(self.config_data["productive_apps"])
        )

        # Distracting Apps
        label2 = ctk.CTkLabel(
            frame,
            text="🚫 Distracting Apps",
            font=("Segoe UI", 20, "bold")
        )
        label2.pack(anchor="w", padx=25, pady=(25, 8))

        self.distracting_apps_box = ctk.CTkTextbox(
            frame,
            height=100
        )
        self.distracting_apps_box.pack(fill="x", padx=25)

        self.distracting_apps_box.insert(
            "0.0",
            "\n".join(self.config_data["distracting_apps"])
        )

        # Productive Sites
        label3 = ctk.CTkLabel(
            frame,
            text="🌐 Productive Sites",
            font=("Segoe UI", 20, "bold")
        )
        label3.pack(anchor="w", padx=25, pady=(25, 8))

        self.productive_sites_box = ctk.CTkTextbox(
            frame,
            height=100
        )
        self.productive_sites_box.pack(fill="x", padx=25)

        self.productive_sites_box.insert(
            "0.0",
            "\n".join(self.config_data["productive_sites"])
        )

        # Distracting Sites
        label4 = ctk.CTkLabel(
            frame,
            text="❌ Distracting Sites",
            font=("Segoe UI", 20, "bold")
        )
        label4.pack(anchor="w", padx=25, pady=(25, 8))

        self.distracting_sites_box = ctk.CTkTextbox(
            frame,
            height=100
        )
        self.distracting_sites_box.pack(fill="x", padx=25)

        self.distracting_sites_box.insert(
            "0.0",
            "\n".join(self.config_data["distracting_sites"])
        )

        # SAVE BUTTON

        save_btn = ctk.CTkButton(
            frame,
            text="💾 Save Configuration",
            height=50,
            width=260,
            corner_radius=14,
            fg_color=self.theme_color,
            hover_color="#7C3AED",
            font=("Segoe UI", 16, "bold"),
            command=self.save_user_config
        )

        save_btn.pack(pady=30)

    # =========================
    # SAVE USER CONFIG
    # =========================

    def save_user_config(self):

        self.config_data["productive_apps"] = (
            self.productive_apps_box.get("0.0", "end")
            .strip()
            .split("\n")
        )

        self.config_data["distracting_apps"] = (
            self.distracting_apps_box.get("0.0", "end")
            .strip()
            .split("\n")
        )

        self.config_data["productive_sites"] = (
            self.productive_sites_box.get("0.0", "end")
            .strip()
            .split("\n")
        )

        self.config_data["distracting_sites"] = (
            self.distracting_sites_box.get("0.0", "end")
            .strip()
            .split("\n")
        )

        save_config(self.config_data)

        self.distracting_apps = (
            self.config_data["distracting_apps"]
        )

        add_log("💾 Configuration saved")
        CTkMessagebox(
            title="Saved",
            message="Configuration saved successfully 🔥",
            icon="check"
        )

    # =========================
    # LOGS
    # =========================

    def show_logs(self):

        self.clear_main()

        title = ctk.CTkLabel(
            self.main_frame,
            text="System Logs",
            font=("Segoe UI", 36, "bold")
        )

        title.pack(anchor="w", padx=40, pady=30)

        log_box = ctk.CTkTextbox(
            self.main_frame,
            corner_radius=20,
            font=("Consolas", 14)
        )

        log_box.pack(fill="both", expand=True, padx=40, pady=20)

        logs = get_logs()

        for log in logs:
            log_box.insert("end", f"{log}\n")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app = FocusOS()
    app.mainloop()