FlowMind ASSETS Engine Output v1 (Canonical)

All outputs must be written into PROJECT_STATE["artifacts"]

Required structure:

artifacts:
  voice_path: path to main narration audio
  music_path: path to background music
  assets_map:
    - shot_id
    - asset_type
    - asset_path
  timeline:
    - shot_id
    - start
    - end

Rules:
- No new top-level fields in PROJECT_STATE
- No duplication outside artifacts
- All paths must be project-scoped
- No placeholders or fake assets
- Fail-closed if any asset missing

PASS:
- voice exists
- all shots mapped
- no duplicates
- timeline consistent with shot_plan

FAIL:
- missing audio
- missing asset
- repeat asset
- timeline mismatch
