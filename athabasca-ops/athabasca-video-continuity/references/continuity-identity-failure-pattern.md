# Continuity + identity failure pattern

## Symptom
A follow-on dialogue/helper clip fails to match the preceding shot, or a recurring character drifts despite being named in prompt text.

## Root cause to test first
The actual attachment payload lacks either the preceding frame or the character’s canonical identity sheet. Packet prose may describe both while the submitted reference array omits one.

## Corrective design
Use the preceding stable frame as reference #1, followed by featured-character identity, other-character identity, and environment/geography. Remove generic blocking art if reference budget is exhausted.

## Dialogue warning
Adjacent identical lines attributed to different speakers (especially an object/echo after an off-screen character) often collapse into the on-screen character’s voice. Remove the echo from a serious helper or isolate it as a silent-character insert.
