import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from TextProcessor import TextProcessor
from analyzer import ContextSentimentAnalyzer

class AnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise Text Mining & Sentiment Analytics Tool")
        self.root.geometry("800x650")
        self.root.minimum_size = (750, 550)
        self.root.configure(bg="#f4f6f9")
        
        self.processor = TextProcessor()
        self.analyzer = ContextSentimentAnalyzer()
        
        self.setup_ui_styles()
        self.create_layout_widgets()

    def setup_ui_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10), background="#f4f6f9")
        style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background="#f4f6f9", foreground="#2c3e50")
        style.configure("Sub.TLabel", font=("Segoe UI", 11, "bold"), background="#ffffff", foreground="#2c3e50")
        style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#2980b9", padding=6)
        style.map("Action.TButton", background=[('active', '#1f618d')])
        style.configure("TNotebook", background="#f4f6f9", padding=2)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[15, 4])
        
        # Table (Treeview) Styling
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#eaeded", foreground="#2c3e50")

    def create_layout_widgets(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Context-Aware Text Mining System", style="Header.TLabel").pack(anchor="w", pady=(0, 15))
        
        ttk.Label(container, text="Input Unstructured Review Text:").pack(anchor="w", pady=(0, 5))
        self.text_input = tk.Text(container, height=5, font=("Segoe UI", 10), wrap="word", relief="solid", bd=1)
        self.text_input.pack(fill="x", pady=(0, 15))
        
        self.process_btn = ttk.Button(container, text="Run Analytics Pipeline", style="Action.TButton", command=self.execute_pipeline)
        self.process_btn.pack(anchor="center", pady=(0, 15))

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.tab_sentiment = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.tab_sentiment, text=" Sentiment Analytics Matrix ")
        self.build_sentiment_tab_layout()

        self.tab_ngrams = ttk.Frame(self.notebook, style="TNotebook")
        self.notebook.add(self.tab_ngrams, text=" Key Phrases & Context Mining ")
        self.build_ngram_tab_layout()

    def build_sentiment_tab_layout(self):
        card = tk.Frame(self.tab_sentiment, bg="#ffffff", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_class = ttk.Label(card, text="Overall Evaluation: No Input Data", font=("Segoe UI", 13, "bold"), background="#ffffff")
        self.lbl_class.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.lbl_compound = ttk.Label(card, text="Compound Normalized Score: 0.0000", background="#ffffff")
        self.lbl_compound.pack(anchor="w", padx=20, pady=5)
        
        metrics_frame = tk.Frame(card, bg="#ffffff")
        metrics_frame.pack(fill="x", padx=20, pady=15)
        
        self.lbl_pos = ttk.Label(metrics_frame, text="Positivity Ratio: 0.0", background="#ffffff")
        self.lbl_pos.grid(row=0, column=0, sticky="w", padx=(0, 30))
        
        self.lbl_neu = ttk.Label(metrics_frame, text="Neutrality Ratio: 0.0", background="#ffffff")
        self.lbl_neu.grid(row=0, column=1, sticky="w", padx=(0, 30))
        
        self.lbl_neg = ttk.Label(metrics_frame, text="Negativity Ratio: 0.0", background="#ffffff")
        self.lbl_neg.grid(row=0, column=2, sticky="w")

    def build_ngram_tab_layout(self):
        card = tk.Frame(self.tab_ngrams, bg="#ffffff", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(card, text="Extracted Structural Expressions (Key Bi-grams):", style="Sub.TLabel").pack(anchor="w", padx=20, pady=(15, 10))
        
        # --- NEW STEP: SLEEK DATA TABLE LAYOUT ---
        table_frame = ttk.Frame(card)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.tree = ttk.Treeview(table_frame, columns=("Phrase", "Count"), show="headings", selectmode="browse")
        self.tree.heading("Phrase", text="EXTRACTED CONTEXT PHRASE", anchor="w")
        self.tree.heading("Count", text="FREQUENCY COUNT", anchor="center")
        
        self.tree.column("Phrase", width=450, minwidth=300, stretch=True, anchor="w")
        self.tree.column("Count", width=150, minwidth=100, stretch=False, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def execute_pipeline(self):
        raw_input = self.text_input.get("1.0", tk.END).strip()
        if not raw_input:
            messagebox.showwarning("Empty Text Buffer", "Pipeline execution canceled. Please enter text to analyze.")
            return

        # Sentiment Engine Execution
        sentiment_data = self.analyzer.analyze_review(raw_input)
        color_themes = {"Positive": "#27ae60", "Negative": "#c0392b", "Mixed / Neutral": "#d35400"}
        selected_color = color_themes.get(sentiment_data["sentiment"], "#2c3e50")
        
        self.lbl_class.config(text=f"Overall Evaluation: {sentiment_data['sentiment']}", foreground=selected_color)
        self.lbl_compound.config(text=f"Compound Normalized Score: {sentiment_data['score']} (Range: -1.0 to 1.0)")
        self.lbl_pos.config(text=f"Positivity Ratio: {sentiment_data['pos']}")
        self.lbl_neu.config(text=f"Neutrality Ratio: {sentiment_data['neu']}")
        self.lbl_neg.config(text=f"Negativity Ratio: {sentiment_data['neg']}")

        # Clear the old table data entries
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Advanced Filtered Text Miner Feature Extraction
        extracted_bigrams = self.processor.extract_features(raw_input, n=2)
        top_phrases = Counter(extracted_bigrams).most_common(10)

        # Populate the table view
        if top_phrases:
            for phrase, frequency in top_phrases:
                self.tree.insert("", tk.END, values=(phrase.title(), f"{frequency} usage(s)"))
        else:
            self.tree.insert("", tk.END, values=("No critical Noun/Adjective expressions found.", "-"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyticsApp(root)
    root.mainloop()