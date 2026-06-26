import time


class RateLimiter:
    def __init__(self):
        self.user_records: dict = {}
        self.repeat_cooldowns: dict = {}

    def is_spaming(self, uid: str, threshold: int) -> bool:
        now = time.time()
        timestamps = self.user_records.setdefault(uid, [])
        timestamps[:] = [ts for ts in timestamps if now - ts < 60]
        if len(timestamps) >= threshold:
            return True
        timestamps.append(now)
        return False

    def is_repeat_in_cooldown(self, group_id: str, cooldown_seconds: int) -> bool:
        now = time.time()
        last_time = self.repeat_cooldowns.get(group_id, 0.0)
        return now - last_time < cooldown_seconds

    def record_repeat_trigger(self, group_id: str):
        self.repeat_cooldowns[group_id] = time.time()
