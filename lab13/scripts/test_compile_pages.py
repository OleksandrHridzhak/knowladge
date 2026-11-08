import os, subprocess, fitz

def check_pages(tex_path, pdf_path):
    print(f"Compiling {tex_path} ...")
    res = subprocess.run(["cmd.exe", "/c", "compile.bat"], cwd=os.path.dirname(tex_path), capture_output=True, text=True)
    if not os.path.exists(pdf_path):
        print("Compile failed:", res.stderr or res.stdout)
        return False
        
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    for i, p in enumerate(doc):
        # calculate approximate page fill
        text_rects = [b[:4] for b in p.get_text("blocks")]
        if text_rects:
            min_y = min(r[1] for r in text_rects)
            max_y = max(r[3] for r in text_rects)
            fill_pct = (max_y - min_y) / p.rect.height * 100
        else:
            fill_pct = 0
        first_word = p.get_text().strip().split()
        fw = first_word[0] if first_word else "EMPTY"
        print(f"  Page {i+1}: fill ~{fill_pct:.1f}%, starts with: [{fw}]")
    return len(doc)

if __name__ == "__main__":
    check_pages(
        r"C:\Users\userstudent\uni\knowladge\knowladge_work\week13\lab\Гріджак_Олександр_ЛР13_СЗУЗ.tex",
        r"C:\Users\userstudent\uni\knowladge\knowladge_work\week13\lab\latex_pdf\Гріджак_Олександр_ЛР13_СЗУЗ.pdf"
    )
