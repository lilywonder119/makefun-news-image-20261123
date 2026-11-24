# DUEL — NI23 G4 Final 7 (@lilywonder1) · THE FULL RECORD

## Duel A vs B (both rendered 1024x1024, judged shrunk to 300x300)
- Variant A: full-width Lisbon lead, then 12 cards in a 3-wide grid,
  title 24px, facts 14px. File 223,370 bytes.
- Variant B: compact masthead, 12 cards in a 2-wide grid. File 208,857 bytes.
  At full size its DAY IN NUMBERS rows overlap and its footer is clipped
  at the bottom edge; at 300px its bottom third turns to mush.
- WINNER: A. At 300x300 every A headline stays legible, the grid reads as
  one clear newspaper page, and nothing is clipped: all 13 card facts fit
  inside their cards, ALSO ON THE DAY (27 items) and all three HOW SURE
  WE ARE lines are fully on the page. B is smaller but less readable,
  and readability is the deciding axis, so the tie-break on size never
  comes into play.

## Gerbang Tembak Pengganti — winner A vs standing entry G3
Standing: G3 "THE WORLD DISPATCH", build 317,402 bytes, sha 669c11c9...,
13 cards, cream palette (data supplied by coordinator; repo not opened).

Measured axes:
- File size: A 223,370 B vs G3 317,402 B — A is 94,032 B (29.6%) smaller;
  exact ties in judging go to the smaller file.
- Breadth, counted on the page: A carries 40 stories (13 cards + 27
  numbered ALSO ON) across 8 regions, and its colour region strip sums
  to exactly 40 (Europe 8, Middle East 4, N. America 6, S. Asia 13,
  Global 3, SE Asia 3, Africa 2, Asia-Pacific 1).
- Consensus trio of 23 Nov all present as cards: #2 Hormuz tankers,
  #3 IRGC Patriot claim, #4+#5 Kyiv (boy pulled alive; 14 missing).
  Account lead #1 is pool #15, the Lisbon cost-of-living march.
- Faithfulness audit (zero-bound standard): the IRGC story is framed as
  a claim in its headline and carries a CLAIM chip; the Kyiv missing
  story is attributed in its headline ("..., Zelenskiy Says"); the
  Finland ship "still burns", never "sunk". No claim is printed as fact.
- DATE CHECK names 7 dated discards (19/18/21/22 Nov) and contradicts no
  card: the Indonesia factory fire itself is listed as a 22 Nov discard,
  and only its 23 Nov update numbers (7 found, 50 missing) are used.
- Honest furniture: kicker "52 reports cross-checked"; prices/weather
  strip prints NO DAY-POOL WIRE instead of invented figures; timeline
  times only the two slots the pool times (00:02Z, 02:00Z), other slots
  labelled by part of day; THE DAY IN NUMBERS holds 8 pool figures;
  map pins carry card numbers with a legend; no text anywhere implies
  a day other than Monday 23 November 2026; no garbled text found on
  visual inspection at full size and at 300x300.

VERDICT vs G3: LEBIH KUAT (stronger on size, counted breadth, claim
framing, date-check consistency and completeness of furniture).

## Entry
- entry.png: 223,370 bytes, 1024x1024
- sha256: fc602b792b63a54222e67e45f3bf586a3435de9a71142d979d168378608a1413
- Anchor commit: cc51d8953d5686518c06336ea2b8d9bfff6b1d59
- Staging commit: recorded in the git log of this staging repo
  (message "NI23 G4 final7: THE FULL RECORD"); hash reported to the
  coordinator in the build report.
