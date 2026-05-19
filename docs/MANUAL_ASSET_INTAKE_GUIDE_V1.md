# MANUAL ASSET INTAKE GUIDE V1

Status: TRUSTED GUIDE
Scope: Manual asset intake process for FlowMind Asset Resolver v1.

## Purpose

This guide explains how to manually add real media assets so FlowMind can move from blocked planning assets to resolved usable assets.

The goal is simple:

- add real image/video files
- add license sidecar files
- run Asset Resolver
- confirm resolved_count increases
- avoid fake assets

## Current context

Asset Resolver v1 searches only approved local directories.

Approved directories:

- assets_library/
- projects/<PROJECT_ID>/manual_assets/

For the current test project, use:

- projects/P2026_TEST_001/manual_assets/

Current resolver result without manual assets:

- resolved_count = 0
- blocked_count = 9
- license_cleared_count = 0

This is expected when no approved local media exists.

## First target

For first manual intake test, do not try to resolve all assets.

Minimum target:

- add 1 real file for ASSET_001
- add 1 license sidecar for that file
- run Asset Resolver
- confirm resolved_count = 1
- confirm license_cleared_count = 1

After that works, repeat for more assets.

## Step 1: Create manual assets directory

Run:

cd ~/FlowMind_2026
mkdir -p projects/P2026_TEST_001/manual_assets

## Step 2: Choose one asset from assets.json

Open:

projects/P2026_TEST_001/assets/assets.json

Start with ASSET_001.

Look at:

- asset_id
- asset_query
- visual_intent
- asset_type
- usage_role

For ASSET_001 in the current test project, the expected visual is a simple bill or motion-text style visual.

## Step 3: Add a real media file

Put the file here:

projects/P2026_TEST_001/manual_assets/

Recommended filename:

ASSET_001_electric_bill_breakdown.png

Allowed file extensions:

- .jpg
- .jpeg
- .png
- .webp
- .mp4
- .mov
- .mkv

Best first test file type:

- .png

Reason:

- easiest to verify
- easiest to use later in render
- no video duration issues yet

## Step 4: Create license sidecar

For every media file, create a matching license sidecar.

If media file is:

ASSET_001_electric_bill_breakdown.png

then license sidecar must be:

ASSET_001_electric_bill_breakdown.png.license.json

Both files must be in the same directory.

Example path:

projects/P2026_TEST_001/manual_assets/ASSET_001_electric_bill_breakdown.png
projects/P2026_TEST_001/manual_assets/ASSET_001_electric_bill_breakdown.png.license.json

## Step 5: License sidecar content

Create:

projects/P2026_TEST_001/manual_assets/ASSET_001_electric_bill_breakdown.png.license.json

Required content:

{
  "allowed_use": "youtube_video",
  "attribution_text": null,
  "commercial_use_allowed": true,
  "created_at": "2026-05-19T00:00:00Z",
  "license_note": "User-provided media approved for this project.",
  "license_status": "cleared",
  "requires_attribution": false,
  "source_provider": "manual",
  "source_url": "local_manual_source"
}

## Step 6: What source_provider means

Allowed source_provider values in v1:

- manual
- user_created
- local_owned
- internal_library

Use manual when:

- you manually selected the file
- you accept responsibility that it is safe for this project
- you created the license sidecar as evidence

Use user_created when:

- you personally created the visual
- it is not copied from a third-party source

Use local_owned when:

- the business already owns the file
- usage rights are known

## Step 7: What not to use

Do not use:

- random Google Images downloads
- copyrighted movie clips
- copyrighted TV footage
- YouTube screenshots
- social media screenshots without rights
- watermarked stock previews
- files with unknown origin
- fake placeholder images
- dummy mp4 files

If source is unclear, do not use it.

## Step 8: Naming rules

Best naming format:

ASSET_<number>_<keywords>.<ext>

Examples:

ASSET_001_electric_bill_breakdown.png
ASSET_002_usage_rate_fixed_charges.png
ASSET_003_home_appliances_energy.mp4

Why:

Asset Resolver matches files by:

1. asset_id in filename
2. scene_id in filename
3. asset_type in filename
4. asset_query keyword overlap
5. compatible media extension

The safest match is asset_id in filename.

## Step 9: Run Asset Resolver

After adding the file and sidecar, run:

cd ~/FlowMind_2026
python engine/executors/asset_resolver.py --state projects/P2026_TEST_001/PROJECT_STATE.json

Expected success output after adding one valid ASSET_001 file:

- status = ASSET_RESOLVER_OK
- resolved_count = 1
- blocked_count = 8
- license_cleared_count = 1

## Step 10: Validate result

Run:

cd ~/FlowMind_2026
python3 -c 'import json; d=json.load(open("projects/P2026_TEST_001/assets/resolved_assets.json", encoding="utf-8")); print("provider_mode=", d["provider_mode"]); print("asset_count=", d["asset_count"]); print("resolved_count=", d["resolved_count"]); print("blocked_count=", d["blocked_count"]); print("license_cleared_count=", d["license_cleared_count"]); print([(a["asset_id"], a["provider_status"], a["license_status"], a["local_path"]) for a in d["assets"]])'

Expected result after first valid file:

- ASSET_001 provider_status = resolved
- ASSET_001 license_status = cleared
- ASSET_001 local_path is not null
- other assets may remain blocked

## Step 11: Re-run QA later

After assets are resolved, QA should eventually be re-run to update blockers.

Important:

Asset Resolver improves asset evidence.

QA decides readiness.

Do not manually change qa_report.json.

## Common failure cases

### File exists but resolver still blocks it

Likely reasons:

- filename does not include ASSET_001 or useful keywords
- file extension is not allowed
- file is outside approved directories
- license sidecar is missing
- license sidecar has invalid fields
- license_status is not cleared

### License sidecar exists but asset remains blocked

Likely reasons:

- source_provider is empty
- license_note is empty
- commercial_use_allowed is missing
- license_status is not cleared
- sidecar filename does not exactly match media filename plus .license.json

### Resolver finds file but blocks license

This means the file was detected, but license evidence was not strong enough.

Fix the sidecar, not the resolver.

## Safety rule

Never force resolved status manually.

Never edit resolved_assets.json by hand to make an asset look resolved.

The correct flow is:

manual_assets file
plus license sidecar
then Asset Resolver
then resolved_assets.json

## First manual test recommendation

Start with one simple image:

ASSET_001_electric_bill_breakdown.png

Do not add all 9 assets at once.

Reason:

- easier debugging
- less noise
- proves resolver accepts the intake format

After ASSET_001 works, add ASSET_002 and ASSET_003.

## Exit condition

Manual Asset Intake Guide v1 is complete when:

- this document exists
- manual_assets directory rule is clear
- media naming rule is clear
- license sidecar rule is clear
- first single-asset test is defined
- resolver validation command is defined
- forbidden sources are defined
- no fake assets are allowed
