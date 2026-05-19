ASSET SOURCE STRATEGY V1

Status: TRUSTED STRATEGY
Scope: Asset sourcing strategy for FlowMind production pipeline v1.

Purpose

This document defines how FlowMind sources, stores, validates, and approves visual media assets for production use.

The goal is to move from planning-only assets to real usable media without fake progress.

Asset Source Strategy v1 prioritizes:

speed
license safety
deterministic local resolution
no fake assets
no premature API complexity
Current system state

FlowMind currently creates:

assets.json
resolved_assets.json
assembly_plan.json
qa_report.json

Asset Resolver v1 currently runs in:

provider_mode = local_existing_only

Current expected result without local media files:

resolved_count = 0
blocked_count = asset_count
license_cleared_count = 0

This is correct behavior.

Core decision

Asset Source Strategy v1 starts with manual/local sourcing.

The first production-ready media path is:

projects/<PROJECT_ID>/manual_assets/

Each media file must have a license sidecar file next to it.

This gives us the fastest safe route to first real video without building provider integrations too early.

Why manual/local first

Manual/local first is chosen because:

it avoids API rate limits
it avoids provider instability
it avoids unclear automated license handling
it allows fast human judgment on visual quality
it allows us to test render pipeline with real files
it keeps Asset Resolver deterministic
it prevents fake media generation

External providers can be added later only after manual/local mode proves the full render path.

Approved source directories

Asset Resolver v1 may search only:

assets_library/
projects/<PROJECT_ID>/manual_assets/

Meaning:

assets_library/ is reusable approved media library
projects/<PROJECT_ID>/manual_assets/ is project-specific approved media input

No other directory is approved in v1.

Required file types

Allowed media extensions in v1:

.jpg
.jpeg
.png
.webp
.mp4
.mov
.mkv

Other formats are not accepted in v1.

License sidecar rule

Every media file must have a sidecar file.

Sidecar naming format:

filename.ext.license.json

Example:

projects/P2026_TEST_001/manual_assets/ASSET_001_bill_visual.png
projects/P2026_TEST_001/manual_assets/ASSET_001_bill_visual.png.license.json

If the sidecar is missing, Asset Resolver must block the asset.

License sidecar schema

Minimum required sidecar fields:

license_status
source_provider
source_url
license_note
allowed_use
commercial_use_allowed
requires_attribution
attribution_text
created_at

Minimum valid sidecar example as field values:

license_status: cleared
source_provider: manual
source_url: local_manual_source
license_note: User-provided media approved for this project.
allowed_use: youtube_video
commercial_use_allowed: true
requires_attribution: false
attribution_text: null
created_at: 2026-05-19T00:00:00Z
License rule

License may be cleared only if the sidecar explicitly confirms:

license_status = cleared
source_provider is non-empty
license_note is non-empty
commercial_use_allowed is true
allowed_use includes YouTube, video, or commercial production context

If any of these are missing, the asset must remain blocked.

Allowed source providers in v1

Allowed source_provider values:

manual
user_created
local_owned
internal_library

External provider values are reserved for later and must not be used in v1.

Reserved future provider values:

pexels
pixabay
storyblocks
envato
artgrid
other_stock_provider
Manual source rule

For v1, the fastest allowed production path is:

source_provider = manual
source_url = local_manual_source
license_status = cleared

This is acceptable only when the user manually confirms that the file is safe to use.

The sidecar is the evidence record.

User-created source rule

If the visual was created by the user or generated internally outside the automated pipeline, use:

source_provider = user_created
source_url = local_user_created
license_status = cleared

The sidecar must still exist.

Local owned source rule

If the visual comes from media the business already owns, use:

source_provider = local_owned
source_url = local_owned_archive
license_status = cleared

The sidecar must still exist.

Naming convention

Recommended asset file naming:

ASSET_001_short_description.png
ASSET_002_short_description.mp4
SCENE_003_short_description.jpg

Best naming pattern:

ASSET_<number>_<main_keywords>.<ext>

Examples:

ASSET_001_electric_bill_breakdown.png
ASSET_002_usage_rate_fixed_charges.png
ASSET_003_home_appliances_energy.mp4

This helps deterministic matching.

Matching priority

Asset Resolver should prefer local media files matched by:

asset_id in filename
scene_id in filename
asset_type in filename
asset_query keyword overlap
compatible media extension

Best result comes from naming files with asset IDs.

No-repeat rule

For stock_first_no_repeat:

do not reuse the same local_path for multiple assets
do not reuse the same source_url for multiple assets
if no unique media file exists, block the asset
do not silently duplicate visuals

Exception may be added later for intentional repeated branding elements, but not in v1.

Quality requirements

A visual asset should be useful for the scene.

Minimum quality expectations:

visually understandable
no visible watermark
no broken or corrupt file
no irrelevant visual
no copyrighted brand focus unless legally safe
no private personal data
no low-resolution stretched image
no unreadable text if text is central to the scene
Forbidden asset sources

Forbidden in v1:

random Google Images downloads
copyrighted movie clips
copyrighted TV footage
social media screenshots without rights
watermarked stock previews
unknown-source files
AI-generated visuals without clear usage rights
fake placeholder images
dummy mp4 files
copied YouTube clips
unverified screenshots of private pages
External providers

External providers are not part of v1 implementation.

Not allowed yet:

Pexels API
Pixabay API
Storyblocks API
Envato API
Artgrid API
Cloudinary ingestion
AI image generation
AI video generation

These may be added later only after:

manual/local mode works end-to-end
render pipeline accepts resolved_assets.json
license sidecar schema is stable
QA can validate resolved assets correctly
First production video asset strategy

For the first real production video, use manual/local assets.

Process:

Generate assets.json
Read asset_query and visual_intent
Manually collect or create one visual per asset
Save files into projects/<PROJECT_ID>/manual_assets/
Create one license sidecar per file
Run Asset Resolver
Confirm resolved_count > 0
Confirm license_cleared_count > 0
Re-run QA
Continue toward render only after assets are actually resolved
Minimum first-video target

For first real video, do not require perfect visual coverage.

Minimum acceptable target:

60 percent or more required assets resolved
all used assets license cleared
no fake files
no repeated local_path
unresolved assets explicitly blocked

This target may be tightened later.

Relationship to QA

QA should continue to block upload if:

resolved_assets_path is missing
resolved_count is 0
license_cleared_count is 0
required assets are blocked
final_video_path is missing
audio_ready is false
render_ready is false

Asset Resolver improves evidence.

QA decides readiness.

Relationship to Assembly

Assembly must not use assets.json directly for final rendering once resolved_assets.json exists.

Assembly/render should use:

resolved_assets.json

not:

assets.json

Reason:

assets.json is planning intent
resolved_assets.json is evidence-backed media state
Relationship to future provider integrations

Future provider integrations should write the same resolved asset structure.

Provider-specific resolvers may be added later:

pexels_asset_provider.py
pixabay_asset_provider.py
storyblocks_asset_provider.py
cloudinary_asset_ingest.py

But all must produce the same evidence-backed fields:

provider_status
source_provider
source_url
local_path
license_status
license_note
resolution_status
blocker_reason
Fail-closed principle

If a source is unclear, block it.

If license is unclear, block it.

If the file does not exist, block it.

If the file is repeated against policy, block it.

If the file is watermarked, block it.

If metadata is missing, block it.

Do not guess.

What success looks like

Asset Source Strategy v1 succeeds when:

local manual assets can be added safely
license sidecars are easy to create
Asset Resolver can resolve files deterministically
QA receives stronger evidence
render pipeline can use real media files later
no fake progress is introduced
What this does not solve yet

This strategy does not yet solve:

automatic stock search
automatic downloads
automatic attribution generation
provider API cost control
provider rate limits
visual quality ranking
AI visual generation
Cloudinary upload
render integration

These are later phases.

Current decision

For now:

use manual/local assets
require sidecar license files
block anything uncertain
do not integrate external asset APIs yet
do not create fake media files
use resolved_assets.json as the evidence-backed asset layer
Exit condition

Asset Source Strategy v1 is complete when:

this document exists
approved source directories are defined
license sidecar schema is defined
manual/local source rule is defined
no-repeat policy is defined
forbidden sources are defined
first production video asset process is defined
future provider integrations are explicitly deferred
strategy supports Asset Resolver v1 behavior
