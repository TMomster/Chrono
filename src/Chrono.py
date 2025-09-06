import tkinter as tk
import time

class ElegantTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrono")
        self.root.geometry("400x350")  # 增加高度以容纳菜单栏
        self.root.configure(bg="#212529")
        
        # 移除窗口装饰并设置为无边框窗口
        self.root.overrideredirect(True)
        
        # 主题状态：0为浅色模式，1为深色模式
        self.theme_mode = 1
        self.animating = False  # 防止动画冲突
        
        # 语言状态：0为中文，1为英文
        self.language_mode = 0
        
        # 菜单状态
        self.menu_open = False
        
        # 关于窗口实例
        self.about_window = None
        
        # 计时器状态变量
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.last_update = 0
        
        # 鼠标拖动相关变量
        self.drag_threshold = 5  # 拖动阈值（像素）
        self.is_dragging = False
        self.mouse_pressed = False
        self.press_start_x = 0
        self.press_start_y = 0
        self.window_start_x = 0
        self.window_start_y = 0
        
        # 标记是否点击了菜单相关组件
        self.clicked_menu_item = False
        
        # 主题配置
        self.themes = [
            {  # 浅色主题
                'bg': '#f8f9fa',
                'fg': '#2c3e50',
                'status_fg': '#6c757d',
                'active_fg': '#28a745',
                'pause_fg': '#dc3545',
                'hint_fg': '#adb5bd',
                'separator': '#e9ecef',
                'button_hover': '#e9ecef',
                'window_border': '#dee2e6',
                'confirm_button': '#28a745',
                'scrollbar_bg': '#dee2e6',
                'scrollbar_thumb': '#adb5bd'
            },
            {  # 深色主题
                'bg': '#212529',
                'fg': '#f8f9fa',
                'status_fg': '#adb5bd',
                'active_fg': '#4caf50',
                'pause_fg': '#f44336',
                'hint_fg': '#6c757d',
                'separator': '#495057',
                'button_hover': '#343a40',
                'window_border': '#343a40',
                'confirm_button': '#4caf50',
                'scrollbar_bg': '#343a40',
                'scrollbar_thumb': '#6c757d'
            }
        ]
        
        # 语言配置
        self.languages = [
            {  # 中文
                'title': 'Chrono',
                'status_start': '点击开始计时',
                'status_running': '进行中',
                'status_paused': '暂停',
                'status_reset': '已复位',
                'reset_hint_running': '点击暂停',
                'reset_hint_paused': '按空格键复位',
                'reset_hint_reset': '点击"更多"查看选项',
                'more_button': '更多',
                'theme_menu_light': '浅色模式',
                'theme_menu_dark': '深色模式',
                'language_menu': '英文',
                'about_menu': '关于',
                'minimize': '—',
                'close': '×',
                'about_title': '关于 Chrono',
                'version_info': '版本: 1.0.0\n开发者: Momster\n2024, 保留所有权利',
                'help_content': '''使用说明:

1. 开始/暂停计时
   - 点击时间显示区域
   - 或按回车键(ENTER)

2. 重置计时器
   - 在暂停状态下按空格键
   - 或在暂停状态下按ESC键

3. 切换主题
   - 按R键
   - 或点击"更多"菜单中的主题选项

4. 切换语言
   - 点击"更多"菜单中的语言选项

5. 窗口操作
   - 拖动标题栏移动窗口
   - 点击"-"最小化窗口
   - 点击"×"关闭程序

6. 紧急关闭
   - 按F4键可立即关闭程序

快捷键列表:
- 空格键: 暂停时重置
- 回车键: 开始/暂停
- ESC键: 暂停时复位
- R键: 切换深色或浅色模式
- H键: 显示关于信息
- F4键: 紧急关闭

其他:
- 计时精度为0.01秒
- 支持小时显示(超过60分钟)
- 主题切换有平滑动画效果
- 界面可自由拖动
'''
            },
            {  # 英文
                'title': 'Chrono',
                'status_start': 'Click to start timing',
                'status_running': 'Running',
                'status_paused': 'Paused',
                'status_reset': 'Reset',
                'reset_hint_running': 'Click to pause',
                'reset_hint_paused': 'Press SPACE to reset',
                'reset_hint_reset': 'Click "More" for options',
                'more_button': 'More',
                'theme_menu_light': 'Light Mode',
                'theme_menu_dark': 'Dark Mode',
                'language_menu': 'Chinese',
                'about_menu': 'About',
                'minimize': '—',
                'close': '×',
                'about_title': 'About Chrono',
                'version_info': 'Version: 1.0.0\nDeveloper: Momster\n2024, All Rights Reserved',
                'help_content': '''Usage Instructions:

1. Start/Pause Timer
   - Click on the time display area
   - Or press ENTER key

2. Reset Timer
   - Press SPACE key when paused
   - Or press ESC key when paused

3. Toggle Theme
   - Press R key
   - Or click theme option in "More" menu

4. Switch Language
   - Click language option in "More" menu

5. Window Operations
   - Drag the title bar to move window
   - Click "-" to minimize window
   - Click "×" to close program

6. Emergency Close
   - Press F4 key to close immediately

Shortcut Keys:
- Space: Reset when paused
- Enter: Start/Pause
- ESC: Reset when paused
- R: Toggle theme
- H: Show about information
- F4: Emergency close

What's More:
- Timing precision: 0.01 seconds
- Hours display supported (over 60 minutes)
- Smooth animation for theme switching
- Window can be dragged freely
'''
            }
        ]
        
        # 用于渐变动画的颜色值
        self.current_colors = self.themes[1].copy()
        
        # 菜单窗口实例
        self.menu_window = None
        
        # 创建界面
        self.create_widgets()
        
        # 绑定事件
        self.root.bind("<space>", self.handle_space_key)
        self.root.bind("<Return>", self.handle_enter_key)
        self.root.bind("<Escape>", self.handle_escape_key)
        self.root.bind("<r>", self.start_theme_transition)
        self.root.bind("<h>", self.show_about)
        self.root.bind("<H>", self.show_about)
        self.root.bind("<F4>", self.handle_f4_key)  # F4紧急关闭
        self.root.bind("<Key>", self.on_key_press)
        
        # 绑定整个窗口的鼠标事件
        self.root.bind("<ButtonPress-1>", self.on_window_press)
        self.root.bind("<ButtonRelease-1>", self.on_window_release)
        self.root.bind("<B1-Motion>", self.on_window_motion)
        
        # 确保窗口能接收键盘事件
        self.root.focus_set()
        
        # 初始更新
        self.update_display()
        self.center_window(self.root, 400, 350)
    
    def create_widgets(self):
        # 主容器
        self.main_frame = tk.Frame(
            self.root, 
            bg=self.current_colors['bg'], 
            padx=20, 
            pady=20,
            highlightthickness=1,
            highlightbackground=self.current_colors['window_border']
        )
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)
        
        # 标题栏框架（包含菜单和控制按钮）
        self.title_frame = tk.Frame(self.main_frame, bg=self.current_colors['bg'])
        self.title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左侧菜单按钮框架
        self.menu_frame = tk.Frame(self.title_frame, bg=self.current_colors['bg'])
        self.menu_frame.pack(side=tk.LEFT)
        
        # 更多按钮
        self.more_button = tk.Label(
            self.menu_frame,
            text=self.languages[self.language_mode]['more_button'],
            font=("Helvetica", 9),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg'],
            padx=8,
            pady=2,
            cursor="hand2"
        )
        self.more_button.pack(side=tk.LEFT)
        self.more_button.bind("<Button-1>", self.toggle_menu)
        self.more_button.bind("<Enter>", self.on_control_enter)
        self.more_button.bind("<Leave>", self.on_control_leave)
        
        # 标题文本（居中）
        self.title_label = tk.Label(
            self.title_frame,
            text=self.languages[self.language_mode]['title'],
            font=("Helvetica", 10),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 右侧窗口控制按钮框架
        self.control_frame = tk.Frame(self.title_frame, bg=self.current_colors['bg'])
        self.control_frame.pack(side=tk.RIGHT)
        
        # 最小化按钮
        self.minimize_btn = tk.Label(
            self.control_frame,
            text=self.languages[self.language_mode]['minimize'],
            font=("Helvetica", 12),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg'],
            padx=8,
            pady=2,
            cursor="hand2"
        )
        self.minimize_btn.pack(side=tk.LEFT, padx=2)
        self.minimize_btn.bind("<Button-1>", self.minimize_window)
        self.minimize_btn.bind("<Enter>", self.on_control_enter)
        self.minimize_btn.bind("<Leave>", self.on_control_leave)
        
        # 关闭按钮
        self.close_btn = tk.Label(
            self.control_frame,
            text=self.languages[self.language_mode]['close'],
            font=("Helvetica", 14),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg'],
            padx=6,
            pady=0,
            cursor="hand2"
        )
        self.close_btn.pack(side=tk.LEFT, padx=2)
        self.close_btn.bind("<Button-1>", self.close_window)
        self.close_btn.bind("<Enter>", self.on_close_enter)
        self.close_btn.bind("<Leave>", self.on_close_leave)
        
        # 计时器显示标签
        self.time_label = tk.Label(
            self.main_frame, 
            text="00:00.00", 
            font=("Helvetica", 48, "normal"),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg'],
            pady=20
        )
        self.time_label.pack(expand=True)
        
        # 分隔线
        self.separator = tk.Frame(
            self.main_frame, 
            height=2, 
            bg=self.current_colors['separator']
        )
        self.separator.pack(fill=tk.X, pady=15)
        
        # 状态提示
        self.status_label = tk.Label(
            self.main_frame,
            text=self.languages[self.language_mode]['status_start'],
            font=("Helvetica", 11),
            fg=self.current_colors['status_fg'],
            bg=self.current_colors['bg'],
            pady=8
        )
        self.status_label.pack()
        
        # 重置提示
        self.reset_label = tk.Label(
            self.main_frame,
            text=self.languages[self.language_mode]['reset_hint_reset'],
            font=("Helvetica", 9),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        self.reset_label.pack()
        
        # 标题栏绑定拖动事件
        self.title_frame.bind("<ButtonPress-1>", self.on_title_press)
        self.title_frame.bind("<ButtonRelease-1>", self.on_title_release)
        self.title_frame.bind("<B1-Motion>", self.on_title_motion)
        self.title_label.bind("<ButtonPress-1>", self.on_title_press)
        self.title_label.bind("<ButtonRelease-1>", self.on_title_release)
        self.title_label.bind("<B1-Motion>", self.on_title_motion)
    
    def toggle_menu(self, event=None):
        """切换菜单显示/隐藏"""
        # 如果关于窗口存在，不显示菜单
        if self.about_window is not None:
            return
            
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        """打开菜单"""
        if self.menu_window is not None:
            return
            
        self.menu_open = True
        self.menu_window = tk.Toplevel(self.root)
        menu_win = self.menu_window
        
        # 设置菜单窗口属性
        menu_win.overrideredirect(True)
        menu_win.configure(bg=self.current_colors['bg'])
        
        # 计算菜单位置（在"更多"按钮下方）
        x = self.more_button.winfo_rootx()
        y = self.more_button.winfo_rooty() + self.more_button.winfo_height() + 2
        
        # 创建菜单框架
        menu_frame = tk.Frame(
            menu_win,
            bg=self.current_colors['bg'],
            highlightthickness=1,
            highlightbackground=self.current_colors['window_border']
        )
        menu_frame.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)
        
        # 主题菜单项
        theme_text = (self.languages[self.language_mode]['theme_menu_light'] 
                     if self.theme_mode == 1 
                     else self.languages[self.language_mode]['theme_menu_dark'])
        theme_menu = tk.Label(
            menu_frame,
            text=theme_text,
            font=("Helvetica", 9),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg'],
            padx=15,
            pady=8,
            cursor="hand2",
            anchor="w"
        )
        theme_menu.pack(fill=tk.X, padx=1, pady=1)
        theme_menu.bind("<Button-1>", self.toggle_theme_from_menu)
        theme_menu.bind("<Enter>", lambda e: theme_menu.configure(bg=self.current_colors['button_hover']))
        theme_menu.bind("<Leave>", lambda e: theme_menu.configure(bg=self.current_colors['bg']))
        
        # 语言菜单项
        language_menu = tk.Label(
            menu_frame,
            text=self.languages[self.language_mode]['language_menu'],
            font=("Helvetica", 9),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg'],
            padx=15,
            pady=8,
            cursor="hand2",
            anchor="w"
        )
        language_menu.pack(fill=tk.X, padx=1, pady=1)
        language_menu.bind("<Button-1>", self.toggle_language_from_menu)
        language_menu.bind("<Enter>", lambda e: language_menu.configure(bg=self.current_colors['button_hover']))
        language_menu.bind("<Leave>", lambda e: language_menu.configure(bg=self.current_colors['bg']))
        
        # 关于菜单项
        about_menu = tk.Label(
            menu_frame,
            text=self.languages[self.language_mode]['about_menu'],
            font=("Helvetica", 9),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg'],
            padx=15,
            pady=8,
            cursor="hand2",
            anchor="w"
        )
        about_menu.pack(fill=tk.X, padx=1, pady=(1, 2))
        about_menu.bind("<Button-1>", self.show_about_from_menu)
        about_menu.bind("<Enter>", lambda e: about_menu.configure(bg=self.current_colors['button_hover']))
        about_menu.bind("<Leave>", lambda e: about_menu.configure(bg=self.current_colors['bg']))
        
        # 设置窗口位置和大小
        menu_win.geometry(f"120x{theme_menu.winfo_reqheight() + language_menu.winfo_reqheight() + about_menu.winfo_reqheight() + 6}+{x}+{y}")
        
        # 点击其他地方关闭菜单
        menu_win.bind("<FocusOut>", self.close_menu_on_focus_out)
        menu_win.focus_set()
    
    def close_menu(self, event=None):
        """关闭菜单"""
        if self.menu_window is not None:
            try:
                self.menu_window.destroy()
            except tk.TclError:
                pass
            self.menu_window = None
        self.menu_open = False
        self.root.focus_set()
    
    def close_menu_on_focus_out(self, event=None):
        """失去焦点时关闭菜单"""
        # 延迟关闭，避免点击菜单项时立即关闭
        self.root.after(100, self.close_menu)
    
    def toggle_theme_from_menu(self, event=None):
        """从菜单切换主题"""
        self.clicked_menu_item = True
        self.close_menu()
        self.start_theme_transition()

    def toggle_language_from_menu(self, event=None):
        """从菜单切换语言"""
        self.clicked_menu_item = True
        self.close_menu()
        self.toggle_language()

    def show_about_from_menu(self, event=None):
        """从菜单显示关于窗口"""
        self.clicked_menu_item = True
        self.close_menu()
        self.show_about()
    
    def show_about(self, event=None):
        """显示关于窗口"""
        # 如果关于窗口已经存在，则将其置于最前
        if self.about_window is not None:
            try:
                self.about_window.lift()
                self.about_window.focus_force()
                return
            except tk.TclError:
                # 窗口已被销毁
                self.about_window = None
        
        # 创建关于窗口
        self.create_about_window()
    
    def create_about_window(self):
        """创建关于窗口"""
        self.about_window = tk.Toplevel(self.root)
        about_win = self.about_window
        
        # 设置窗口属性
        about_win.title(self.languages[self.language_mode]['about_title'])
        about_win.geometry("400x400")
        about_win.configure(bg=self.current_colors['bg'])
        about_win.overrideredirect(True)  # 无边框
        
        # 确保关于窗口在主窗口前面
        about_win.attributes('-topmost', True)
        
        # 居中显示
        self.center_window(about_win, 400, 400)
        
        # 创建主容器
        about_main_frame = tk.Frame(
            about_win, 
            bg=self.current_colors['bg'], 
            padx=20, 
            pady=20,
            highlightthickness=1,
            highlightbackground=self.current_colors['window_border']
        )
        about_main_frame.pack(expand=True, fill=tk.BOTH, padx=1, pady=1)
        
        # 标题栏框架
        about_title_frame = tk.Frame(about_main_frame, bg=self.current_colors['bg'])
        about_title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 标题文本
        about_title_label = tk.Label(
            about_title_frame,
            text=self.languages[self.language_mode]['about_title'],
            font=("Helvetica", 12, "bold"),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg']
        )
        about_title_label.pack(side=tk.LEFT)
        
        # 关闭按钮
        about_close_btn = tk.Label(
            about_title_frame,
            text="×",
            font=("Helvetica", 14),
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg'],
            padx=8,
            pady=0,
            cursor="hand2"
        )
        about_close_btn.pack(side=tk.RIGHT)
        about_close_btn.bind("<Button-1>", self.close_about_window)
        about_close_btn.bind("<Enter>", lambda e: about_close_btn.configure(bg="#ff4444", fg="white"))
        about_close_btn.bind("<Leave>", lambda e: about_close_btn.configure(bg=self.current_colors['bg'], fg=self.current_colors['hint_fg']))
        
        # 内容框架
        content_frame = tk.Frame(about_main_frame, bg=self.current_colors['bg'])
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        # 创建文本框和自定义滚动条
        text_frame = tk.Frame(content_frame, bg=self.current_colors['bg'])
        text_frame.pack(expand=True, fill=tk.BOTH, pady=(0, 15))
        
        # 自定义滚动条（无边框）
        scrollbar = tk.Canvas(
            text_frame,
            width=12,
            bg=self.current_colors['scrollbar_bg'],
            highlightthickness=0
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        
        # 文本框
        text_widget = tk.Text(
            text_frame,
            font=("Helvetica", 9),
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg'],
            wrap=tk.WORD,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            highlightthickness=0,
            selectbackground=self.current_colors['button_hover']
        )
        text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # 插入内容
        lang = self.languages[self.language_mode]
        content = f"{lang['version_info']}\n\n{lang['help_content']}"
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # 只读
        
        # 创建滚动条滑块
        self.scrollbar_thumb = scrollbar.create_rectangle(
            2, 0, 10, 20,
            fill=self.current_colors['scrollbar_thumb'],
            outline=""
        )
        
        # 绑定滚动事件
        def on_text_scroll(first, last):
            # 更新滑块位置
            self.update_scrollbar_thumb(scrollbar, text_widget, first, last)
        
        def on_mousewheel(event):
            # 处理鼠标滚轮事件
            text_widget.yview_scroll(int(-1*(event.delta/120)), "units")
            # 手动更新滚动条
            try:
                first, last = text_widget.yview()
                self.update_scrollbar_thumb(scrollbar, text_widget, first, last)
            except:
                pass
        
        # 配置文本框的滚动命令
        text_widget.config(yscrollcommand=on_text_scroll)
        text_widget.bind("<MouseWheel>", on_mousewheel)
        scrollbar.bind("<MouseWheel>", on_mousewheel)
        
        # 初始化滚动条位置
        try:
            first, last = text_widget.yview()
            self.update_scrollbar_thumb(scrollbar, text_widget, first, last)
        except:
            pass
        
        # 确认按钮
        confirm_btn = tk.Label(
            about_main_frame,
            text="确认" if self.language_mode == 0 else "OK",
            font=("Helvetica", 10),
            fg="white",
            bg=self.current_colors['confirm_button'],
            padx=20,
            pady=8,
            cursor="hand2"
        )
        confirm_btn.pack(pady=(0, 10))
        confirm_btn.bind("<Button-1>", self.close_about_window)
        confirm_btn.bind("<Enter>", lambda e: confirm_btn.configure(bg=self.darken_color(self.current_colors['confirm_button'])))
        confirm_btn.bind("<Leave>", lambda e: confirm_btn.configure(bg=self.current_colors['confirm_button']))
        
        # 绑定标题栏拖动事件
        about_title_frame.bind("<ButtonPress-1>", lambda e: self.on_about_title_press(e, about_win))
        about_title_frame.bind("<ButtonRelease-1>", lambda e: self.on_about_title_release(e, about_win))
        about_title_frame.bind("<B1-Motion>", lambda e: self.on_about_title_motion(e, about_win))
        about_title_label.bind("<ButtonPress-1>", lambda e: self.on_about_title_press(e, about_win))
        about_title_label.bind("<ButtonRelease-1>", lambda e: self.on_about_title_release(e, about_win))
        about_title_label.bind("<B1-Motion>", lambda e: self.on_about_title_motion(e, about_win))
        
        # 窗口关闭事件
        about_win.protocol("WM_DELETE_WINDOW", self.close_about_window)
    
    def update_scrollbar_thumb(self, scrollbar_canvas, text_widget, first, last):
        """更新滚动条滑块位置和大小"""
        try:
            # 计算滑块位置和大小
            canvas_height = scrollbar_canvas.winfo_height()
            if canvas_height <= 1:  # 防止除零错误
                return
                
            thumb_height = max(20, int(canvas_height * (float(last) - float(first))))
            thumb_y = int(float(first) * canvas_height)
            
            # 更新滑块
            scrollbar_canvas.coords(
                self.scrollbar_thumb,
                2, thumb_y, 10, thumb_y + thumb_height
            )
        except:
            pass
    
    def on_about_title_press(self, event, window):
        """关于窗口标题栏按下事件"""
        self.mouse_pressed = True
        self.press_start_x = event.x_root
        self.press_start_y = event.y_root
        self.is_dragging = False
        self.window_start_x = window.winfo_x()
        self.window_start_y = window.winfo_y()
    
    def on_about_title_motion(self, event, window):
        """关于窗口标题栏拖动事件"""
        if not self.mouse_pressed:
            return
            
        dx = abs(event.x_root - self.press_start_x)
        dy = abs(event.y_root - self.press_start_y)
        
        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True
            new_x = self.window_start_x + (event.x_root - self.press_start_x)
            new_y = self.window_start_y + (event.y_root - self.press_start_y)
            window.geometry(f"+{int(new_x)}+{int(new_y)}")
    
    def on_about_title_release(self, event, window):
        """关于窗口标题栏释放事件"""
        self.mouse_pressed = False
    
    def close_about_window(self, event=None):
        """关闭关于窗口"""
        if self.about_window is not None:
            try:
                self.about_window.destroy()
            except tk.TclError:
                pass
            self.about_window = None
            # 重新获取主窗口焦点
            self.root.focus_set()
    
    def center_window(self, window, width, height):
        """居中窗口"""
        # 获取屏幕尺寸
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def darken_color(self, hex_color, factor=0.8):
        """加深颜色"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, int(c * factor)) for c in rgb)
        return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"
    
    def toggle_theme(self, event=None):
        """切换主题"""
        self.start_theme_transition()
    
    def toggle_language(self, event=None):
        """切换语言"""
        self.language_mode = 1 - self.language_mode
        self.update_language()
    
    def update_language(self):
        """更新界面语言"""
        lang = self.languages[self.language_mode]
        
        # 更新窗口标题
        self.root.title(lang['title'])
        
        # 更新各组件文本
        self.title_label.config(text=lang['title'])
        self.minimize_btn.config(text=lang['minimize'])
        self.close_btn.config(text=lang['close'])
        self.more_button.config(text=lang['more_button'])
        
        # 更新状态和提示文本
        if not self.running and self.elapsed_time == 0:
            self.status_label.config(text=lang['status_start'])
            self.reset_label.config(text=lang['reset_hint_reset'])
        elif self.running:
            self.status_label.config(text=lang['status_running'])
            self.reset_label.config(text=lang['reset_hint_running'])
        elif not self.running and self.elapsed_time > 0:
            self.status_label.config(text=lang['status_paused'])
            self.reset_label.config(text=lang['reset_hint_paused'])
    
    def on_control_enter(self, event):
        """控制按钮悬停效果（通用）"""
        event.widget.configure(bg=self.current_colors['button_hover'])
    
    def on_control_leave(self, event):
        """控制按钮离开效果（通用）"""
        event.widget.configure(bg=self.current_colors['bg'])
    
    def on_window_press(self, event):
        """整个窗口鼠标按下事件"""
        # 如果关于窗口存在，不处理主窗口的拖动
        if self.about_window is not None:
            return
            
        self.mouse_pressed = True
        self.press_start_x = event.x_root
        self.press_start_y = event.y_root
        self.is_dragging = False
        self.clicked_menu_item = False  # 重置菜单点击标记
        
        # 保存窗口当前位置用于拖动计算
        self.window_start_x = self.root.winfo_x()
        self.window_start_y = self.root.winfo_y()
    
    def on_window_motion(self, event):
        """整个窗口鼠标拖动事件"""
        # 如果关于窗口存在，不处理主窗口的拖动
        if self.about_window is not None:
            return
            
        if not self.mouse_pressed:
            return
            
        # 计算移动距离
        dx = abs(event.x_root - self.press_start_x)
        dy = abs(event.y_root - self.press_start_y)
        
        # 如果移动超过阈值，则认为是拖动
        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True
            # 执行窗口拖动
            new_x = self.window_start_x + (event.x_root - self.press_start_x)
            new_y = self.window_start_y + (event.y_root - self.press_start_y)
            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")
    
    def on_window_release(self, event):
        """整个窗口鼠标释放事件"""
        # 如果关于窗口存在，不处理主窗口的点击
        if self.about_window is not None:
            return
            
        self.mouse_pressed = False
        
        # 如果不是在拖动，且没有点击菜单项，则控制计时器
        if not self.is_dragging and not self.clicked_menu_item:
            widget = event.widget
            # 检查是否点击在控制按钮上
            control_widgets = [self.minimize_btn, self.close_btn, self.more_button]
            
            # 如果不在控制组件上，则控制计时器
            if widget not in control_widgets:
                # 检查是否点击在标题栏上
                if not self.is_widget_in_title_bar(widget):
                    # 额外检查：确保不是点击了菜单窗口
                    if (self.menu_window is None or 
                        not self.is_widget_in_menu_window(widget)):
                        self.toggle_timer()
        
        # 重置菜单点击标记（延迟一点时间，确保所有相关事件都已处理）
        self.root.after(10, lambda: setattr(self, 'clicked_menu_item', False))
    
    def is_widget_in_menu_window(self, widget):
        """检查组件是否在菜单窗口中"""
        if self.menu_window is None:
            return False
            
        current_widget = widget
        while current_widget and current_widget != self.root:
            if current_widget == self.menu_window:
                return True
            current_widget = current_widget.master
        return False

    def is_widget_in_title_bar(self, widget):
        """检查组件是否在标题栏区域"""
        title_widgets = [self.title_frame, self.title_label, self.control_frame, 
                        self.minimize_btn, self.close_btn, self.menu_frame,
                        self.more_button]
        current_widget = widget
        while current_widget and current_widget != self.root:
            if current_widget in title_widgets:
                return True
            current_widget = current_widget.master
        return False
    
    def on_title_press(self, event):
        """标题栏按下事件"""
        # 如果关于窗口存在，不处理主窗口的拖动
        if self.about_window is not None:
            return
            
        self.mouse_pressed = True
        self.press_start_x = event.x_root
        self.press_start_y = event.y_root
        self.is_dragging = False
        self.clicked_menu_item = False  # 重置菜单点击标记
        
        # 保存窗口当前位置用于拖动计算
        self.window_start_x = self.root.winfo_x()
        self.window_start_y = self.root.winfo_y()
    
    def on_title_motion(self, event):
        """标题栏拖动事件"""
        # 如果关于窗口存在，不处理主窗口的拖动
        if self.about_window is not None:
            return
            
        if not self.mouse_pressed:
            return
            
        # 计算移动距离
        dx = abs(event.x_root - self.press_start_x)
        dy = abs(event.y_root - self.press_start_y)
        
        # 如果移动超过阈值，则认为是拖动
        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True
            # 执行窗口拖动
            new_x = self.window_start_x + (event.x_root - self.press_start_x)
            new_y = self.window_start_y + (event.y_root - self.press_start_y)
            self.root.geometry(f"+{int(new_x)}+{int(new_y)}")
    
    def on_title_release(self, event):
        """标题栏释放事件"""
        # 如果关于窗口存在，不处理主窗口的拖动
        if self.about_window is not None:
            return
            
        self.mouse_pressed = False
        # 标题栏不触发计时器控制
    
    def on_close_enter(self, event):
        """关闭按钮特殊悬停效果"""
        self.close_btn.configure(bg="#ff4444", fg="white")
    
    def on_close_leave(self, event):
        """关闭按钮特殊离开效果"""
        self.close_btn.configure(bg=self.current_colors['bg'], fg=self.current_colors['hint_fg'])
    
    def minimize_window(self, event=None):
        """最小化窗口 - 使用withdraw替代iconify"""
        # 如果关于窗口存在，不处理最小化
        if self.about_window is not None:
            return
            
        self.root.withdraw()  # 隐藏窗口
        # 创建一个临时的顶层窗口来恢复原窗口
        temp_window = tk.Toplevel()
        temp_window.withdraw()
        temp_window.after(100, lambda: self.restore_window(temp_window))
    
    def restore_window(self, temp_window):
        """恢复窗口显示"""
        temp_window.destroy()
        self.root.deiconify()
        self.root.lift()
    
    def close_window(self, event=None):
        """关闭窗口"""
        # 先关闭所有子窗口
        self.close_menu()
        self.close_about_window()
        self.root.destroy()
    
    def start_theme_transition(self, event=None):
        """开始主题渐变切换"""
        # 如果关于窗口存在，不处理主题切换
        if self.about_window is not None:
            return
            
        if self.animating:
            return
            
        self.animating = True
        target_mode = 1 - self.theme_mode  # 切换到另一个主题
        self.animate_theme_transition(target_mode)
    
    def animate_theme_transition(self, target_mode, step=0):
        """执行主题渐变动画"""
        if step > 10:  # 动画完成
            self.theme_mode = target_mode
            self.animating = False
            # 动画完成后更新主题按钮文本和恢复状态标签的颜色
            self.update_language()  # 更新语言相关文本
            self.restore_status_color()
            return
        
        # 计算渐变颜色
        start_theme = self.themes[1 - target_mode]
        end_theme = self.themes[target_mode]
        
        for key in self.current_colors:
            if key in start_theme and key in end_theme:
                start_color = self.hex_to_rgb(start_theme[key])
                end_color = self.hex_to_rgb(end_theme[key])
                
                # 线性插值计算当前步骤的颜色
                r = int(start_color[0] + (end_color[0] - start_color[0]) * step / 10)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * step / 10)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * step / 10)
                
                self.current_colors[key] = self.rgb_to_hex(r, g, b)
        
        # 应用当前颜色
        self.apply_current_colors()
        
        # 继续动画
        self.root.after(20, lambda: self.animate_theme_transition(target_mode, step + 1))
    
    def restore_status_color(self):
        """恢复状态标签的颜色（解决主题切换时颜色丢失问题）"""
        theme = self.themes[self.theme_mode]
        lang = self.languages[self.language_mode]
        if self.running:
            self.status_label.config(fg=theme['active_fg'], text=lang['status_running'])
        elif not self.running and self.elapsed_time > 0:
            self.status_label.config(fg=theme['pause_fg'], text=lang['status_paused'])
        else:
            self.status_label.config(fg=theme['status_fg'], text=lang['status_start'])
    
    def hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB元组"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r, g, b):
        """将RGB元组转换为十六进制颜色"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def apply_current_colors(self):
        """应用当前颜色到所有组件"""
        self.root.configure(bg=self.current_colors['bg'])
        self.main_frame.configure(
            bg=self.current_colors['bg'],
            highlightbackground=self.current_colors['window_border']
        )
        
        # 更新标题栏组件
        self.title_frame.configure(bg=self.current_colors['bg'])
        self.menu_frame.configure(bg=self.current_colors['bg'])
        self.control_frame.configure(bg=self.current_colors['bg'])
        self.title_label.configure(
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        
        # 更新菜单按钮颜色
        self.more_button.configure(
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        
        # 更新窗口控制按钮颜色
        self.minimize_btn.configure(
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        self.close_btn.configure(
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        
        # 更新所有其他组件
        self.time_label.configure(
            fg=self.current_colors['fg'],
            bg=self.current_colors['bg']
        )
        self.status_label.configure(
            fg=self.current_colors['status_fg'],
            bg=self.current_colors['bg']
        )
        self.reset_label.configure(
            fg=self.current_colors['hint_fg'],
            bg=self.current_colors['bg']
        )
        self.separator.configure(bg=self.current_colors['separator'])
        
        # 如果菜单窗口存在，也更新其颜色
        if self.menu_window is not None:
            try:
                self.menu_window.configure(bg=self.current_colors['bg'])
                # 更新菜单项颜色
                for child in self.menu_window.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(
                            bg=self.current_colors['bg'],
                            highlightbackground=self.current_colors['window_border']
                        )
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.configure(
                                    fg=self.current_colors['fg'],
                                    bg=self.current_colors['bg']
                                )
            except tk.TclError:
                pass
        
        # 如果关于窗口存在，也更新其颜色
        if self.about_window is not None:
            try:
                self.about_window.configure(bg=self.current_colors['bg'])
            except tk.TclError:
                pass
    
    def on_key_press(self, event):
        """处理键盘事件"""
        self.root.focus_set()
    
    def handle_enter_key(self, event=None):
        """处理Enter键 - 控制计时器开始/暂停"""
        # 如果关于窗口存在，不处理键盘事件
        if self.about_window is not None:
            return
        self.toggle_timer()
    
    def handle_space_key(self, event=None):
        """处理空格键 - 暂停时复位"""
        # 如果关于窗口存在，不处理键盘事件
        if self.about_window is not None:
            return
        if not self.running:
            self.reset_timer()
    
    def handle_escape_key(self, event=None):
        """处理ESC键 - 暂停时复位"""
        # 如果关于窗口存在，不处理键盘事件
        if self.about_window is not None:
            return
        if not self.running:
            self.reset_timer()
    
    def handle_f4_key(self, event=None):
        """处理F4键 - 紧急关闭"""
        self.close_window()
    
    def toggle_timer(self, event=None):
        lang = self.languages[self.language_mode]
        if not self.running:
            # 开始计时
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.status_label.config(
                text=lang['status_running'], 
                fg=self.themes[self.theme_mode]['active_fg']
            )
            self.reset_label.config(text=lang['reset_hint_running'])
        else:
            # 暂停计时
            self.running = False
            self.status_label.config(
                text=lang['status_paused'], 
                fg=self.themes[self.theme_mode]['pause_fg']
            )
            self.reset_label.config(text=lang['reset_hint_paused'])
    
    def reset_timer(self, event=None):
        lang = self.languages[self.language_mode]
        if not self.running:
            self.elapsed_time = 0
            self.update_display()
            self.status_label.config(
                text=lang['status_reset'], 
                fg=self.themes[self.theme_mode]['status_fg']
            )
            self.reset_label.config(text=lang['reset_hint_reset'])
    
    def update_timer(self):
        # 如果关于窗口存在，仍然可以更新计时器显示
        if self.running:
            current_time = time.time()
            if current_time - self.last_update >= 0.01:
                self.elapsed_time = current_time - self.start_time
                self.update_display()
                self.last_update = current_time
            self.root.after(10, self.update_timer)
    
    def update_display(self):
        # 计算时间
        total_seconds = self.elapsed_time
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds - int(total_seconds)) * 100)
        
        # 格式化显示
        if hours > 0:
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
        
        self.time_label.config(text=time_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ElegantTimerApp(root)
    root.mainloop()