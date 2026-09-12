import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from gsuid_core.models import Event
from gsuid_core.plugins.ChisaEating.ChisaEating import chisaeating_api
from gsuid_core.plugins.ChisaEating.ChisaEating.chisaeating_config import CHISA_CONFIG
from gsuid_core.plugins.ChisaEating.ChisaEating.chisaeating_main import _is_admin


class SkinApiAndAdminTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

    def test_is_admin(self) -> None:
        # 1. user_pm <= 3 is admin
        ev_admin = Event(user_pm=3, user_id="10001")
        self.assertTrue(_is_admin(ev_admin))

        # 2. user_pm > 3 but in admin_users
        ev_mod = Event(user_pm=6, user_id="88888")
        CHISA_CONFIG.set_config("admin_users", ["88888", "99999"])
        self.assertTrue(_is_admin(ev_mod))

        # 3. normal user
        ev_user = Event(user_pm=6, user_id="12345")
        self.assertFalse(_is_admin(ev_user))

    async def test_skin_get_payload_compatibility(self) -> None:
        # Invalid skin_id
        req_bad = AsyncMock()
        req_bad.json.return_value = {"id": "invalid/id.."}
        resp = await chisaeating_api.page_skin_get(req_bad)
        self.assertEqual(resp.status_code, 400)

        # Valid skin_id using 'id'
        req_id = AsyncMock()
        req_id.json.return_value = {"id": "test_skin_a"}
        with patch.object(
            chisaeating_api, "_get_or_fetch_skin_config", return_value=({"id": "test_skin_a"}, None)
        ) as mock_fetch:
            resp = await chisaeating_api.page_skin_get(req_id)
            self.assertEqual(resp.status_code, 200)
            mock_fetch.assert_called_once()
            args, _ = mock_fetch.call_args
            self.assertEqual(args[0], "test_skin_a")

        # Valid skin_id using 'skin_id'
        req_skin_id = AsyncMock()
        req_skin_id.json.return_value = {"skin_id": "test_skin_b"}
        with patch.object(
            chisaeating_api, "_get_or_fetch_skin_config", return_value=({"id": "test_skin_b"}, None)
        ) as mock_fetch:
            resp = await chisaeating_api.page_skin_get(req_skin_id)
            self.assertEqual(resp.status_code, 200)
            mock_fetch.assert_called_once()
            args, _ = mock_fetch.call_args
            self.assertEqual(args[0], "test_skin_b")

    async def test_skin_delete_compatibility_and_response(self) -> None:
        skins_root = Path(self.temp_dir) / "skins"
        with patch.object(chisaeating_api, "_skins_dir", return_value=skins_root):
            # Missing ID
            req_empty = AsyncMock()
            req_empty.json.return_value = {}
            resp = await chisaeating_api.page_skin_delete(req_empty)
            self.assertEqual(resp.status_code, 400)

            # Create mock skin config file
            official_dir = chisaeating_api._skin_store_dir(chisaeating_api.OFFICIAL_SKIN_SOURCE) / "skin"
            official_dir.mkdir(parents=True, exist_ok=True)
            test_file = official_dir / "del_skin.json"
            test_file.write_text(json.dumps({"id": "del_skin", "name": "To Delete"}), encoding="utf-8")
            self.assertTrue(test_file.exists())

            # Delete using 'id'
            req_del = AsyncMock()
            req_del.json.return_value = {"id": "del_skin"}
            resp = await chisaeating_api.page_skin_delete(req_del)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.body.decode())
            self.assertTrue(data.get("deleted"))
            self.assertEqual(data.get("id"), "del_skin")
            self.assertFalse(test_file.exists())

    async def test_skin_local_scans_root_skins(self) -> None:
        skins_root = Path(self.temp_dir) / "skins"
        skins_root.mkdir(parents=True, exist_ok=True)
        # Put custom skin directly in skins_root
        custom_skin = skins_root / "my_custom_skin.json"
        custom_skin.write_text(json.dumps({"id": "my_custom", "name": "My Custom Skin"}), encoding="utf-8")

        with patch.object(chisaeating_api, "_skins_dir", return_value=skins_root):
            resp = await chisaeating_api.page_skin_local()
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.body.decode())
            skins = data.get("data", [])
            found = [s for s in skins if s.get("id") == "my_custom"]
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].get("name"), "My Custom Skin")


if __name__ == "__main__":
    unittest.main()
