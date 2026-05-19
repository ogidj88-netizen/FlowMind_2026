VISUAL_PACING_LAYER_CONTRACT_V1

Status: TRUSTED CONTRACT
Version: 1.0.0
Layer: Visual Pacing Layer
Renderer target: FFmpeg only

1. Purpose

Visual Pacing Layer v1 fixes the first confirmed quality failure in P2026_TEST_001.

The current system works technically:

script exists
scenes exist
assets exist
audio exists
final video exists
QA sees only upload_readiness as blocker

But the video is not publishable because it feels like a narrated slideshow.

This layer must improve visual pacing without changing script, audio, final video approval, or upload state.

2. Confirmed problem

Current failure pattern:

1 logical scene = 1 long static visual asset

Observed result:

slow visual rhythm
weak retention
too much text on screen
unclear scene-to-voiceover sync
no visual impulse every 3-6 seconds

This is a quality failure, not a runtime failure.

3. Scope

Visual Pacing Layer v1 creates one artifact:

projects/<PROJECT_ID>/visual_pacing/visual_pacing_plan.json

The artifact splits each long scene into short visual beats.

Each beat must define:

beat_id
scene_id
asset_id
audio_segment_id
order
beat_order
scene_start_sec
scene_end_sec
global_start_sec
global_end_sec
beat_duration_sec
source_visual_path
source_audio_path
visual_action
motion_profile
text_mode
display_text
render_instruction
4. Non-goals

This layer must not:

upload video
set qa_passed=true
set approved_for_upload=true
rewrite script
regenerate audio
modify audio_render.json
modify final_video.mp4
call AI providers
call stock providers
call YouTube API
create fake media
create placeholder assets
add Remotion
5. Inputs

Required inputs:

PROJECT_STATE.json
assembly_plan.json
resolved_assets.json
audio_render.json
scenes.json
final_render_report.json

Authoritative timing source:
audio_render.segments[].duration_sec

Authoritative visual source:
resolved_assets.assets[].local_path

Authoritative scene order:
assembly_plan.timeline[].order

Audio Master Clock remains the source of truth.

6. Preconditions

The layer may run only when:

PROJECT_STATE.phase = QA
assembly_plan.assets_ready = true
assembly_plan.audio_ready = true
assembly_plan.render_ready = true
audio_render.audio_status = ready
audio_render.audio_ready = true
audio_render.duration_validated = true
audio_render.loudness_validated = true
final_render_report.verdict = PASS
final_video_path exists

If any precondition fails, the tool must fail closed.

7. Split rule

Default beat split:

If audio_duration_sec <= 7:
beat_count = 1

If audio_duration_sec > 7:
beat_count = ceil(audio_duration_sec / 5)

Beat duration limits:

minimum: 3.0 sec
target: 5.0 sec
maximum: 6.5 sec

If final beat is shorter than 3 seconds, merge it into the previous beat.

Total beat duration per scene must match audio segment duration within 0.05 sec.

8. Allowed visual actions

Allowed visual_action values:

slow_zoom_in
slow_zoom_out
pan_left
pan_right
crop_focus_left
crop_focus_right
crop_focus_center
text_focus
chart_focus
checklist_focus
hold_safe

Allowed motion_profile values:

none
ken_burns_subtle
micro_pan
micro_zoom
static_safe

No random effects in v1.
No aggressive transitions in v1.
No glitch effects in v1.

9. Text rules

The current video has too much text on screen.

Rule:
one beat = one focus message

Allowed text_mode values:

none
single_focus_line
short_label
number_emphasis
checklist_item_focus

Forbidden:

paragraphs on screen
full script on screen
tiny unreadable text
text outside safe margins
more than 12 words in display_text

Safe margin:
all text must stay inside 10 percent screen margin.

10. State update rule

This layer may update PROJECT_STATE only by adding:

visual_pacing_plan_path

It must not modify:

phase
qa_passed
approved_for_upload
final_video_path
final_render_report_path
audio_render_path
11. QA rule

After this layer runs, QA must still remain blocked by upload_readiness.

Expected state:

qa_passed = false
approved_for_upload = false
upload_readiness = blocked

This is correct.

12. Exit condition

Visual Pacing Layer v1 is complete only when:

this contract exists
visual_pacing_plan.json exists
beat_count is greater than scene_count
total beat duration matches audio duration
preflight passes
git commit exists
final renderer has not yet been modified
13. Current decision

Do not upload.
Do not rewrite script.
Do not add external providers.
Do not add Remotion.
Do not regenerate assets.

Build deterministic visual_pacing_plan.json first.
