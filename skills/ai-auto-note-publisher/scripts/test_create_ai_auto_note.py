import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import datetime as dt
import unittest

from create_ai_auto_note import (
    _extract_arxiv_link,
    _extract_paper_title,
    build_post,
    classify_subcategory,
    summarize_points,
)


class AutoNoteTests(unittest.TestCase):
    def test_classify_paper_reading(self):
        text = "这篇paper在arxiv上发布，包含ablation实验和baseline对比"
        self.assertEqual(classify_subcategory(text), "paper-reading")

    def test_classify_productivity(self):
        text = "今天复盘学习计划，明确todo和行动项"
        self.assertEqual(classify_subcategory(text), "productivity")

    def test_extract_paper_metadata(self):
        text = "Title: Test-Time Scaling\n链接：https://arxiv.org/abs/2501.12345"
        self.assertEqual(_extract_paper_title(text), "Test-Time Scaling")
        self.assertEqual(_extract_arxiv_link(text), "https://arxiv.org/abs/2501.12345")

    def test_extract_paper_title_with_fullwidth_colon(self):
        text = "论文标题：使用 CoT 增强推理能力"
        self.assertEqual(_extract_paper_title(text), "使用 CoT 增强推理能力")

    def test_build_post_paper_reading_contains_sections(self):
        source = """Title: Test-Time Scaling
我们讨论了method与ablation结果。
链接：https://arxiv.org/abs/2501.12345
下一步复现实验。"""
        _, post = build_post(
            title="论文测试",
            source_text=source,
            date=dt.date(2026, 3, 16),
            forced_subcategory="paper-reading",
        )
        self.assertIn("## 论文信息", post)
        self.assertIn("- 论文标题：Test-Time Scaling", post)
        self.assertIn("- 链接：https://arxiv.org/abs/2501.12345", post)
        self.assertIn("## 方法与实验要点", post)
        # metadata lines should not be duplicated as bullets in summary
        self.assertNotIn("- Title: Test-Time Scaling", post)
        self.assertNotIn("- 链接：https://arxiv.org/abs/2501.12345", post.split("## 结论速记", 1)[1])

    def test_summarize_points_keeps_explanatory_line_with_arxiv_url(self):
        source = """我们参考了 https://arxiv.org/abs/2501.12345 并总结了关键实验结论。"""
        points = summarize_points(source)
        self.assertEqual(points, ["我们参考了 https://arxiv.org/abs/2501.12345 并总结了关键实验结论。"])


    def test_build_post_includes_fallback_tags_for_sparse_input(self):
        _, post = build_post(
            title="简短记录",
            source_text="仅有一行简短内容。",
            date=dt.date(2026, 3, 16),
            forced_subcategory="paper-reading",
        )
        self.assertIn('tags: ["ai-auto-note", "paper-reading", "paper"', post)
    def test_summarize_points_skips_metadata_lines(self):
        source = """Title: A
链接：https://arxiv.org/abs/2501.12345
这是有效总结内容，长度足够。"""
        points = summarize_points(source)
        self.assertEqual(points, ["这是有效总结内容，长度足够。"])


if __name__ == "__main__":
    unittest.main()
