import ast
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'ChisaEating'


class HelpAndConfigSourceTests(unittest.TestCase):
    def test_appearance_config_and_help_renderer_exist(self) -> None:
        config_source = (PKG / 'chisaeating_config' / 'config_default.py').read_text(encoding='utf-8')
        init_source = (PKG / 'chisaeating_config' / '__init__.py').read_text(encoding='utf-8')
        help_source = (PKG / 'chisaeating_help' / '__init__.py').read_text(encoding='utf-8')

        for key in (
            'ChisaHelpBannerBgUpload',
            'ChisaHelpBgUpload',
            'ChisaHelpIconUpload',
            'ChisaHelpColumn',
        ):
            self.assertIn(key, config_source)
            self.assertIn(key, help_source)

        self.assertIn('APPEARANCE_CONFIG_DEFAULT', config_source)
        self.assertIn('CHISA_APPEARANCE_CONFIG = StringConfig(', init_source)
        self.assertIn('千小妹外观配置', init_source)
        self.assertIn('get_new_help', help_source)
        self.assertIn('register_help("ChisaEating", "千小妹还在吃帮助"', help_source)
        self.assertIn('MessageSegment.image', help_source)

    def test_config_dividers_make_main_config_grouped(self) -> None:
        source = (PKG / 'chisaeating_config' / 'config_default.py').read_text(encoding='utf-8')
        for divider in (
            '使用范围',
            '默认世界',
            '世界 1：鸣潮',
            '世界 2：原神',
            '自定义世界',
            '触发词',
            '食物文字池',
            '概率与限流',
            '推荐模式',
            '文案模板',
        ):
            self.assertIn(divider, source)

    def test_help_assets_and_circle_icon_exist(self) -> None:
        help_json = PKG / 'chisaeating_help' / 'help.json'
        icon_path = PKG / 'chisaeating_help' / 'icon_path'
        self.assertTrue(help_json.is_file())
        expected_icons = {
            '随机干饭.png',
            '随机饮品.png',
            '黑暗料理.png',
            '现实食物.png',
            '现实饮品.png',
            '异界特产.png',
            '自定义干饭人.png',
        }
        self.assertTrue(expected_icons.issubset({p.name for p in icon_path.glob('*.png')}))

        with Image.open(ROOT / 'ICON.png') as icon:
            self.assertEqual(icon.mode, 'RGBA')
            self.assertEqual(icon.size[0], icon.size[1])
            self.assertEqual(icon.getpixel((0, 0))[3], 0)
            center = icon.size[0] // 2
            self.assertEqual(icon.getpixel((center, center))[3], 255)


if __name__ == '__main__':
    unittest.main()
