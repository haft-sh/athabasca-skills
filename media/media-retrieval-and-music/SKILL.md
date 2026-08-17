---
name: media-retrieval-and-music
description: "Use when handling general media and music tasks: YouTube transcript extraction, GIF search/download, Spotify playback/playlists, audio feature visualization, open-source song generation, and songwriting or AI-music prompts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [media, music, youtube, gif, spotify, audio, songwriting]
    related_skills: [voice-cloning-workflows]
---

# Media Retrieval and Music

## Overview

This umbrella covers lightweight media retrieval, music control, audio visualization, and song-generation workflows. Route by intent: find/download media, extract transcript/content, control playback, analyze audio, generate music, or write lyrics/prompts.

## When to Use

- Search/download reaction GIFs or media snippets.
- Fetch YouTube transcripts and convert them into summaries, threads, blogs, or timestamped notes.
- Control Spotify playback, search, queue tracks, inspect devices, or manage playlists.
- Generate spectrograms/audio features such as mel, chroma, or MFCC panels.
- Use HeartMuLa-like open-source music generation from lyrics and tags.
- Write lyrics or craft Suno/AI-music prompts.

## Router

| Task | Route |
| --- | --- |
| "Find a GIF" / "download a GIF" | GIF/Tenor search |
| "Summarize this YouTube video" | Transcript extraction first, then writing task |
| "Play/pause/queue/add to playlist" | Spotify tools |
| "Show the spectrogram/features" | Audio visualization |
| "Generate a song from lyrics/tags" | Open-source music generation |
| "Write lyrics / Suno prompt" | Songwriting and AI-music prompt craft |

## YouTube Transcripts

Fetch transcript text before summarizing. Prefer JSON output when metadata/timestamps matter and plain text when feeding another writing step. If a language is requested, use a fallback chain and report when the exact language is unavailable.

## GIF Search

Use Tenor/API search when the user asks for a GIF. Return usable URLs and choose preview/smaller variants when the platform benefits from lighter media. If downloading, verify the file exists and is the expected media type.

## Spotify

For playback commands, minimize tool calls by using canonical patterns: search then play, inspect currently playing, pause/skip/volume, add to playlist. Be careful with side effects such as playlist edits: resolve the track and playlist before mutating.

## Audio Visualization

Use audio feature tools when the user wants to inspect or visualize audio. Common outputs include spectrogram, mel, chroma, MFCC, or multi-panel grids. Verify input path/URL and produce a concrete output file path.

## Music Generation

For open-source generation, check hardware and Python version requirements before starting. Separate lyric writing from generation parameters/tags. If using local models, report expected resource constraints rather than silently falling back.

## Songwriting and AI-Music Prompts

For lyrics, choose structure, rhyme/meter, emotional arc, and dynamics before prompt polish. For Suno-style prompts, separate lyrics from style/genre descriptors and avoid stuffing the lyrics field with production notes.

## Common Pitfalls

1. **Summarizing YouTube without transcript.** Always retrieve or report failure first.
2. **Mutating Spotify playlists blindly.** Resolve track and playlist IDs/names.
3. **Confusing lyrics with model tags.** Keep song text and generation style separate.
4. **Ignoring media file verification.** Check downloaded/generated files exist before reporting success.

## Verification Checklist

- [ ] Correct media route selected.
- [ ] Input URL/path/query validated.
- [ ] Side effects resolved to exact target.
- [ ] Output URL/file/transcript/playback state verified with tool output.
