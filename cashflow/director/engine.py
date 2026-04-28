import json
from pathlib import Path


class DirectorEngineError(Exception):
    pass


class DirectorEngine:
    MIN_SENTENCES = 3
    DEFAULT_SHOT_DURATION = 3.0

    def __init__(self, project_dir: Path):
        self.project_dir = Path(project_dir)
        self.state_path = self.project_dir / "PROJECT_STATE.json"
        self.state = self._load_state()

        self.script_path = self._resolve_required_path("script_path")
        self.output_path = self._resolve_required_path("scene_plan_path")

    def run(self) -> Path:
        script_text = self._load_script_text()
        sentences = self._split_sentences(script_text)

        if len(sentences) < self.MIN_SENTENCES:
            raise DirectorEngineError("Script too short")

        scene_plan = self._build_scene_plan(sentences)
        shot_plan = self._build_shot_plan(sentences)

        self._validate_hook_requirements(shot_plan)

        self._save_output({
            "project_id": self.project_dir.name,
            "scene_plan": scene_plan,
            "shot_plan": shot_plan,
            "normalized_asset_queries": self._collect_queries(shot_plan),
        })

        return self.output_path

    def _load_state(self):
        if not self.state_path.exists():
            raise DirectorEngineError("PROJECT_STATE.json missing")
        return json.loads(self.state_path.read_text())

    def _resolve_required_path(self, key: str) -> Path:
        val = self.state.get(key)
        if not val:
            raise DirectorEngineError(f"Missing {key}")
        return Path(val)

    def _load_script_text(self):
        if not self.script_path.exists():
            raise DirectorEngineError("script.txt missing")
        text = self.script_path.read_text().strip()
        if not text:
            raise DirectorEngineError("Empty script")
        return text

    def _split_sentences(self, text):
        return [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

    def _build_scene_plan(self, sentences):
        return [
            {"scene_id": "scene_1", "scene_role": "hook"},
            {"scene_id": "scene_2", "scene_role": "build"},
            {"scene_id": "scene_3", "scene_role": "payoff"},
        ]

    def _build_shot_plan(self, sentences):
        shots = []
        t = 0.0

        for i, s in enumerate(sentences):
            shots.append({
                "shot_id": f"shot_{i+1}",
                "timing": {"start": t, "end": t+3, "duration": 3},
                "scene_role": self._infer_role(i),
                "visual": {
                    "asset_type": "video",
                    "query": self._build_query(s, i),
                    "style": "locked_runtime_style",
                    "motion": ["static", "zoom_in", "pan", "zoom_out"][i % 4],
                    "priority": "primary"
                },
                "text_overlay": {
                    "enabled": i < 2,
                    "content": s[:80],
                    "style": "highlight" if i < 2 else "default",
                    "position": "center" if i < 2 else "bottom"
                },
                "audio_intent": {
                    "sfx": ["transition_swoosh"] if i % 5 == 0 else [],
                    "music_energy": 7
                },
                "constraints": {
                    "no_repeat": True,
                    "style_lock": True
                }
            })
            t += 3

        return shots

    def _infer_role(self, i):
        if i < 3: return "hook"
        if i < 6: return "build"
        return "payoff"

    def _build_query(self, sentence, i):
        text = sentence.lower()

        templates = [
            ["car dashboard warning light close up", "car dashboard check engine light blinking"],
            ["car interior driver driving city traffic", "driver perspective city road driving"],
            ["person paying expensive car repair bill", "shocked person holding repair invoice"],
            ["car repair mechanic working in garage", "mechanic fixing car engine close up"],
            ["person worried about car problem close up", "stressed driver inside car"],
            ["mechanic diagnostic scanner checking car", "car diagnostic scan tool close up"],
        ]

        if "engine" in text:
            return templates[0][i % len(templates[0])]
        if "drive" in text or "road" in text:
            return templates[1][i % len(templates[1])]
        if "money" in text or "cost" in text:
            return templates[2][i % len(templates[2])]
        if "repair" in text or "mechanic" in text:
            return templates[3][i % len(templates[3])]
        if "worry" in text or "stress" in text:
            return templates[4][i % len(templates[4])]

        return templates[5][i % len(templates[5])]

    def _collect_queries(self, shots):
        return list({s["visual"]["query"] for s in shots})

    def _validate_hook_requirements(self, shots):
        if len([s for s in shots if s["scene_role"] == "hook"]) < 3:
            raise DirectorEngineError("Weak hook")

    def _save_output(self, data):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(data, indent=2))
