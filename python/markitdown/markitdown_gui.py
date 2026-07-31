import threading
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, END, RIGHT, Y, LEFT, BOTH
from markitdown import MarkItDown

md = MarkItDown()

DEFAULT_INPUT_FOLDER = Path(r"C:\Course")
DEFAULT_OUTPUT_FOLDER = Path(r"C:\Users\willow\Documents\Mnemosyne\markdownkit")


class MarkitdownGUI:
    def __init__(self, master):
        self.master = master
        master.title("Markitdown GUI - PPTX 转 Markdown")

        self.selected_file = None
        self.selected_folder = DEFAULT_INPUT_FOLDER
        self.output_folder = DEFAULT_OUTPUT_FOLDER
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.label_info = Label(
            master,
            text=(
                f"默认 PPT 文件夹：{DEFAULT_INPUT_FOLDER}\n"
                f"默认输出文件夹：{DEFAULT_OUTPUT_FOLDER}"
            ),
            justify="left"
        )
        self.label_info.pack(pady=5)

        self.label_file = Label(master, text="（可选）选择单个文件，只转这一个：")
        self.label_file.pack()
        self.btn_select_file = Button(master, text="选择单个文件", command=self.select_file)
        self.btn_select_file.pack()

        self.label_folder = Label(master, text="（可选）重新选择 PPT 文件夹：")
        self.label_folder.pack()
        self.btn_select_folder = Button(master, text="重新选择 PPT 文件夹", command=self.select_folder)
        self.btn_select_folder.pack()

        self.label_output = Label(master, text="（可选）重新选择输出目录：")
        self.label_output.pack()
        self.btn_output_folder = Button(master, text="重新选择输出目录", command=self.select_output_folder)
        self.btn_output_folder.pack()

        self.btn_convert = Button(master, text="开始转换", command=self.start_convert_thread)
        self.btn_convert.pack(pady=10)

        self.log_text = Text(master, height=15, wrap="word")
        self.log_scroll = Scrollbar(master, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scroll.set)
        self.log_scroll.pack(side=RIGHT, fill=Y)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)

        self.log(f"已加载默认 PPT 文件夹：{self.selected_folder}")
        self.log(f"已加载默认输出文件夹：{self.output_folder}")

    def log(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        self.master.update()

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("PPTX 文件", "*.pptx"), ("PDF 文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.selected_file = Path(file_path)
            self.log(f"已选择单个文件：{self.selected_file}")
        else:
            self.log("未选择文件。")

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择 PPT 文件夹")
        if folder_path:
            self.selected_folder = Path(folder_path)
            self.selected_file = None
            self.log(f"已重新选择 PPT 文件夹：{self.selected_folder}")
        else:
            self.log("未选择文件夹。")

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="选择输出目录")
        if folder_path:
            self.output_folder = Path(folder_path)
            self.output_folder.mkdir(parents=True, exist_ok=True)
            self.log(f"已重新选择输出目录：{self.output_folder}")
        else:
            self.log("未选择输出目录。")

    def start_convert_thread(self):
        thread = threading.Thread(target=self.convert)
        thread.daemon = True
        thread.start()

    def convert(self):
        if not self.output_folder:
            self.log("请先设置输出目录！")
            return

        if self.selected_file:
            self.convert_single_file(self.selected_file)
            return

        if self.selected_folder:
            pptx_files = list(self.selected_folder.glob("*.pptx"))
            if not pptx_files:
                self.log(f"在 {self.selected_folder} 中没有找到 .pptx 文件。")
                return

            self.log(f"开始批量转换，找到 {len(pptx_files)} 个 .pptx 文件...")
            for pptx in pptx_files:
                self.convert_single_file(pptx)
            self.log("批量转换完成。")
            return

        self.log("没有可转换的文件或文件夹。")

    def convert_single_file(self, file_path: Path):
        try:
            self.log(f"正在转换：{file_path.name}")
            result = md.convert(file_path)

            out_name = file_path.stem + ".md"
            out_path = self.output_folder / out_name

            out_path.write_text(result.text_content, encoding="utf-8")
            self.log(f"转换完成：{out_path}")
        except Exception as e:
            self.log(f"转换失败：{file_path.name}，错误：{e}")


if __name__ == "__main__":
    root = Tk()
    gui = MarkitdownGUI(root)
    root.mainloop()