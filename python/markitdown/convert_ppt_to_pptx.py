from pathlib import Path
import win32com.client

INPUT_FOLDER = Path(r"C:\Course")

def convert_ppt_to_pptx(folder: Path):
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1

    ppt_files = list(folder.glob("*.ppt"))
    if not ppt_files:
        print("没有找到 .ppt 文件。")
        return

    for ppt_path in ppt_files:
        print(f"正在转换：{ppt_path.name}")
        pptx_path = ppt_path.with_suffix(".pptx")

        presentation = powerpoint.Presentations.Open(str(ppt_path), WithWindow=False)
        presentation.SaveAs(str(pptx_path), 24)
        presentation.Close()

        ppt_path.unlink()  # 删除原始 .ppt 文件
        print(f"转换完成，已删除原文件：{ppt_path.name} → {pptx_path.name}")

    powerpoint.Quit()
    print("全部完成。")


if __name__ == "__main__":
    convert_ppt_to_pptx(INPUT_FOLDER)