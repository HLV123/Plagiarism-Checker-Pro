import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import webbrowser
from typing import Dict, Optional
from checker import PlagiarismChecker
from config import *

class ModernPlagiarismGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.checker = PlagiarismChecker()
        self.current_report = None
        self.is_checking = False
        
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        self.root.title("Plagiarism Checker Pro - AI-Powered Detection")
        self.root.geometry(f"{UI_SETTINGS['WINDOW_WIDTH']}x{UI_SETTINGS['WINDOW_HEIGHT']}")
        self.root.minsize(UI_SETTINGS['MIN_WIDTH'], UI_SETTINGS['MIN_HEIGHT'])
        self.root.configure(bg=THEME_COLORS['BACKGROUND'])
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
    def create_interface(self):
        main_container = tk.Frame(self.root, bg=THEME_COLORS['BACKGROUND'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_header(main_container)
        self.create_content_area(main_container)
        self.create_footer(main_container)
        
    def create_header(self, parent):
        header_frame = tk.Frame(
            parent,
            bg=THEME_COLORS['PRIMARY'],
            relief='flat',
            bd=0,
            height=120
        )
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 Plagiarism Checker Pro DEV BY LE VAN HUNG",
            font=(FONTS['PRIMARY'][0], 24, 'bold'),
            fg='white',
            bg=THEME_COLORS['PRIMARY']
        )
        title_label.pack(expand=True)
        
        self.api_label = tk.Label(
            header_frame,
            text="API: Ready",
            font=(FONTS['PRIMARY'][0], 9),
            fg='white',
            bg=THEME_COLORS['PRIMARY']
        )
        self.api_label.place(relx=0.95, rely=0.15, anchor='ne')
        
    def create_content_area(self, parent):
        content_frame = tk.Frame(parent, bg=THEME_COLORS['BACKGROUND'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(
            content_frame,
            bg=THEME_COLORS['SURFACE'],
            relief='solid',
            bd=1
        )
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = tk.Frame(
            content_frame,
            bg=THEME_COLORS['SURFACE'],
            relief='solid',
            bd=1
        )
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_input_section(left_panel)
        self.create_results_section(right_panel)
        
    def create_input_section(self, parent):
        input_header = tk.Frame(parent, bg=THEME_COLORS['SURFACE_ALT'], height=50)
        input_header.pack(fill=tk.X)
        input_header.pack_propagate(False)
        
        tk.Label(
            input_header,
            text="📝 Text Input & Analysis",
            font=(FONTS['PRIMARY'][0], 14, 'bold'),
            fg=THEME_COLORS['TEXT_PRIMARY'],
            bg=THEME_COLORS['SURFACE_ALT']
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.word_count_label = tk.Label(
            input_header,
            text="Words: 0",
            font=(FONTS['PRIMARY'][0], 10),
            fg=THEME_COLORS['TEXT_SECONDARY'],
            bg=THEME_COLORS['SURFACE_ALT']
        )
        self.word_count_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        text_container = tk.Frame(parent, bg=THEME_COLORS['SURFACE'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.text_area = scrolledtext.ScrolledText(
            text_container,
            font=(FONTS['PRIMARY'][0], 11),
            wrap=tk.WORD,
            bg='white',
            fg=THEME_COLORS['TEXT_PRIMARY'],
            selectbackground=THEME_COLORS['PRIMARY'],
            selectforeground='white',
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=THEME_COLORS['PRIMARY']
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind('<KeyRelease>', self.update_word_count)
        
        button_frame = tk.Frame(parent, bg=THEME_COLORS['SURFACE'], height=80)
        button_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        button_frame.pack_propagate(False)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=(FONTS['PRIMARY'][0], 10),
            bg=THEME_COLORS['TEXT_SECONDARY'],
            fg='white',
            relief='flat',
            bd=0,
            command=self.clear_text,
            cursor='hand2',
            padx=15,
            pady=8
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.load_btn = tk.Button(
            button_frame,
            text="📁 Load File",
            font=(FONTS['PRIMARY'][0], 10),
            bg=THEME_COLORS['TEXT_SECONDARY'],
            fg='white',
            relief='flat',
            bd=0,
            command=self.load_file,
            cursor='hand2',
            padx=15,
            pady=8
        )
        self.load_btn.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.sample_btn = tk.Button(
            button_frame,
            text="📄 Sample",
            font=(FONTS['PRIMARY'][0], 10),
            bg=THEME_COLORS['TEXT_SECONDARY'],
            fg='white',
            relief='flat',
            bd=0,
            command=self.load_sample,
            cursor='hand2',
            padx=15,
            pady=8
        )
        self.sample_btn.pack(side=tk.LEFT, padx=(0, 20), pady=10)
        
        self.check_btn = tk.Button(
            button_frame,
            text="🔍 Analyze Text",
            font=(FONTS['PRIMARY'][0], 12, 'bold'),
            bg=THEME_COLORS['PRIMARY'],
            fg='white',
            relief='flat',
            bd=0,
            command=self.start_analysis,
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.check_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.progress_frame = tk.Frame(parent, bg=THEME_COLORS['SURFACE'])
        
        self.progress_var = tk.StringVar(value="Ready to analyze...")
        self.progress_label = tk.Label(
            self.progress_frame,
            textvariable=self.progress_var,
            font=(FONTS['PRIMARY'][0], 10),
            fg=THEME_COLORS['TEXT_SECONDARY'],
            bg=THEME_COLORS['SURFACE']
        )
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        
    def create_results_section(self, parent):
        results_header = tk.Frame(parent, bg=THEME_COLORS['SURFACE_ALT'], height=50)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)
        
        tk.Label(
            results_header,
            text="📊 Analysis Results",
            font=(FONTS['PRIMARY'][0], 14, 'bold'),
            fg=THEME_COLORS['TEXT_PRIMARY'],
            bg=THEME_COLORS['SURFACE_ALT']
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.export_btn = tk.Button(
            results_header,
            text="💾 Export",
            font=(FONTS['PRIMARY'][0], 9),
            bg=THEME_COLORS['SUCCESS'],
            fg='white',
            relief='flat',
            bd=0,
            command=self.export_report,
            cursor='hand2',
            state='disabled',
            padx=15,
            pady=5
        )
        self.export_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.results_container = tk.Frame(parent, bg=THEME_COLORS['SURFACE'])
        self.results_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.create_welcome_screen()
        
    def create_welcome_screen(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        welcome_frame = tk.Frame(self.results_container, bg=THEME_COLORS['SURFACE'])
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        icon_label = tk.Label(
            welcome_frame,
            text="🎯",
            font=(FONTS['PRIMARY'][0], 48),
            fg=THEME_COLORS['TEXT_MUTED'],
            bg=THEME_COLORS['SURFACE']
        )
        icon_label.place(relx=0.5, rely=0.4, anchor='center')
        
        welcome_text = tk.Label(
            welcome_frame,
            text="Enter text above and click 'Analyze Text'\nto start plagiarism detection",
            font=(FONTS['PRIMARY'][0], 12),
            fg=THEME_COLORS['TEXT_SECONDARY'],
            bg=THEME_COLORS['SURFACE'],
            justify='center'
        )
        welcome_text.place(relx=0.5, rely=0.55, anchor='center')
        
        features_text = tk.Label(
            welcome_frame,
            text="✓ AI-Powered Detection\n✓ Real-time Analysis\n✓ Detailed Reports\n✓ Source Identification",
            font=(FONTS['PRIMARY'][0], 10),
            fg=THEME_COLORS['TEXT_MUTED'],
            bg=THEME_COLORS['SURFACE'],
            justify='left'
        )
        features_text.place(relx=0.5, rely=0.75, anchor='center')
        
    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=THEME_COLORS['SURFACE_ALT'], height=30)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        tk.Label(
            footer_frame,
            text="Powered by Google Custom Search API • Version 2.0",
            font=(FONTS['PRIMARY'][0], 9),
            fg=THEME_COLORS['TEXT_MUTED'],
            bg=THEME_COLORS['SURFACE_ALT']
        ).pack(expand=True)
        
    def update_word_count(self, event=None):
        text = self.text_area.get(1.0, tk.END).strip()
        word_count = len(text.split()) if text else 0
        self.word_count_label.config(text=f"Words: {word_count}")
        
    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.update_word_count()
        self.create_welcome_screen()
        
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    self.update_word_count()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file:\n{str(e)}")
                
    def load_sample(self):
        sample_text = """Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention. Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.

Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data."""
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, sample_text)
        self.update_word_count()
        
    def start_analysis(self):
        text = self.text_area.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter text to analyze!")
            return
            
        if len(text.split()) < 10:
            messagebox.showwarning("Warning", "Text is too short! Please enter at least 10 words.")
            return
            
        if not self.checker.test_connection():
            messagebox.showerror("Connection Error", 
                               "Cannot connect to search API. Please check your internet connection and API configuration!")
            return
            
        if self.is_checking:
            return
            
        self.is_checking = True
        self.disable_controls()
        self.show_progress()
        
        thread = threading.Thread(target=self.analyze_text, args=(text,))
        thread.daemon = True
        thread.start()
        
    def analyze_text(self, text):
        try:
            def progress_callback(current, total, sentence):
                self.root.after(0, self.update_progress, current, total, sentence)
                
            report = self.checker.check_text(text, progress_callback)
            self.root.after(0, self.show_results, report)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            self.root.after(0, self.analysis_complete)
            
    def update_progress(self, current, total, sentence):
        percentage = (current / total) * 100
        self.progress_bar['value'] = percentage
        self.progress_var.set(f"Analyzing sentence {current}/{total}...")
        
    def show_progress(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        self.progress_frame.pack(fill=tk.X, padx=20, pady=10)
        self.progress_label.pack(pady=(10, 5))
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        progress_info = tk.Label(
            self.progress_frame,
            text="Please wait while we analyze your text...",
            font=(FONTS['PRIMARY'][0], 9),
            fg=THEME_COLORS['TEXT_MUTED'],
            bg=THEME_COLORS['SURFACE']
        )
        progress_info.pack(pady=(0, 10))
        
    def hide_progress(self):
        self.progress_frame.pack_forget()
        
    def disable_controls(self):
        self.check_btn.config(state='disabled', text="🔄 Analyzing...")
        self.clear_btn.config(state='disabled')
        self.load_btn.config(state='disabled')
        self.sample_btn.config(state='disabled')
        
    def enable_controls(self):
        self.check_btn.config(state='normal', text="🔍 Analyze Text")
        self.clear_btn.config(state='normal')
        self.load_btn.config(state='normal')
        self.sample_btn.config(state='normal')
        
    def analysis_complete(self):
        self.is_checking = False
        self.hide_progress()
        self.enable_controls()
        
    def show_results(self, report):
        self.current_report = report
        
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        notebook = ttk.Notebook(self.results_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_summary_tab(notebook, report)
        self.create_details_tab(notebook, report)
        self.create_recommendations_tab(notebook, report)
        
        self.export_btn.config(state='normal')
        
    def create_summary_tab(self, notebook, report):
        summary_frame = tk.Frame(notebook, bg=THEME_COLORS['SURFACE'])
        notebook.add(summary_frame, text="📈 Summary")
        
        canvas = tk.Canvas(summary_frame, bg=THEME_COLORS['SURFACE'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME_COLORS['SURFACE'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        summary = report['summary']
        risk_level = summary['risk_level']
        
        risk_colors = {
            'CRITICAL': THEME_COLORS['CRITICAL'],
            'HIGH': THEME_COLORS['DANGER'],
            'MEDIUM': THEME_COLORS['WARNING'],
            'LOW': THEME_COLORS['SECONDARY'],
            'SAFE': THEME_COLORS['SUCCESS']
        }
        
        risk_color = risk_colors.get(risk_level, THEME_COLORS['TEXT_SECONDARY'])
        
        risk_frame = tk.Frame(scrollable_frame, bg=risk_color, relief='flat', bd=0)
        risk_frame.pack(fill=tk.X, padx=20, pady=20)
        
        risk_icons = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '⚡',
            'LOW': '✓',
            'SAFE': '🎉'
        }
        
        risk_icon = risk_icons.get(risk_level, '❓')
        
        tk.Label(
            risk_frame,
            text=f"{risk_icon} RISK LEVEL: {risk_level}",
            font=(FONTS['PRIMARY'][0], 16, 'bold'),
            fg='white',
            bg=risk_color
        ).pack(pady=15)
        
        tk.Label(
            risk_frame,
            text=f"Overall Score: {summary['overall_score']}/100",
            font=(FONTS['PRIMARY'][0], 12),
            fg='white',
            bg=risk_color
        ).pack(pady=(0, 15))
        
        stats_grid = tk.Frame(scrollable_frame, bg=THEME_COLORS['SURFACE'])
        stats_grid.pack(fill=tk.X, padx=20, pady=10)
        
        stats_data = [
            ("📊 Plagiarism Rate", f"{summary['plagiarism_percentage']}%"),
            ("📝 Total Sentences", f"{summary['total_sentences']}"),
            ("🚩 Flagged Sentences", f"{summary['plagiarized_sentences']}"),
            ("📈 Avg Similarity", f"{summary['average_similarity']}%"),
            ("⚡ Max Similarity", f"{summary['maximum_similarity']}%"),
            ("🔍 API Requests", f"{summary['api_requests_used']}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_frame = tk.Frame(
                stats_grid,
                bg=THEME_COLORS['SURFACE_ALT'],
                relief='solid',
                bd=1
            )
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(
                stat_frame,
                text=label,
                font=(FONTS['PRIMARY'][0], 10),
                fg=THEME_COLORS['TEXT_SECONDARY'],
                bg=THEME_COLORS['SURFACE_ALT']
            ).pack(pady=(10, 5))
            
            tk.Label(
                stat_frame,
                text=value,
                font=(FONTS['PRIMARY'][0], 14, 'bold'),
                fg=THEME_COLORS['TEXT_PRIMARY'],
                bg=THEME_COLORS['SURFACE_ALT']
            ).pack(pady=(0, 10))
            
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_details_tab(self, notebook, report):
        details_frame = tk.Frame(notebook, bg=THEME_COLORS['SURFACE'])
        notebook.add(details_frame, text="🔍 Details")
        
        canvas = tk.Canvas(details_frame, bg=THEME_COLORS['SURFACE'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME_COLORS['SURFACE'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        problematic_results = [r for r in report['detailed_results'] if r['is_plagiarism']]
        
        if not problematic_results:
            tk.Label(
                scrollable_frame,
                text="🎉 No plagiarism detected!\nAll sentences appear to be original.",
                font=(FONTS['PRIMARY'][0], 14),
                fg=THEME_COLORS['SUCCESS'],
                bg=THEME_COLORS['SURFACE'],
                justify='center'
            ).pack(expand=True, pady=50)
        else:
            for i, result in enumerate(problematic_results, 1):
                self.create_detail_item(scrollable_frame, i, result)
                
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_detail_item(self, parent, index, result):
        item_frame = tk.Frame(
            parent,
            bg=THEME_COLORS['SURFACE_ALT'],
            relief='solid',
            bd=1
        )
        item_frame.pack(fill=tk.X, padx=20, pady=10)
        
        header_frame = tk.Frame(item_frame, bg=THEME_COLORS['DANGER'])
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame,
            text=f"🚩 Sentence {index} - {result['similarity']:.1%} Match",
            font=(FONTS['PRIMARY'][0], 11, 'bold'),
            fg='white',
            bg=THEME_COLORS['DANGER']
        ).pack(pady=8, padx=15)
        
        content_frame = tk.Frame(item_frame, bg=THEME_COLORS['SURFACE_ALT'])
        content_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            content_frame,
            text="Original Text:",
            font=(FONTS['PRIMARY'][0], 9, 'bold'),
            fg=THEME_COLORS['TEXT_SECONDARY'],
            bg=THEME_COLORS['SURFACE_ALT']
        ).pack(anchor='w')
        
        text_label = tk.Label(
            content_frame,
            text=result['sentence'],
            font=(FONTS['PRIMARY'][0], 10),
            fg=THEME_COLORS['TEXT_PRIMARY'],
            bg=THEME_COLORS['SURFACE_ALT'],
            wraplength=400,
            justify='left'
        )
        text_label.pack(anchor='w', pady=(5, 10))
        
        if result.get('source'):
            tk.Label(
                content_frame,
                text="Source:",
                font=(FONTS['PRIMARY'][0], 9, 'bold'),
                fg=THEME_COLORS['TEXT_SECONDARY'],
                bg=THEME_COLORS['SURFACE_ALT']
            ).pack(anchor='w')
            
            source_btn = tk.Button(
                content_frame,
                text=f"🔗 {result.get('source_domain', 'Unknown')}",
                font=(FONTS['PRIMARY'][0], 9),
                fg=THEME_COLORS['PRIMARY'],
                bg=THEME_COLORS['SURFACE_ALT'],
                relief='flat',
                bd=0,
                cursor='hand2',
                command=lambda url=result['source']: webbrowser.open(url)
            )
            source_btn.pack(anchor='w', pady=(2, 5))
            
    def create_recommendations_tab(self, notebook, report):
        rec_frame = tk.Frame(notebook, bg=THEME_COLORS['SURFACE'])
        notebook.add(rec_frame, text="💡 Recommendations")
        
        canvas = tk.Canvas(rec_frame, bg=THEME_COLORS['SURFACE'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(rec_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME_COLORS['SURFACE'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, recommendation in enumerate(report['recommendations'], 1):
            rec_item = tk.Frame(
                scrollable_frame,
                bg=THEME_COLORS['SURFACE_ALT'],
                relief='solid',
                bd=1
            )
            rec_item.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                rec_item,
                text=f"{i}. {recommendation}",
                font=(FONTS['PRIMARY'][0], 11),
                fg=THEME_COLORS['TEXT_PRIMARY'],
                bg=THEME_COLORS['SURFACE_ALT'],
                wraplength=400,
                justify='left'
            ).pack(anchor='w', padx=15, pady=10)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def export_report(self):
        if not self.current_report:
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    self.write_report_to_file(f, self.current_report)
                messagebox.showinfo("Success", "Report exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not export report:\n{str(e)}")
                
    def write_report_to_file(self, file, report):
        file.write("PLAGIARISM ANALYSIS REPORT\n")
        file.write("=" * 50 + "\n\n")
        
        summary = report['summary']
        file.write(f"Risk Level: {summary['risk_level']}\n")
        file.write(f"Overall Score: {summary['overall_score']}/100\n")
        file.write(f"Plagiarism Percentage: {summary['plagiarism_percentage']}%\n")
        file.write(f"Total Sentences: {summary['total_sentences']}\n")
        file.write(f"Flagged Sentences: {summary['plagiarized_sentences']}\n\n")
        
        file.write("RECOMMENDATIONS:\n")
        file.write("-" * 20 + "\n")
        for i, rec in enumerate(report['recommendations'], 1):
            file.write(f"{i}. {rec}\n")
        file.write("\n")
        
        problematic = [r for r in report['detailed_results'] if r['is_plagiarism']]
        if problematic:
            file.write("DETAILED FINDINGS:\n")
            file.write("-" * 20 + "\n")
            for i, result in enumerate(problematic, 1):
                file.write(f"Sentence {i} ({result['similarity']:.1%} match):\n")
                file.write(f"Text: {result['sentence']}\n")
                if result.get('source'):
                    file.write(f"Source: {result['source']}\n")
                file.write("\n")
        
        file.write(f"\nReport generated on: {report['metadata']['timestamp']}\n")
        
    def show_error(self, error_message):
        messagebox.showerror("Analysis Error", f"An error occurred during analysis:\n\n{error_message}")
        
    def run(self):
        self.root.mainloop()

def main():
    try:
        app = ModernPlagiarismGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application:\n\n{str(e)}")

if __name__ == "__main__":
    main()
