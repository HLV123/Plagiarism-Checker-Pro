# gui.py
"""
GUI interface cho Plagiarism Checker
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Dict
from checker import PlagiarismChecker
from config import COLORS, MAX_REQUESTS_PER_DAY

class PlagiarismGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.checker = PlagiarismChecker()
        self.setup_window()
        self.create_widgets()
        self.current_report = None
        
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Plagiarism Checker - Python Tool")
        self.root.geometry("900x700")
        self.root.configure(bg=COLORS['BACKGROUND'])
        
        # Icon và style
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Tạo các widget"""
        # Header
        header_frame = tk.Frame(self.root, bg=COLORS['PRIMARY'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🔍 PLAGIARISM CHECKER",
            font=("Arial", 20, "bold"),
            fg=COLORS['WHITE'],
            bg=COLORS['PRIMARY']
        )
        title_label.pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['BACKGROUND'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
        
        # Footer
        self.create_footer()
        
    def create_input_section(self, parent):
        """Tạo phần nhập văn bản"""
        input_frame = tk.LabelFrame(
            parent,
            text="📝 Nhập văn bản cần kiểm tra",
            font=("Arial", 12, "bold"),
            bg=COLORS['WHITE'],
            fg=COLORS['SECONDARY']
        )
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            font=("Arial", 11),
            wrap=tk.WORD,
            bg=COLORS['WHITE']
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(input_frame, bg=COLORS['WHITE'])
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Xóa",
            font=("Arial", 10),
            bg=COLORS['SECONDARY'],
            fg=COLORS['WHITE'],
            command=self.clear_text,
            relief=tk.FLAT,
            padx=20
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Sample text button
        sample_btn = tk.Button(
            button_frame,
            text="📄 Văn bản mẫu",
            font=("Arial", 10),
            bg=COLORS['SECONDARY'],
            fg=COLORS['WHITE'],
            command=self.load_sample,
            relief=tk.FLAT,
            padx=20
        )
        sample_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Check button
        self.check_btn = tk.Button(
            button_frame,
            text="🔍 Kiểm tra đạo văn",
            font=("Arial", 12, "bold"),
            bg=COLORS['PRIMARY'],
            fg=COLORS['WHITE'],
            command=self.start_check,
            relief=tk.FLAT,
            padx=30
        )
        self.check_btn.pack(side=tk.RIGHT)
        
    def create_progress_section(self, parent):
        """Tạo phần hiển thị tiến trình"""
        self.progress_frame = tk.LabelFrame(
            parent,
            text="⏳ Tiến trình kiểm tra",
            font=("Arial", 12, "bold"),
            bg=COLORS['WHITE'],
            fg=COLORS['SECONDARY']
        )
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Sẵn sàng kiểm tra...")
        self.progress_label = tk.Label(
            self.progress_frame,
            textvariable=self.progress_var,
            font=("Arial", 10),
            bg=COLORS['WHITE']
        )
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        
    def create_results_section(self, parent):
        """Tạo phần hiển thị kết quả"""
        self.results_frame = tk.LabelFrame(
            parent,
            text="📊 Kết quả kiểm tra",
            font=("Arial", 12, "bold"),
            bg=COLORS['WHITE'],
            fg=COLORS['SECONDARY']
        )
        
        # Results notebook
        self.notebook = ttk.Notebook(self.results_frame)
        
        # Summary tab
        self.summary_frame = tk.Frame(self.notebook, bg=COLORS['WHITE'])
        self.notebook.add(self.summary_frame, text="📈 Tổng quan")
        
        # Details tab
        self.details_frame = tk.Frame(self.notebook, bg=COLORS['WHITE'])
        self.notebook.add(self.details_frame, text="📋 Chi tiết")
        
        # Recommendations tab
        self.recommendations_frame = tk.Frame(self.notebook, bg=COLORS['WHITE'])
        self.notebook.add(self.recommendations_frame, text="💡 Khuyến nghị")
        
    def create_footer(self):
        """Tạo footer"""
        footer_frame = tk.Frame(self.root, bg=COLORS['SECONDARY'], height=30)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Powered by Google Custom Search API",
            font=("Arial", 9),
            fg=COLORS['WHITE'],
            bg=COLORS['SECONDARY']
        )
        footer_label.pack(expand=True)
        
    def clear_text(self):
        """Xóa văn bản"""
        self.text_area.delete(1.0, tk.END)
        
    def load_sample(self):
        """Load văn bản mẫu"""
        sample_text = """Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.

Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Python is a high-level, interpreted programming language with dynamic semantics and simple, easy-to-learn syntax."""
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, sample_text)
        
    def start_check(self):
        """Bắt đầu kiểm tra đạo văn"""
        text = self.text_area.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần kiểm tra!")
            return
            
        # Test API connection
        if not self.checker.test_connection():
            messagebox.showerror("Lỗi", "Không thể kết nối API. Kiểm tra lại cấu hình!")
            return
        
        # Disable button và show progress
        self.check_btn.config(state=tk.DISABLED)
        self.show_progress()
        
        # Start checking in separate thread
        thread = threading.Thread(target=self.check_plagiarism, args=(text,))
        thread.daemon = True
        thread.start()
        
    def check_plagiarism(self, text):
        """Kiểm tra đạo văn (chạy trong thread riêng)"""
        try:
            def progress_callback(current, total, sentence):
                self.root.after(0, self.update_progress, current, total, sentence)
            
            report = self.checker.check_text(text, progress_callback)
            self.root.after(0, self.show_results, report)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.root.after(0, self.hide_progress)
            
    def update_progress(self, current, total, sentence):
        """Cập nhật tiến trình"""
        percentage = (current / total) * 100
        self.progress_bar['value'] = percentage
        self.progress_var.set(f"Đang kiểm tra câu {current}/{total}: {sentence[:50]}...")
        
    def show_progress(self):
        """Hiển thị progress bar"""
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        self.progress_label.pack(pady=5)
        self.progress_bar.pack(pady=5)
        
    def hide_progress(self):
        """Ẩn progress bar"""
        self.progress_frame.pack_forget()
        self.check_btn.config(state=tk.NORMAL)
        
    def show_results(self, report):
        """Hiển thị kết quả"""
        self.current_report = report
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear previous results
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()
            
        # Show summary
        self.show_summary(report['summary'])
        
        # Show details
        self.show_details(report['detailed_results'])
        
        # Show recommendations
        self.show_recommendations(report['recommendations'])
        
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def show_summary(self, summary):
        """Hiển thị tổng quan"""
        # Risk level với màu sắc
        risk_color = COLORS[summary['risk_level']]
        
        # Main stats
        stats_frame = tk.Frame(self.summary_frame, bg=COLORS['WHITE'])
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Risk level indicator
        risk_frame = tk.Frame(stats_frame, bg=risk_color, relief=tk.RAISED, bd=2)
        risk_frame.pack(fill=tk.X, pady=(0, 15))
        
        risk_label = tk.Label(
            risk_frame,
            text=f"🎯 MỨC ĐỘ RỦI RO: {summary['risk_level']}",
            font=("Arial", 14, "bold"),
            fg=COLORS['WHITE'],
            bg=risk_color
        )
        risk_label.pack(pady=10)
        
        # Statistics
        stats_text = f"""
📊 THỐNG KÊ CHI TIẾT:

• Tổng số câu kiểm tra: {summary['total_sentences']}
• Câu có dấu hiệu đạo văn: {summary['plagiarized_sentences']}
• Tỷ lệ đạo văn: {summary['plagiarism_percentage']}%
• Độ tương đồng trung bình: {summary['average_similarity']}%
• API requests sử dụng: {summary['requests_used']}/{MAX_REQUESTS_PER_DAY}
        """
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=("Arial", 11),
            bg=COLORS['WHITE'],
            justify=tk.LEFT
        )
        stats_label.pack(anchor=tk.W)
        
    def show_details(self, results):
        """Hiển thị chi tiết"""
        # Scrollable frame for details
        canvas = tk.Canvas(self.details_frame, bg=COLORS['WHITE'])
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['WHITE'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Show problematic sentences
        problematic = [r for r in results if r['is_plagiarism']]
        
        if problematic:
            for i, result in enumerate(problematic, 1):
                self.create_detail_item(scrollable_frame, i, result)
        else:
            no_issues_label = tk.Label(
                scrollable_frame,
                text="✅ Không phát hiện câu nào có vấn đề!",
                font=("Arial", 12),
                bg=COLORS['WHITE'],
                fg=COLORS['LOW']
            )
            no_issues_label.pack(pady=50)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_detail_item(self, parent, index, result):
        """Tạo item chi tiết cho một câu"""
        # Main frame for this result
        item_frame = tk.LabelFrame(
            parent,
            text=f"Câu {index}",
            font=("Arial", 10, "bold"),
            bg=COLORS['WHITE'],
            fg=COLORS['SECONDARY']
        )
        item_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Sentence text
        sentence_label = tk.Label(
            item_frame,
            text=f"📝 {result['sentence']}",
            font=("Arial", 10),
            bg=COLORS['WHITE'],
            wraplength=700,
            justify=tk.LEFT
        )
        sentence_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Similarity info
        similarity_text = f"📊 Độ tương đồng: {result['similarity']:.1%} ({result['confidence']})"
        similarity_label = tk.Label(
            item_frame,
            text=similarity_text,
            font=("Arial", 9),
            bg=COLORS['WHITE'],
            fg=COLORS['MEDIUM']
        )
        similarity_label.pack(anchor=tk.W, padx=10)
        
        # Source info
        if result['source']:
            source_label = tk.Label(
                item_frame,
                text=f"🔗 Nguồn: {result['source']}",
                font=("Arial", 9),
                bg=COLORS['WHITE'],
                fg=COLORS['PRIMARY'],
                cursor="hand2"
            )
            source_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
    def show_recommendations(self, recommendations):
        """Hiển thị khuyến nghị"""
        rec_text = "\n".join([f"• {rec}" for rec in recommendations])
        
        rec_label = tk.Label(
            self.recommendations_frame,
            text=rec_text,
            font=("Arial", 11),
            bg=COLORS['WHITE'],
            justify=tk.LEFT,
            wraplength=700
        )
        rec_label.pack(anchor=tk.W, padx=20, pady=20)
        
    def show_error(self, error_msg):
        """Hiển thị lỗi"""
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {error_msg}")
        
    def run(self):
        """Chạy GUI"""
        self.root.mainloop()

def main():
    app = PlagiarismGUI()
    app.run()

if __name__ == "__main__":
    main()